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
from CiscoAutomationFramework import TransportEngines
from abc import ABC, abstractmethod


class CiscoFirmware(ABC):

    def __init__(self, transport):
        if not isinstance(transport, TransportEngines.BaseClass):
            raise TypeError('transport object MUST be a sub class of CiscoAutomationFramework.TransportEngines.BaseClass')
        self.transport = transport
        self.terminal_length()

    def cli_to_config_mode(self):
        self.cli_to_privileged_exec_mode()
        self.transport.send_command_get_output('config t')

    def cli_to_privileged_exec_mode(self):  # TODO: Enable password typing will fail trying to get output. Fix!
        if self.transport.in_privileged_exec_mode:
            return None
        if self.transport.in_configuration_mode:
            self.transport.send_command_get_output('end')
            return self.transport.in_privileged_exec_mode

        if self.transport.in_user_exec_mode:
            enabling_output = self.transport.send_command_get_output('enable')
            if self.transport.prompt not in enabling_output:
                if not self.transport.enable_password:
                    raise Exception('No enable password provided, network device is asking for one!')
                self.transport.send_command_get_output(self.transport.enable_password)


    @property
    def prompt(self):
        return self.transport.prompt

    @property
    def hostname(self):
        return self.transport.hostname

    @property
    def last_issued_command(self):
        return self.transport.last_issued_command

    def send_command_get_output(self, command, *args, **kwargs):
        return self.transport.send_command_get_output(command, *args, **kwargs)

    def send_command(self, command):
        return self.transport.send_command(command)

    def get_output(self, *args, **kwargs):
        return self.transport.get_output(*args, **kwargs)

    def close_connection(self):
        return self.transport.close_connection()

    # Begin abstract properties

    @property
    @abstractmethod
    def uptime(self):
        pass

    @property
    @abstractmethod
    def interfaces(self):
        pass

    @property
    @abstractmethod
    def mac_address_table(self):
        pass

    @property
    @abstractmethod
    def arp_table(self):
        pass

    @property
    @abstractmethod
    def running_config(self):
        pass

    @property
    @abstractmethod
    def startup_config(self):
        pass

    # Begin abstract methods

    @abstractmethod
    def terminal_length(self, n='0'):
        pass

    @abstractmethod
    def terminal_width(self, n='0'):
        pass

    @abstractmethod
    def save_config(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close_connection()


