'''
Copyright 2021 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from time import sleep

default_command_end = '\n'
default_buffer = 100
default_timeout = 1
default_delay = .5
standard_prompt_endings = ('>', '#', '> ', '# ')


class BaseEngine(ABC):

    def __init__(self):
        self.hostname = ''
        self.prompt = None
        self.enable_password = None
        self.commands_sent_since_last_output_get = 0
        self.all_commands_sent = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def _extract_prompt(self, output):
        """
        Attempts to get last line of output, if successful checks for the standard prompt ending in
        the last line, if one is found, it splits the line by the prompt ending and sets the prompt to the
        first element plus the prompt ending and quits checking if any remain
        """
        try:
            last_line_of_output = output[-1].strip()
        except IndexError:
            return
        for prompt_ending in standard_prompt_endings:
            if prompt_ending in last_line_of_output:
                self.prompt = f'{last_line_of_output.split(prompt_ending)[0]}{prompt_ending}'
                return

    def send_command(self, command, end=default_command_end):

        self.commands_sent_since_last_output_get += 1
        self.all_commands_sent.append(command)
        return self._send_command(command, end)

    def get_output(self, buffer_size=default_buffer, timeout=default_timeout, no_command_sent_previous=False):
        """
        Gets the output that is being returned from the network device. It checks how many commands were run
        since the last time it got output, and will get output until a prompt is encountered. Each command
        should return the prompt after execution so if the user enters 6 commands, this will loop 6 times
        to get the output of all 6 commands. It is up to the user to either get data between all 6 commands
        or parse it out theirselves. If no command is sent, to loop through a single time set the
        'no_command_sent_previous' flag to True so it auctually attempts to gather output. The reason
        for manually setting that flag is so that if the user attempts to get output when there is none
        and has a higher timeout it will not try and gather output and hang. If the user wants to get output
        without sending a command they should know to expect some output.

        This could run into issues if there is logging enabled on the terminal but that is not something
        that is being done inside the framework at this time so I dont believe there is a need to change that.
        """

        if no_command_sent_previous:
            self.commands_sent_since_last_output_get += 1

        output = ''
        for x in range(self.commands_sent_since_last_output_get):
            data = '\n'
            end = datetime.now() + timedelta(seconds=timeout)

            # while the last line of output DOES NOT START with the hostname AND DOES NOT CONTAIN a standard prompt ending
            while not all([data.splitlines()[-1].startswith(self.hostname), any([x in data.splitlines()[-1] for x in standard_prompt_endings])]):
                from_device = self._get_output(buffer_size)
                if from_device:
                    data += from_device
                    end = datetime.now() + timedelta(seconds=timeout)  # reset timeout clock
                else:
                    if datetime.now() > end:
                        # timeout clock triggered, break out of loop because we must be at a point
                        # in the CLI where it does not return a prompt or is hung
                        break
                    sleep(.1)
            output += data[1:]

        self.commands_sent_since_last_output_get = 0

        if type(output) != list:
            output = output.splitlines()

        self._extract_prompt(output)

        return output

    def send_command_get_output(self, command, end=default_command_end, buffer_size=default_buffer, timeout=default_timeout, delay=default_delay):
        self.send_command(command, end)
        if delay:
            sleep(delay)
        return self.get_output(buffer_size, timeout)

    @property
    def in_user_exec_mode(self) -> bool:
        if self.prompt.endswith('>'):
            return True
        return False

    @property
    def in_privileged_exec_mode(self) -> bool:
        if self.prompt.endswith('#') and not self.prompt.endswith(')#'):
            return True
        return False

    @property
    def in_configuration_mode(self) -> bool:
        if self.prompt.endswith(')#'):
            return True
        return False

    @abstractmethod
    def connect_to_server(self, ip, username, password, port) -> bool:
        pass

    @abstractmethod
    def _send_command(self, command, end) -> None:
        pass

    @abstractmethod
    def _get_output(self, buffer_size) -> str:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass


class SSHEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.shell = None
        self.timeout = 10

    def connect_to_server(self, ip, username, password, port):
        self.client.connect(hostname=ip, port=port, username=username, password=password, timeout=self.timeout)
        self.shell = self.client.invoke_shell()
        self.prompt, self.hostname = self._get_prompt_and_hostname()

    def _get_output(self, buffer_size):
        if self.shell.recv_ready():
            return bytes.decode(self.shell.recv(buffer_size))
        return ''

    def _send_command(self, command, end='\n'):
        self.shell.send(f'{command}{end}')

    def close_connection(self):
        self.client.close()

    # Methods required for some lower level SSH handling. These methods should not be called outside of this class

    def _send_space_get_data(self, timeout=1):
        self._send_command('', end='\n')
        end = datetime.now() + timedelta(seconds=timeout)
        data = ''
        while not data.endswith(standard_prompt_endings):
            from_device = self._get_output(1000)
            if from_device:
                data += from_device
                end = datetime.now() + timedelta(seconds=timeout)
            else:
                sleep(.1)
                if datetime.now() >= end:
                    break
        return data

    def _prompt_lookup(self, output_data):
        """
        Recursive method that will try and find the prompt in the last 3 lines of config, if not
        will send a space, get the data and call itself to run again
        """

        prompt = None
        for line in reversed(output_data.splitlines()[-3:]):
            if len(line.split()) == 1 and any(x in line for x in standard_prompt_endings):
                prompt = line.strip().replace('\r\n', '')
                break
        if not prompt:
            return self._prompt_lookup(self._send_space_get_data())

        return prompt

    def _get_prompt_and_hostname(self):
        # gets initial prompt out of device
        output = ''
        while not output.endswith(standard_prompt_endings):
            data = self._get_output(100)
            output += data
        prompt = self._prompt_lookup(output)

        # prompt = data.splitlines()[-1].strip()
        hostname = prompt[:-1]
        return prompt, hostname

    # End low level methods