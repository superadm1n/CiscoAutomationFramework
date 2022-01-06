from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from time import sleep

default_command_end = '\n'
default_buffer = 1
default_timeout = 1

class BaseEngine(ABC):

    def __init__(self):
        self.hostname = None
        self.prompt = None
        self.enable_password = None

    def send_command(self, command, end=default_command_end):
        return self._send_command(command, end)

    def get_output(self, buffer_size=default_buffer, timeout=default_timeout):
        from_device = self._get_output(buffer_size, timeout)
        if type(from_device) is not list:
            return from_device.splitlines()
        return from_device

    def send_command_get_output(self, command, end=default_command_end, buffer_size=default_buffer, timeout=default_timeout):
        self.send_command(command, end)
        return self.get_output(buffer_size, timeout)

    @property
    def in_user_exec_mode(self):
        if self.prompt.endswith('>'):
            return True
        return False

    @property
    def in_privileged_exec_mode(self):
        if self.prompt.endswith('#') and not self.prompt.endswith(')#'):
            return True
        return False

    @property
    def in_configuration_mode(self):
        if self.prompt.endswith(')#'):
            return True
        return False

    @abstractmethod
    def connect_to_server(self, ip, username, password, port):
        pass

    @abstractmethod
    def _send_command(self, command, end):
        pass

    @abstractmethod
    def _get_output(self, buffer_size, timeout):
        pass

    @abstractmethod
    def close_connection(self):
        pass


class SSHEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.commands_sent_since_last_output_get = 0
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.shell = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_to_server(self, ip, username, password, port):
        self.client.connect(hostname=ip, port=port, username=username, password=password)
        self.shell = self.client.invoke_shell()
        #_ = bytes.decode(self.shell.recv(1000))  # capture first bit of data
        self.prompt, self.hostname = self._get_prompt_and_hostname()

    def _get_prompt_and_hostname(self):
        timeout = .5
        self.send_command('', end='\n')
        end = datetime.now() + timedelta(seconds=timeout)
        data = ''
        while True:
            if self.shell.recv_ready():
                data = bytes.decode(self.shell.recv(1000))
                end = datetime.now() + timedelta(seconds=timeout)
            else:
                if datetime.now() >= end:
                    break

        prompt = data.splitlines()[-1].strip()
        hostname = prompt[:-1]
        return prompt, hostname


    def _get_output(self, buffer_size, timeout):
        output = ''

        for x in range(self.commands_sent_since_last_output_get):
            data = '\n'
            end = datetime.now() + timedelta(seconds=timeout)
            # while the last line of output doesnt start with the hostname or end with a > or a #
            while not all([data.splitlines()[-1].startswith(self.hostname), data.splitlines()[-1].endswith(('>', '#'))]):
                if self.shell.recv_ready():
                    data += bytes.decode(self.shell.recv(buffer_size))
                    end = datetime.now() + timedelta(seconds=timeout)  # reset timeout clock
                else:
                    sleep(.1)
                    if datetime.now() > end:
                        # timeout clock triggered, break out of loop because we must be at a point
                        # in the CLI where it does not return a prompt or is hung
                        break
            output += data[1:]

        return output.splitlines()


    def _send_command(self, command, end='\n'):
        self.commands_sent_since_last_output_get += 1
        self.shell.send(f'{command}{end}')

    def close_connection(self):
        self.client.close()