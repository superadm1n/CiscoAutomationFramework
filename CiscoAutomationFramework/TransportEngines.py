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
from . import CustomExceptions


class BaseClass:
    def __init__(self):
        self.prompt = ''
        self.hostname = ''
        self.shell = None
        self.total_discarded_buffer_bytes = 0


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

    def send_command_expect_different_prompt(self, command, return_as_list=False, buffer_size=1):
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

        return self.get_output_different_prompt(
            return_as_list=return_as_list,
            buffer_size=buffer_size
        )

    def send_command_expect_same_prompt(self, command, detecting_firmware=False, return_as_list=False, buffer_size=1):
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
            buffer_size=buffer_size
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
            self.invoke_shell()
            return 'Connection Successful'

    def invoke_shell(self):
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
        return self.get_initial_prompt()

    def get_initial_prompt(self):
        '''
        Gathers the initial prompt from the remote device

        :return: Output from device
        '''

        output = self.get_output_different_prompt(.5)

        # At times the server will return the data in the 1st line, and others the second line, this try except block handles that
        try:
            # Sends return key and grabs the prompt that is returned, subtracting 1 character to give the hostname
            self.send_command('')
            output = self.get_output_different_prompt(return_as_list=True)
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

    def throw_away_buffer_data(self):
        '''
        Will capture any data waiting in the incoming buffer and discard it

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

    def get_output_different_prompt(self, wait_time=.2, return_as_list=False, buffer_size=1):
        '''
        This method will use a pre determined time to capture output, if the server doesnt begin to return output
        within that predetermined amount of time it will be missed, also if the server hangs for more than 1 second
        while returning the output, the rest will be missed. This method should only be used when issuing a command
        to the server that will return a different prompt, if it will return the same prompt use the 'get_output'
        method.

        :param wait_time: The time to wait before gathering buffer data (used to give the device time to fill the buffer
        :type wait_time: float
        :param return_as_list: default set to False will return as a string, set to True it will output as a list \
        split by lines
        :type return_as_list: bool
        :param buffer_size: Number of bytes to gather at a time when retrieving data from buffer
        :type buffer_size: int

        :return: Output from server in string or list format

        '''

        time.sleep(wait_time)

        output = '\n\n'

        # This will loop until a > or # is in the output
        while True:

            if self.shell.recv_ready():
                output += bytes.decode(self.shell.recv(buffer_size))

            if '>' in output.splitlines()[-1] or '#' in output.splitlines()[-1]:
                break

        output = output.splitlines()[2:]

        self.prompt = output[-1]

        if return_as_list is False:
            # formats output as a string for return to user
            cleanoutput = ''

            for line in output:
                cleanoutput += '{}\n'.format(line)

            return cleanoutput

        return output

    def get_output(self, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1):

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
        output = '\n\n'

        while output.splitlines()[-1] != self.prompt:
            output += bytes.decode(self.shell.recv(buffer_size))
            if not self.shell.recv_ready():
                time.sleep(.5)

        output = output.splitlines()[2:]

        if detecting_firmware is True:
            # This is needed because of the way CAF detects firmware, it will leave extra lines of the prompt in the buffer
            # and methods grabbing data downstream will cause issues on other commands. This will take those lines from the buffer
            # and throw them away this  will only run if this method is run with the 'detecting_firmware' flag set to 'True'
            # to prevent necessary data from being thrown away.
            self.total_discarded_buffer_bytes += self.throw_away_buffer_data()

        self.prompt = output[-1]

        if return_as_list is False:
            # Formats the output as a string and returns it
            cleanoutput = ''

            for line in output:
                cleanoutput += '{}\n'.format(line)

            return cleanoutput

        return output

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

    def send_command_expect_different_prompt(self, command, return_as_list=False, buffer_size=1):
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

        return self.get_output_different_prompt(
            return_as_list=return_as_list,
            buffer_size=buffer_size
        )

    def send_command_expect_same_prompt(self, command, detecting_firmware=False, return_as_list=False, buffer_size=1):
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
            buffer_size=buffer_size
        )

    def get_initial_prompt(self):
        '''
        Gets the initial prompt and hostname of the device and sets the corresponding class variables

        :return: Nothing
        '''

        self.send_command_expect_different_prompt(command=' ', return_as_list=True)[-1].strip()

        self.hostname = self.prompt[:-1]

    def send_command(self, command):
        '''
        Method to send a command out the serial interface to the server

        :param command: Command to send to the device
        :type command: str
        :return: Nothing
        '''

        self.ser.write('{}\n'.format(command).encode())

    def get_output(self, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1):

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

        time.sleep(wait_time)

        output = ['\n', '\n']

        while output[-1] != self.prompt:
            for line in self.ser.readlines():
                output.append(line.decode().strip('\r\n'))

            if self.ser.in_waiting == 0:
                time.sleep(.5)

        output = output[2:]  # removes first 2 entries in list

        if detecting_firmware is True:
            # :TODO: Add logic here
            pass

        self.prompt = output[-1].strip()

        if return_as_list is False:
            return '\n'.join(output)
        else:
            return output

    def get_output_different_prompt(self, wait_time=.2, return_as_list=False, buffer_size=1):

        '''
        Gets outut when a different prompt is expected to be returned

        :param wait_time: Time to wait before retrieving output from buffer
        :type wait_time: float
        :param return_as_list: When set to True will return output as list, when set to False will return output as string
        :type return_as_list: bool
        :param buffer_size: Not used but kept for compatibility
        :type buffer_size: int
        :return:
        '''

        time.sleep(wait_time)

        output = ['\n', '\n']

        while True:
            time.sleep(1)

            if self.ser.in_waiting:
                for line in self.ser.readlines():
                    output.append(line.decode().strip('\r\n'))

            if '>' in output[-1] or '#' in output[-1]:
                break

        self.prompt = output[-1].strip()

        if return_as_list is False:
            return '\n'.join(output)
        else:
            return output

    def close_connection(self):
        '''
        Closes Serial connection

        :return: Nothing
        '''

        if '(conf' in self.prompt:
            self.send_command('end')

        self.send_command('exit')
        self.ser.close()


class TransportInterface(SSHEngine, SerialEngine):
    '''
    This class is a polymorphic interface that allows CAF and firmware specific code downstream to
    seamlessly interface with the ssh and serial engines. It is responsible for handling calls from CAF
    and sending them to either the SSH or Serial engine depending on what the user has specified
    '''

    def __init__(self, engine):
        '''
        Initializes a TransportInterface object and gets it ready to interface calls

        :param engine: serial or ssh depending on which engine the user wants to use
        :type engine: str
        '''
        self.engine = engine

        # calls factor function to initiate a transport object that will hold the calls for the corresponding engine
        transport = self.transport_factory()
        transport.__init__(self)  # initializes the transport object

        self.transport = transport  # makes transport object an instance variable

    def transport_factory(self):

        '''
        Factory function that will return an object that points to the proper engine the user has specified to use

        :return: Engine object
        :raises EngineNotSelected: Error raised if the user did not pass the proper string for which engine they \
        wished to use
        '''

        if self.engine == 'serial':
            return SerialEngine
        elif self.engine == 'ssh':
            return SSHEngine
        else:
            raise CustomExceptions.EngineNotSelected('Valid Transport Engine not Specified!')

    def __enter__(self):

        return self.transport.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):

        return self.transport.__exit__(self, exc_type, exc_val, exc_tb)

    def send_command_expect_different_prompt(self, command, return_as_list=False, buffer_size=1):

        return self.transport.send_command_expect_different_prompt(self, command=command, return_as_list=return_as_list,
                                                                   buffer_size=buffer_size)

    def send_command_expect_same_prompt(self, command, detecting_firmware=False, return_as_list=False, buffer_size=1):
        return self.transport.send_command_expect_same_prompt(self, command=command,
                                                              detecting_firmware=detecting_firmware,
                                                              return_as_list=return_as_list, buffer_size=buffer_size)

    def connect_to_server(self, ip, username, password):
        return self.transport.connect_to_server(self, ip, username, password)

    def invoke_shell(self):
        return self.transport.invoke_shell(self)

    def get_initial_prompt(self):
        return self.transport.get_initial_prompt(self)

    def send_command(self, command):
        return self.transport.send_command(self, command=command)

    def throw_away_buffer_data(self):
        return self.transport.throw_away_buffer_data(self)

    def get_output_different_prompt(self, wait_time=.2, return_as_list=False, buffer_size=1):
        return self.transport.get_output_different_prompt(self, wait_time=wait_time, return_as_list=return_as_list,
                                                          buffer_size=buffer_size)

    def get_output(self, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1):
        return self.transport.get_output(self, wait_time=wait_time, detecting_firmware=detecting_firmware,
                                         return_as_list=return_as_list, buffer_size=buffer_size)

    def close_connection(self):
        return self.transport.close_connection(self)

    '''

    def determine_location(self):

        return self.determine_location()
    '''