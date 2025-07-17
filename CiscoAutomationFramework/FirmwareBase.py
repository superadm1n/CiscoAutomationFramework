from CiscoAutomationFramework.TransportEngines import BaseEngine, default_buffer, default_timeout, \
    default_command_end, default_delay
from CiscoAutomationFramework.Exceptions import EnablePasswordError
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser
from abc import ABC, abstractmethod
from inspect import getmodule


class CiscoFirmware(ABC):

    def __init__(self, transport):
        if not isinstance(transport, BaseEngine):
            raise TypeError(f'transport object MUST be an instance of {getmodule(BaseEngine).__name__}.{BaseEngine.__name__}')
        self._terminal_length_value = None
        self._terminal_width_value = None
        self.transport = transport
        #self.terminal_length()

    @property
    def is_nexus(self) -> bool:
        """
        Returns True/False if the Cisco device is a Nexus

        :return: True/False
        :rtype: bool
        """
        return False

    @property
    def commands_sent(self) -> list:
        """
        A list of all commands sent to the device in the order they are entered from first to last in the
        current session

        :return: List of commands sent
        :rtype: list
        """
        return self.transport.all_commands_sent


    def cli_to_config_mode(self) -> bool:
        """
        Navigates the CLI into config mode regardless of where it is

        :return: True/False
        :rtype: bool
        """
        if self.transport.in_user_exec_mode:
            self.cli_to_privileged_exec_mode()

        if self.transport.in_privileged_exec_mode:
            self.transport.send_command_get_output('config t')

        return self.transport.in_configuration_mode

    def cli_to_privileged_exec_mode(self) -> bool:  # TODO: Enable password typing will fail trying to get output. Fix!
        """
        Navigates the CLI into prvileged exec mode regardless of where it is. Will raise an EnablePasswordError
        if the transport engine does not have an enable password set and the network device asks for one.

        :return: True/False
        :rtype: bool

        :raises: CiscoAutomationFramework.Exceptions.EnablePasswordError
        """
        if self.transport.in_privileged_exec_mode:
            return True
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
    def prompt(self) -> str:
        """
        Returns the latest prompt that was returned from the device

        :return: Latest prompt returned from device
        :rtype: str
        """
        return self.transport.prompt

    @property
    def hostname(self) -> str:
        """
        Hostname of the Cisco device.

        :return: Hostname
        :rtype: str
        """
        return self.transport.hostname

    @property
    def config_parser(self):
        self.cli_to_privileged_exec_mode()
        return ConfigParser(self.running_config)

    def send_command_get_output(self, command, end=default_command_end, buffer_size=default_buffer,
                                timeout=default_timeout, delay=default_delay) -> list:
        """
        Sends a command to the device and returns the output from the device. If there were multiple commands sent
        this will gather the output from all the commands at once. This command is a combination of send_command
        and get_output.

        :param command: Command to send
        :param end: End character (default \n)
        :param buffer_size: Size of buffer when getting output from device. You shouldnt have to modify this much
        :param timeout: Time to stop waiting for output if no output is received.
        :param delay: Time to wait before gathering output from device
        :return: Output from device starting with command, ending with prompt in a list split by line
        :rtype: list
        """
        return self.transport.send_command_get_output(command, end, buffer_size, timeout, delay)

    def send_command(self, command, end=default_command_end) -> None:
        """
        Sends command to device, does not get any output. You should not need to run this directly often

        :param command: Command to send
        :param end: End character (default \n)
        :return: Nothing
        """
        return self.transport.send_command(command, end)

    def get_output(self, buffer_size=default_buffer, timeout=default_timeout) -> list:
        """
        Gets output from the device until the prompt is returned or the timeout is reached. You should not need
        to run this directly often.

        :param buffer_size: Size of buffer when getting output from device. You shouldnt have to modify this much
        :param timeout: Time to stop waiting for output if no output is received.
        :return:
        """
        return self.transport.get_output(buffer_size, timeout)

    def send_question_get_output(self, command) -> list:
        """
        Special method to get the output from sending a command with a question mark. This will
        send the command with a trailing '?' get the output from that and then erase the command
        that is returned on the ending prompt. You should NOT put a question mark in the command
        this function will handle that for you but if you do, it will be removed so the CLI doesnt do something
        that is not expected

        :param command: Command to inspect
        :return: list of possible command completions, or next possible words in command
        :rtype: list
        """
        if command.endswith('?'):
            command = command.replace('?', '')
        question_output = self.send_command_get_output(command, end=' ?')

        # get rid of command that was sent from the terminal, to do that construct list of backspaces
        # The question mark is not returned as a part of the next prompt line but the space is, account for that.
        backspaces = ''.join([chr(8) for _char in range(len(command) + 1)])
        self.send_command_get_output(backspaces, end='')

        return question_output

    def close_connection(self) -> None:
        """
        Closes connection to device

        :return: Nothing
        """
        return self.transport.close_connection()

    def terminal_length(self, n='0'):
        """
        Sets terminal length of shell

        :param n: length
        :type n: str
        :return: Nothing
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

        :param n: width
        :type n: str
        :return:
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
    def uptime(self) -> str:
        """
        Returns uptime of device

        :return: Uptime
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def interfaces(self) -> list:
        """
        List of interfaces on device

        :return: Interfaces
        :rtype: list
        """
        pass

    @property
    @abstractmethod
    def mac_address_table(self) -> str:
        """
        Returns the MAC address table in its raw form

        :return: MAC Address Table
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def arp_table(self) -> str:
        """
        Returns the arp table in its raw form

        :return: Arp Table
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def running_config(self) -> str:
        """
        Returns running config in its raw form

        :return: Running Configuration
        :rtype: str
        """
        pass

    @property
    @abstractmethod
    def startup_config(self) -> str:
        """
        Returns startup config in its raw form

        :return: Startup Config
        :rtype: str
        """
        pass

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

        :return: Nothing
        """
        pass

    @abstractmethod
    def add_local_user(self, username, password, password_code=0, *args, **kwargs):
        """
        Method here should be generating a string that the network device accepts in the following format
        'username USERNAME <args> <kwarg key> <kwarg value>  password PASSWORD_CODE PASSWORD'

        :param username: Username to use
        :param password: Password to set (cleartext or encrypted depending on password_code)
        :param password_code: Code for password you are providing
        :param args: Single word arguments in command string
        :param kwargs: Key word arguments in command string
        :return: Nothing
        """
        pass

    @abstractmethod
    def delete_local_user(self, username):
        """
        Deletes a locally defined user on device

        :param username: username to delete
        :type username: str
        :return: Nothing
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close_connection()


