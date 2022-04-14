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
from CiscoAutomationFramework.TransportEngines import BaseEngine, default_buffer, default_timeout, \
    default_command_end, default_delay
from CiscoAutomationFramework.Exceptions import EnablePasswordError
from abc import ABC, abstractmethod
from inspect import getmodule


class CiscoFirmware(ABC):

    def __init__(self, transport):
        if not isinstance(transport, BaseEngine):
            raise TypeError(f'transport object MUST be a sub class of {getmodule(BaseEngine).__name__}.{BaseEngine.__name__}')
        self._terminal_length_value = None
        self._terminal_width_value = None
        self.transport = transport
        #self.terminal_length()

    def cli_to_config_mode(self):
        """
        Navigates the CLI into config mode regardless of where it is
        """
        self.cli_to_privileged_exec_mode()
        self.transport.send_command_get_output('config t')
        return self.transport.in_configuration_mode

    def cli_to_privileged_exec_mode(self):  # TODO: Enable password typing will fail trying to get output. Fix!
        """
        Navigates the CLI into prvileged exec mode regardless of where it is. Will raise an EnablePasswordError
        if the transport engine does not have an enable password set and the network device asks for one.
        """
        if self.transport.in_privileged_exec_mode:
            return None
        if self.transport.in_configuration_mode:
            self.transport.send_command_get_output('end')
            return self.transport.in_privileged_exec_mode

        if self.transport.in_user_exec_mode:
            enabling_output = self.transport.send_command_get_output('enable')
            if self.transport.prompt not in enabling_output:
                if not self.transport.enable_password:
                    raise EnablePasswordError('No enable password provided, network device is asking for one!')
                self.transport.send_command_get_output(self.transport.enable_password)
                return self.transport.in_privileged_exec_mode

    @property
    def prompt(self):
        """
        Returns the latest prompt that was returned from the device
        """
        return self.transport.prompt

    @property
    def hostname(self):
        """
        Returns the hostname
        """
        return self.transport.hostname

    def send_command_get_output(self, command, end=default_command_end, buffer_size=default_buffer,
                                timeout=default_timeout, delay=default_delay):
        """
        Sends a command to the device and returns the output from the device. If there were multiple commands sent
        this will gather the output from all the commands at once
        """
        return self.transport.send_command_get_output(command, end, buffer_size, timeout, delay)

    def send_command(self, command, end=default_command_end):
        """
        Sends command to device, does not get any output
        """
        return self.transport.send_command(command, end)

    def get_output(self, buffer_size=default_buffer, timeout=default_timeout):
        """
        Gets output from the device until the prompt is returned or the timeout is reached
        """
        return self.transport.get_output(buffer_size, timeout)

    def send_question_get_output(self, command):
        """
        Special method to get the output from sending a command with a question mark. This will
        send the command with a trailing '?' get the output from that and then erase the command
        that is returned on the ending prompt. You should NOT put a space in the command but
        if you do, it will be removed.
        """
        if command.endswith('?'):
            command = command.replace('?', '')
        question_output = self.send_command_get_output(command, end=' ?')

        # get rid of command that was sent from the terminal, to do that construct list of backspaces
        # The question mark is not returned as a part of the next prompt line but the space is, account for that.
        backspaces = ''.join([chr(8) for _char in range(len(command) + 1)])
        self.send_command_get_output(backspaces)

        return question_output

    def close_connection(self):
        """
        Closes connection to device
        """
        return self.transport.close_connection()

    def terminal_length(self, n='0'):
        """
        Sets terminal length of shell
        """
        if self._terminal_length_value:
            if self._terminal_length_value != int(n):
                self._terminal_length_value = int(n)
                return self._terminal_length(n)
        else:
            self._terminal_length_value = int(n)
            return self._terminal_length(n)

    def terminal_width(self, n='0'):
        """
        Sets terminal width of shell
        """
        if self._terminal_width_value:
            if self._terminal_width_value != int(n):
                self._terminal_width_value = int(n)
                return self._terminal_width(n)
        else:
            self._terminal_width_value = int(n)
            return self._terminal_width(n)

    # Begin abstract properties

    @property
    @abstractmethod
    def uptime(self):
        """
        Returns uptime
        """
        pass

    @property
    @abstractmethod
    def interfaces(self):
        """
        Returns interfaces on the device
        """
        pass

    @property
    @abstractmethod
    def mac_address_table(self):
        """
        Returns the MAC address table in its raw form
        """
        pass

    @property
    @abstractmethod
    def arp_table(self):
        """
        Returns the MAC address table in its raw form
        """
        pass

    @property
    @abstractmethod
    def running_config(self):
        """
        Returns running config in its raw form
        """
        pass

    @property
    @abstractmethod
    def startup_config(self):
        """
        Returns startup config in its raw form
        """

    # Begin abstract methods

    @abstractmethod
    def _terminal_length(self, n='0'):
        pass

    @abstractmethod
    def _terminal_width(self, n='0'):
        pass

    @abstractmethod
    def save_config(self):
        """
        Saves running config to startup config
        """
        pass

    @abstractmethod
    def add_local_user(self, username, password, password_code=0, *args, **kwargs):
        """Method here should be generating a string that the network device accepts in the following format
        'username USERNAME <args> <kwarg key> <kwarg value>  password PASSWORD_CODE PASSWORD'"""
        pass

    @abstractmethod
    def delete_local_user(self, username):
        """
        Deletes a locally defined user on device
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close_connection()


