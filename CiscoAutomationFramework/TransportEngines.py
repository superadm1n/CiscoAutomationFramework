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


import serial
import paramiko
import time
import threading
import logging
from . import CustomExceptions
from CiscoAutomationFramework import log_level, log_to_console
from .CustomExceptions import MethodNotImplemented

level = log_level
logFile = 'CiscoAutomationFramework.log'

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.propagate = False

file_handler = logging.FileHandler(logFile)
file_handler.setLevel(log_level)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)

logFormatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s')

file_handler.setFormatter(logFormatter)
stream_handler.setFormatter(logFormatter)

try:
    logger.addHandler(file_handler)
    if log_to_console:
        logger.addHandler(stream_handler)
except PermissionError:
    print('Permission denied when attempting to write log file, disabling logging')
    logger.disabled = True


class BaseClass:
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

    def __init__(self):
        self.prompt = ''
        self.hostname = ''
        self.shell = None
        self.total_discarded_buffer_bytes = 0
        self.enable_password = ''
        self.terminal_length_value = None
        self.terminal_width_value = None

        self._output = ''

    def _pre_parser(self, output):
        '''Basic pre parser that will process the output from the device prior to passing it up to the user.
        Right now it simply checks for an error and logs it in the log file.

        :param output: Output from the device in a list
        :return: Nothing
        '''
        for line in output:
            if line.startswith('%'):
                logger.error('Error detected! - {}'.format(line))

    def connect_to_server(self):
        '''High level function that will call all the engine specific methods to connect to the server.
        For instance if it is connecting via ssh it will call whatever private methods it needs to so it
        has access to the console, for serial it will end up at the console but call different private methods
        in the serial engine class

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def send_command(self, command):
        '''Method to send command to the device. This method will automatically send the return character
        so there is no need to put that in the command

        :param command: Command to send
        :return: Nothing
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def get_output_different_prompt(self, wait_time=.2, return_as_list=False, buffer_size=1, timeout=10):
        '''Gets the outpu from the device when a different prompt is anticipated. This method will soon be
        depreciated as there is a more robust algorthem used in the get_output method

        .. WARNING::
            This method has been depreciated and will be removed in the future

        :param wait_time:
        :param return_as_list:
        :param buffer_size:
        :param timeout:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def get_output(self, wait_time, detecting_firmware, return_as_list, buffer_size, timeout):
        '''This method gathers the data that is waiting from the Cisco device and then returns it
        for further parsing or directly to the user.

        .. note::
            For Developers: This method should not be overwritten but rather extended via super() as it contains
            code that regardless of the engine, needs to run.

        :param wait_time:
        :param detecting_firmware:
        :param return_as_list:
        :param buffer_size:
        :param timeout:
        :return:
        '''

        output = self._output.splitlines()[2:]

        if detecting_firmware is True:
            # This is needed because of the way CAF detects firmware, it will leave extra lines of the prompt in the buffer
            # and methods grabbing data downstream will cause issues on other commands. This will take those lines from the buffer
            # and throw them away this  will only run if this method is run with the 'detecting_firmware' flag set to 'True'
            # to prevent necessary data from being thrown away.
            self.total_discarded_buffer_bytes += self.throw_away_buffer_data()
        self._pre_parser(output)
        self.prompt = output[-1]

        if return_as_list is False:
            # Formats the output as a string and returns it
            return '\n'.join(output)
        # return output as a list
        return output

    def send_command_get_output(self, command, return_as_list=False, buffer_size=1, timeout=10):
        '''Sends command and returns the output to the Cisco device. This method returns the raw data
        .. NOTE::
          This will soon be replace the send_command_expect_different_prompt and
          send_command_expect_same_prompt methods.

        :param command: Command to send to the device
        :param return_as_list: Set to True to return the output as a list
        :param buffer_size: Number of bytes to return at a time
        :param timeout:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def send_command_expect_different_prompt(self, command, return_as_list=False, buffer_size=1, timeout=10):
        '''.. WARNING::
            This method has been depreciated and will be removed in the future

        This is a high level method that will send a command to the Cisco device and automatically gather the output.


        :param command:
        :param return_as_list:
        :param buffer_size:
        :param timeout:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def send_command_expect_same_prompt(self, command, timeout=10, detecting_firmware=False, return_as_list=False, buffer_size=1):
        '''.. WARNING::
            This method has been depreciated and will be removed in the future
        High level method to send a command to a Cisco device and automatically gather the output. This is the method that should be used
        each time you need to send a command and grab the output from a Cisco device

        :param command:
        :param timeout:
        :param detecting_firmware:
        :param return_as_list:
        :param buffer_size:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def close_connection(self):
        '''Closes the connection to the Cisco device

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def throw_away_buffer_data(self):
        '''Method to gather data from a Cisco device and throw away the output. This method
        is typically only used when determining what Firmware the Cisco device.

        :return: int: total bytes discarded from the buffer
        :rtype: int
        '''

        bytes_discarded = 0

        while True:
            if self.shell.recv_ready():
                bytes.decode(self.shell.recv(1))
                bytes_discarded += 1
                time.sleep(.01)
            else:
                break

        return bytes_discarded


class SSHEngine(BaseClass):
    def __init__(self):
        BaseClass.__init__(self)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.sshPort = 22

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

    def send_command_get_output(self, command, return_as_list=False, buffer_size=1, timeout=10):
        self.send_command(command)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size, timeout=timeout)

    def send_command_expect_different_prompt(self, command, return_as_list=False, buffer_size=1, timeout=10):
        '''
        High level method for sending a command when expecting the prompt to return differently. This uses the
        SSHEngine methods of send_command and get_output_different_prompt

        :param command: command to issue on the server as typed directly from command line
        :param return_as_list: returns the output as a list vs a string, string is default
        :return: output from command in either string or list format

        Note: The Purpose of this method is to provide an interface to type commands that are
        not otherwise satisfied in another method. Make all attempts to not use this method if possible
        as you will have to integrate more error checking and contingency planning in the main body of
        the code when it should be handled in the class
        '''

        self.send_command(command)

        return self.get_output(
            return_as_list=return_as_list,
            buffer_size=buffer_size,
            timeout=timeout
        )

    def send_command_expect_same_prompt(self, command, timeout=10, detecting_firmware=False, return_as_list=False, buffer_size=1):
        '''
        Sends commands and gathers the output in a way that expects the same prompt to be returned
        DO NOT use this method if you are not SURE that the prompt returned will be the same

        :param command: Command to issue to device
        :param detecting_firmware: set to true if you want to throw away buffer data for detecting firmware
        :param return_as_list: returns the output as a list vs a string, string is default
        :return: Output from command in either string or list format
        '''

        self.send_command(command)

        return self.get_output(
            detecting_firmware=detecting_firmware,
            return_as_list=return_as_list,
            buffer_size=buffer_size,
            timeout=timeout
        )

    def connect_to_server(self, ip, username, password):
        '''
        Makes initial connection to server and calls method to invoke shell

        :param ip: IP of server
        :type ip: str
        :param username: username for the server
        :type username: str
        :param password: password for the server
        :type password: str
        :raises AuthenticationError: raised if the method cant authenticate the user
        :raises ConnectionError: Raised if this method can't connect to the IP address on specified port
        :return: string "Connection Succesful"
        '''
        try:
            self.client.connect(ip, port=self.sshPort, username=username,
                                password=password, look_for_keys=False, allow_agent=False)  # Makes connection to server

        except paramiko.ssh_exception.AuthenticationException:
            raise CustomExceptions.LoginFailed('Unable to login to device with supplied username and password')


        except paramiko.ssh_exception.NoValidConnectionsError:
            raise CustomExceptions.ConnectionError(
                'Unable to connect to server {} on port {}!'.format(ip, self.sshPort))

        else:
            time.sleep(.1)
            self._invoke_shell()
            self._get_initial_prompt()
            return 'Connection Successful'

    def _invoke_shell(self):
        '''
        Invokes shell with remote server

        :return: Prompt supplied from server
        :raises InvokeShellError: Raised if the the server is unable to invoke a shell
        '''

        try:
            self.shell = self.client.invoke_shell()
        except paramiko.ssh_exception.SSHException:
            raise CustomExceptions.InvokeShellError('Unable to Invoke Shell in SSHEngine Class')

        # I think to stop the second exception I should add a longer wait time here
        return True

    def _get_initial_prompt(self):
        '''
        Gathers the initial prompt from the remote device

        :return: Output from device
        '''

        output = self.get_output(wait_time=.5)

        # At times the server will return the data in the 1st line, and others the second line, this try except block handles that
        try:
            # Sends return key and grabs the prompt that is returned, subtracting 1 character to give the hostname
            self.send_command('')
            output = self.get_output(return_as_list=True)
            for line in output:
                if line is not '' and line is not ' ':
                    self.hostname = line[:-1]
                    break

        except IndexError:

            try:
                self.hostname = output[0][:-1]
            except IndexError:
                print('This is the second exception\nBegin Output\n{}\nEnd Output'.format(output))

        return output

    def send_command(self, command):

        '''
        Method for sending a command to the remote device

        :param command: Command to issue as it is typed on the command line
        :return: Nothing
        '''

        self.shell.send('{}\n'.format(command))

    def get_output_different_prompt(self, wait_time=.2, return_as_list=False, buffer_size=1, timeout=10):
        return self.get_output(wait_time = wait_time, return_as_list=return_as_list, buffer_size=buffer_size,
                               timeout=timeout, detecting_firmware=False)

    def get_output(self, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1, timeout=10):

        '''
        .. warning:: Only use this method if you are sure the last line of output of the server will be the
            prompt that was previously returned and stored in self.prompt

        Method to capture output from the server, should be run whenever issuing a command
        This method will loop until the last line of output from the server matches self.prompt
        so there is a possibility of an infinate loop if the server does not return the same prompt
        in the last line of output.

        :param wait_time: The time to wait before gathering buffer data (used to give the device time to fill the buffer
        :type wait_time: float
        :param detecting_firmware: Default set to false, if set to true it triggers to disgard buffer data after \
        the prompt is encountered, this is useful if you need to issue multiple enter keystrokes after a command.
        :type detecting_firmware: bool
        :param return_as_list: default set to False will return as a string, set to True it will output as a list \
        split by lines
        :type return_as_list: bool
        :param buffer_size: Number of bytes to gather at a time when retrieving data from buffer
        :type buffer_size: int

        :return: Output from server in string or list format
        '''

        time.sleep(wait_time)
        self._output = '\n\n'
        #output = '\n\n'

        while True:
            self._output += bytes.decode(self.shell.recv(buffer_size))
            self.recievedData = True
            if '>' in self._output.splitlines()[-1] or '#' in self._output.splitlines()[-1] and not self.shell.recv_ready():
                break
            if not self.shell.recv_ready():
                time.sleep(.5)

        return super().get_output(wait_time, detecting_firmware, return_as_list, buffer_size, timeout)

    def close_connection(self):
        '''
        Closes the connection with the remote device

        :return: str: Confirmation that connection is closed
        :rtype: str
        '''
        self.client.close()

        if self.shell is not None:
            if self.shell._closed is True:
                return 'Connection to {} is Closed'.format(self.hostname)
            else:
                return 'Connection to {} is NOT Closed'.format(self.hostname)

        return 'Connection to {} attempted to close, unknown if succeeded'.format(self.hostname)


class SerialEngine(BaseClass, serial.Serial):
    def __init__(self):
        BaseClass.__init__(self)
        serial.Serial.__init__(self)
        self.baud = 9600
        self.timeout = 1
        self.ser = None
        self.location = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_to_server(self, serial_interface, username=None, password=None):

        self.ser = serial.Serial(serial_interface, baudrate=self.baud, timeout=self.timeout)

        self.location = self._determine_location()

        if self.location == 'LOGIN':
            login_output = self._login_to_device(username, password)
            self._validate_login(login_output)

        else:
            self.get_initial_prompt()

    def _login_to_device(self, username, password):

        if username is None or password is None:
            raise CustomExceptions.UsernameOrPasswordNotSupplied(
                'You have not supplied a Username or Password to login to the '
                'device with')

        output = []
        self.send_command(username)
        time.sleep(1)
        for line in self.ser.readlines():
            output.append(line.decode().strip('\r\n'))

        self.send_command(password)
        time.sleep(1)

        while True:
            time.sleep(.2)
            for line in self.ser.readlines():
                output.append(line.decode().strip('\r\n'))

            for line in output:
                line = line.lower()
                if 'fail' in line or '>' in line or '#' in line:
                    if '>' in line or '#' in line:
                        self.prompt = line
                        self.hostname = line[:-1]
                    return output

    def _validate_login(self, output_from_login):

        for line in output_from_login:
            line = line.lower()

            if 'fail' in line:
                raise CustomExceptions.LoginFailed('Unable to Login to device with supplied username and password')

        return True

    def _determine_location(self):

        self.send_command('\r')
        time.sleep(1)

        output = ['']
        while True:

            for line in self.ser.readlines():
                output.append(line.decode().strip('\r'))

            if 'username' in output[-1].lower():
                return 'LOGIN'
            elif '#' in output[-1] or '>' in output[-1]:
                return 'SHELL'

            else:
                raise CustomExceptions.UnableToDetermineLocation(
                    'Serial Engine is unable to determine if the shell is requiring '
                    'login or already logged in ')

    def send_command_get_output(self, command, return_as_list=False, buffer_size=1, timeout=10):
        self.send_command(command)
        return self.get_output(return_as_list=return_as_list, buffer_size=buffer_size, timeout=timeout)

    def send_command_expect_different_prompt(self, command, timeout=10, return_as_list=False, buffer_size=10, pause=1):
        '''
        '''

        self.send_command(command)

        return self.get_output(
            return_as_list=return_as_list,
            buffer_size=buffer_size,
            timeout=timeout
        )

    def send_command_expect_same_prompt(self, command, timeout=10, detecting_firmware=False, return_as_list=False, buffer_size=10):
        '''
        Sends commands and gathers the output in a way that expects the same prompt to be returned
        DO NOT use this method if you are not SURE that the prompt returned will be the same

        :param command: Command to issue to device
        :param detecting_firmware: set to true if you want to throw away buffer data for detecting firmware
        :param return_as_list: returns the output as a list vs a string, string is default
        :return: Output from command in either string or list format
        '''

        self.send_command(command)

        return self.get_output(
            detecting_firmware=detecting_firmware,
            return_as_list=return_as_list,
            buffer_size=buffer_size,
            timeout=timeout
        )

    def get_initial_prompt(self, login_output=None):
        '''
        Gets the initial prompt and hostname of the device and sets the corresponding class variables

        :return: Nothing
        '''

        self.hostname = self.prompt[:-1]

        self.send_command(' ')

        time.sleep(1)

        output = self.get_output(return_as_list=True)

        #output = self.send_command_expect_different_prompt(command=' ', return_as_list=True, timeout=10)

    def send_command(self, command):
        '''
        Method to send a command out the serial interface to the server

        :param command: Command to send to the device
        :type command: str
        :return: Nothing
        '''

        self.ser.write('{}\r\n'.format(command).encode())

    def throw_away_buffer_data(self):
        '''
        Will capture any data waiting in the incoming buffer and discard it

        :return: int: total bytes discarded from the buffer
        :rtype: int
        '''

        total_bytes_discarded = 0

        time.sleep(.1)
        while True:
            bytes_discarded = 0
            for line in self.ser.readlines():
                fromDevice = line.decode().strip('\r\n')
                bytes_discarded += len(fromDevice)
                # output.append(fromDevice

            if bytes_discarded == 0:
                break
            else:
                total_bytes_discarded += bytes_discarded


        logger.debug('Discarded a total of {} bytes'.format(total_bytes_discarded))

        return total_bytes_discarded

    def get_output(self, timeout=10, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1):

        '''
        Gets output when the same prompt is expected to be returned

        :param wait_time: Time to wait before retrieving output from buffer
        :type wait_time: float
        :param return_as_list: When set to True will return output as list, when set to False will return output as string
        :type return_as_list: bool
        :param buffer_size: Not used but kept for compatibility
        :type buffer_size: int
        :return:
        '''

        # TODO: convert this method to have a timeout and use a thread

        logging.debug('Serial engine starting to get output from device')
        self._output = '\n\n'

        time.sleep(.1)
        count = 0
        while True:
            if self.ser.in_waiting > 0:
                self._output += self.ser.read(self.ser.in_waiting).decode()
            count += 1
            if '>' in self._output.splitlines()[-1] or '#' in self._output.splitlines()[-1] and self.ser.in_waiting == 0:
                break

        return super().get_output(wait_time, detecting_firmware, return_as_list, buffer_size, timeout)

    def get_output_different_prompt(self, timeout=10, wait_time=.2, return_as_list=False, buffer_size=1):

        return self.get_output(timeout=timeout, wait_time=wait_time, return_as_list=return_as_list, buffer_size=buffer_size)

    def close_connection(self):
        '''
        Closes Serial connection

        :return: Nothing
        '''

        if '(conf' in self.prompt:
            self.send_command('end')

        self.send_command('exit')
        self.ser.close()

