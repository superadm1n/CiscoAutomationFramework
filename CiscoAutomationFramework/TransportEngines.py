'''
Copyright 2018 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

========================================================================

This module contains the code that is the transport engines and the interface to the engines.
The rest of the framework will call the transport interface to send and receive data and based
on what parameter is passed the interface will chose the correct engine to use to send the data.


'''

from abc import ABC, abstractmethod
import serial
from paramiko import SSHClient, AutoAddPolicy
import time
import logging
from . import CustomExceptions
from CiscoAutomationFramework import log_level, log_to_console
from threading import Thread
from .CustomExceptions import MethodNotImplemented
from datetime import datetime, timedelta

default_buffer_size = 1
default_timeout = 2

class BaseClass(ABC):
    '''
    This class contains all of the API calls that will be presented to the user and the rest of the package
    in a standard way. They are the calls that the methods of the rest of the package uses to interact with
    the switch, for instance the command methods held within CiscoIOS use these calls, and when writing your
    scripts you can access these methods via the transport variable.

    All of these API calls are responsible for handling the interacting with the Cisco device ex. Opening the
    connection, closing the connection, sending, and recieving data.

    Note that when receiving data it is the raw data as returned from the switch so you will need to parse it
    yourself to make it more programmatically meaningful.


    '''

    def __init__(self, error_handler=None):
        super().__init__()
        self.prompt = ''
        self.hostname = ''
        self.shell = None
        self.total_discarded_buffer_bytes = 0
        self.enable_password = ''
        self.terminal_length_value = None
        self.terminal_width_value = None
        self.error_handler = error_handler
        self.last_issued_command = None

        self._output = ''

    def __enter__(self):
        '''
        Required to allow the class to be used inside a 'with' statement (with Ciscossh() as ssh:)

        :return: self object
        '''

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Required to allow the class to be used inside a 'with' statement (with Ciscossh() as ssh:) THis function is
        called when the 'with' statement is exited.

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: Nothing
        '''

        self.close_connection()

    @abstractmethod
    def close_connection(self):
        '''Closes the connection to the Cisco device

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    @abstractmethod
    def _send_command(self, command, end):
        pass

    @abstractmethod
    def _get_output(self, buffer_size, timeout):
        pass

    @abstractmethod
    def connect_to_server(self, ip, username, password, port=22):
        pass

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

    def _pre_parser(self, output):
        '''Pre parser that will process the output from the device prior to passing it up to the user.

        :param output: Output from the device in a list
        :return: Nothing
        '''
        if type(output) is not list:
            output = output.splitlines()
        for line in output:
            if line.startswith('%') and self.error_handler:
                self.error_handler(line, self.last_issued_command)

    def send_command(self, command, end='\n'):
        '''Method to send command to the device. This method will automatically send the return character
        so there is no need to put that in the command

        :param command: Command to send
        :return: Nothing
        '''
        self.last_issued_command = command
        return self._send_command(command, end)

    def get_output(self, return_as_list=True, buffer_size=default_buffer_size, timeout=default_timeout):
        '''This method gathers the data that is waiting from the Cisco device and then returns it
        for further parsing or directly to the user.

        :param wait_time:
        :param detecting_firmware:
        :param return_as_list:
        :param buffer_size:
        :param timeout:
        :return:
        '''

        output = self._get_output(buffer_size, timeout)

        self._pre_parser(output)

        try:
            self.prompt = output[-1]
        except IndexError:
            pass

        if return_as_list is False:
            # Formats the output as a string and returns it
            return '\n'.join(output)
        # return output as a list
        return output

    def send_command_get_output(self, command, return_as_list=False, buffer_size=default_buffer_size, timeout=default_timeout):
        '''Sends command and returns the output to the Cisco device. This method returns the raw data

        :param command: Command to send to the device
        :param return_as_list: Set to True to return the output as a list
        :param buffer_size: Number of bytes to return at a time
        :param timeout:
        :return:
        '''
        self.send_command(command)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size, timeout=timeout)


class SSHEngine(BaseClass):
    def __init__(self, error_handler=None):
        super().__init__(error_handler)
        self.commands_sent_since_last_output_get = 0

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.shell = None
        self.hostname = None
        self.prompt = None

    def connect_to_server(self, ip, username, password, port=22):

        self.client.connect(ip, port, username=username, password=password, look_for_keys=False, allow_agent=False)
        self.shell = self.client.invoke_shell()

        self.prompt = bytes.decode(self.shell.recv(1000)).replace('\r\n', '')
        self.hostname = self.prompt[:-1]

    def _get_output(self, buffer_size, timeout):
        """Gathers all available output from the server if a command was run but output was not already
        gathered. If multiple commands were run, it will gather output for all commands."""

        output = ''

        for x in range(self.commands_sent_since_last_output_get):
            data = '\n'
            end = datetime.now() + timedelta(seconds=timeout)
            # while the last line of output doesnt start with the hostname or end with a > or a #
            while not all([data.splitlines()[-1].startswith(self.hostname), data.splitlines()[-1].endswith(('>', '#'))]):
                if self.shell.recv_ready():
                    data += bytes.decode(self.shell.recv(buffer_size))
                    end = datetime.now() + timedelta(seconds=1)  # reset timeout clock
                else:
                    if datetime.now() > end:
                        # timeout clock triggered, break out of loop because we must be at a point
                        # in the CLI where it does not return a prompt or is hung
                        break
            output += data[1:]


        self.commands_sent_since_last_output_get = 0
        return output.splitlines()

    def _send_command(self, command, end):
        self.commands_sent_since_last_output_get += 1
        self.shell.send(f'{command}{end}')

    def close_connection(self):
        self.client.close()

