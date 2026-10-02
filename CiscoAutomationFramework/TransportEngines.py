from CiscoAutomationFramework.Exceptions import (
    AuthenticationException,
    ForbiddenError,
    JumpHostAuthenticationException,
    DeviceAuthenticationException,
    JumpHostConnectionException,
    JumpHostTunnelException,
)
import paramiko
from paramiko import SSHClient, AutoAddPolicy
import socket
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from time import sleep

default_command_end = '\n'
default_buffer = 1024
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

    def send_command_get_truncated_output(self, command):

        '''
        Method to be used in an instance when setting the terminal length to 0 is not an option and the
        output from the device will be truncated where you need to press the space bar to get it all. An example
        is AP's I have ran into, when the show version is gathered upon login, the terminal length command is
        not available yet until going into enable mode.

        This method is blocking, so it has the potential to hang if for whatever reason the previously
        known prompt is not returned.
        '''

        self.send_command(command)
        output = []
        while True:
            for line in self.get_output(timeout=.1):
                output.append(line)

            if self.prompt in '\n'.join(output):
                break
            else:
                self.send_command(' ', end='')
        return output

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
            if '% Authorization failed.' in output:
                raise DeviceAuthenticationException(
                    "% Authorization failed on network device.",
                    ip=getattr(self, 'hostname', None) or ''
                )
        prompt = self._prompt_lookup(output)

        # prompt = data.splitlines()[-1].strip()
        hostname = prompt[:-1]
        return prompt, hostname

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
    def connect_to_server(self, ip, username, password, port, jumphost=None) -> bool:
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


class JumpHost:
    """
    Represents an SSH jump host (bastion server) used to transparently tunnel
    SSH connections to remote network devices via a direct-tcpip channel.

    Supports password authentication, SSH private keys (file path or PKey object),
    passphrases, and custom SSH ports/timeouts.
    """

    def __init__(self, ip, username, password=None, port=22,
                 key_filename=None, pkey=None, passphrase=None,
                 timeout=10, look_for_keys=None, allow_agent=None, **kwargs):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.key_filename = key_filename
        self.pkey = pkey
        self.passphrase = passphrase
        self.timeout = timeout

        if look_for_keys is None:
            self.look_for_keys = False if (password and not (key_filename or pkey)) else True
        else:
            self.look_for_keys = look_for_keys

        if allow_agent is None:
            self.allow_agent = False if (password and not (key_filename or pkey)) else True
        else:
            self.allow_agent = allow_agent

        self.kwargs = kwargs

    def __repr__(self):
        return f"JumpHost({self.username}@{self.ip}:{self.port})"

    def connect(self) -> SSHClient:
        """
        Establishes an SSH connection to the jump host and returns an active SSHClient.

        :return: Connected Paramiko SSHClient
        :rtype: paramiko.SSHClient
        :raises CiscoAutomationFramework.Exceptions.JumpHostAuthenticationException:
            If credentials (password or SSH key) are rejected by the jump host.
        :raises CiscoAutomationFramework.Exceptions.JumpHostConnectionException:
            If connecting to the jump host fails (e.g. timeout, connection refused, or network unreachable).
        """
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        connect_kwargs = {
            'hostname': self.ip,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'key_filename': self.key_filename,
            'pkey': self.pkey,
            'passphrase': self.passphrase,
            'timeout': self.timeout,
            'look_for_keys': self.look_for_keys,
            'allow_agent': self.allow_agent,
        }
        connect_kwargs.update(self.kwargs)
        try:
            client.connect(**connect_kwargs)
            return client
        except paramiko.AuthenticationException as err:
            raise JumpHostAuthenticationException(
                f"Authentication failed on jump host '{self.username}@{self.ip}:{self.port}'.",
                jumphost=self
            ) from err
        except (socket.error, paramiko.SSHException, TimeoutError) as err:
            raise JumpHostConnectionException(
                f"Failed to connect to jump host '{self.ip}:{self.port}': {err}",
                jumphost=self
            ) from err

    def open_channel(self, client, dest_ip, dest_port=22):
        """
        Opens a direct-tcpip forwarding channel through the jump host to the destination.

        :param client: Connected SSHClient for the jump host
        :type client: paramiko.SSHClient
        :param dest_ip: Target destination IP address or hostname
        :type dest_ip: str
        :param dest_port: Target destination TCP port (default 22)
        :type dest_port: int
        :return: Forwarding channel
        :rtype: paramiko.Channel
        :raises CiscoAutomationFramework.Exceptions.JumpHostConnectionException:
            If the jump host transport is missing or inactive.
        :raises CiscoAutomationFramework.Exceptions.JumpHostTunnelException:
            If opening the direct-tcpip channel fails.
        """
        transport = client.get_transport()
        if transport is None or not transport.is_active():
            raise JumpHostConnectionException(
                f"No active transport on jump host '{self.ip}:{self.port}'.",
                jumphost=self
            )
        try:
            channel = transport.open_channel(
                kind='direct-tcpip',
                dest_addr=(dest_ip, dest_port),
                src_addr=('127.0.0.1', 0),
                timeout=self.timeout
            )
        except paramiko.SSHException as err:
            raise JumpHostTunnelException(
                f"Failed to open forwarding channel through jump host '{self.ip}' to '{dest_ip}:{dest_port}': {err}",
                jumphost=self,
                dest_ip=dest_ip,
                dest_port=dest_port
            ) from err

        if channel is None:
            raise JumpHostTunnelException(
                f"Failed to open direct-tcpip channel through jump host '{self.ip}' to '{dest_ip}:{dest_port}'. "
                f"Check network reachability and sshd 'AllowTcpForwarding' on the jump host.",
                jumphost=self,
                dest_ip=dest_ip,
                dest_port=dest_port
            )
        return channel


class SSHEngine(BaseEngine):

    def __init__(self):
        super().__init__()
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.shell = None
        self.timeout = 10
        self._pre_jumphost_hostname = ''
        self.jump_client = None
        self.jump_channel = None
        self.tunnel_jumphost = None

    @property
    def _in_jumphost(self):
        return self._pre_jumphost_hostname != self.hostname

    def connect_to_server(self, ip, username, password, port=22, jumphost=None):
        """
        Establishes SSH connection to the remote server, optionally tunneled via a JumpHost.

        :param ip: Target device IP or hostname
        :type ip: str
        :param username: Target device username
        :type username: str
        :param password: Target device password
        :type password: str
        :param port: Target device port (default 22)
        :type port: int
        :param jumphost: Optional JumpHost or dict for bastion tunneling
        :type jumphost: JumpHost or dict
        :raises CiscoAutomationFramework.Exceptions.JumpHostAuthenticationException:
            If authentication to the jump host fails.
        :raises CiscoAutomationFramework.Exceptions.JumpHostConnectionException:
            If connecting to the jump host fails.
        :raises CiscoAutomationFramework.Exceptions.JumpHostTunnelException:
            If opening the forwarding channel through the jump host fails.
        :raises CiscoAutomationFramework.Exceptions.DeviceAuthenticationException:
            If authentication to the destination device fails.
        """
        sock = None
        if jumphost is not None:
            if isinstance(jumphost, dict):
                jumphost = JumpHost(**jumphost)
            elif not isinstance(jumphost, JumpHost):
                raise TypeError(f'jumphost must be an instance of JumpHost or dict, got {type(jumphost)}')

            self.tunnel_jumphost = jumphost
            try:
                self.jump_client = jumphost.connect()
                self.jump_channel = jumphost.open_channel(self.jump_client, ip, port)
                sock = self.jump_channel
            except Exception:
                self._cleanup_jumphost()
                raise

        try:
            self.client.connect(hostname=ip, port=port, username=username, password=password, timeout=self.timeout, sock=sock)
            self.shell = self.client.invoke_shell()
            self.prompt, self.hostname = self._get_prompt_and_hostname()
            self._pre_jumphost_hostname = self.hostname
        except paramiko.AuthenticationException as err:
            self.close_connection()
            raise DeviceAuthenticationException(
                f"Authentication failed on network device '{ip}' for user '{username}'.",
                ip=ip,
                username=username
            ) from err
        except Exception:
            self.close_connection()
            raise

    def jumphost(self, ip, password, username=None, port=None, ssh_ver=None, vrf=None):
        command_string = 'ssh '
        if username:
            command_string += f'-l {username} '
        if port:
            command_string += f'-p {port} '
        if ssh_ver:
            command_string += f'-v {ssh_ver} '
        if vrf:
            command_string += f'-vrf {vrf} '
        command_string += ip

        self.send_command(command_string)
        sleep(.3)
        _ = self._get_output(100)
        self.send_command(password)
        self.prompt, self.hostname = self._get_prompt_and_hostname()

    def exit_jumphost(self):
        if self._in_jumphost:
            self.send_command('exit')
            self.prompt, self.hostname = self._get_prompt_and_hostname()

    def _get_output(self, buffer_size):
        if self.shell and self.shell.recv_ready():
            return bytes.decode(self.shell.recv(buffer_size))
        return ''

    def _send_command(self, command, end='\n'):
        if self.shell:
            self.shell.send(f'{command}{end}')

    def _cleanup_jumphost(self):
        if self.jump_channel:
            try:
                self.jump_channel.close()
            except Exception:
                pass
            self.jump_channel = None
        if self.jump_client:
            try:
                self.jump_client.close()
            except Exception:
                pass
            self.jump_client = None

    def close_connection(self):
        self.exit_jumphost()
        if self.shell:
            try:
                self.shell.close()
            except Exception:
                pass
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self._cleanup_jumphost()


class ReadOnlySSHEngine(SSHEngine):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__forbidden_commands = ['configure terminal', 'write erase', 'reload']

    @property
    def forbidden_commands(self):
        return self.__forbidden_commands

    def is_forbidden_command(self, command):

        # Split input into words
        command_parts = command.strip().lower().split()

        for forbidden_command in self.forbidden_commands:
            split_forbidden_command = forbidden_command.split()
            if len(command_parts) == len(split_forbidden_command):
                if all([True if forbidden_word.startswith(command_word) else False for command_word, forbidden_word in zip(command_parts, split_forbidden_command)]):
                    return True

        return False

    def _send_command(self, command, end='\n'):
        if self.is_forbidden_command(command):
            raise ForbiddenError(f'You are not allowed to issue "{command}" using this engine!')
        super()._send_command(command, end)

    # Methods required for some lower level SSH handling. These methods should not be called outside of this class

    # End low level methods