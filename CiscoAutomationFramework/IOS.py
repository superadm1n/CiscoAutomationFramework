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
from CiscoAutomationFramework.FirmwareBase import CiscoFirmware
from time import sleep


class IOS(CiscoFirmware):

    @property
    def uptime(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        device_output = self.transport.send_command_get_output('show version')
        for line in device_output.splitlines():
            if f'{self.transport.hostname.lower()} uptime' in line.lower():
                return ' '.join(line.split()[3:])

        return None

    @property
    def interfaces(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_data = self.transport.send_command_get_output('show interfaces', buffer_size=500)
        try:
            parsed_data = [x.split()[0] for x in raw_data[2:-2] if not x.startswith(' ')]
        except IndexError as _:
            raise IndexError('Unexpected data from device, Unable to extract interface names from "show interfaces" command!')
        return parsed_data

    @property
    def mac_address_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_mac = self.transport.send_command_get_output('show mac address-table')
        return '\n'.join(raw_mac[6:-2])

    @property
    def arp_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_arp = self.transport.send_command_get_output('show ip arp')
        return '\n'.join(raw_arp[2:-1])

    @property
    def running_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')

        running_config = self.transport.send_command_get_output('show running-config', buffer_size=100)
        # if the running config grabbed is less than 4 lines and the prompt is not in the last 4 lines of the config
        while len(running_config) < 4 and not any([True if self.prompt in x else False for x in reversed(running_config[-4:])]):
            running_config += self.transport.get_output(buffer_size=100, no_command_sent_previous=True)
            sleep(.1)
        return '\n'.join(running_config[2:-2])

    @property
    def startup_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        config = self.transport.send_command_get_output('show startup-config', buffer_size=100)
        while len(config) < 4 and not any([True if self.prompt in x else False for x in reversed(config[-4:])]):
            config += self.transport.get_output(buffer_size=100, no_command_sent_previous=True)
            sleep(.1)
        return '\n'.join(config[2:-2])

    def _terminal_length(self, n='0'):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output(f'terminal length {n}')

    def _terminal_width(self, n='0'):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output(f'terminal width {n}')

    def save_config(self):
        self.cli_to_privileged_exec_mode()
        self.transport.send_command('copy running-config startup-config')
        data = self.transport.send_command_get_output('', timeout=15)
        # if the prompt is in the last line of output and there is not a percent sign in any line of output we will
        # interpret that as a succesful save
        if self.transport.prompt in ''.join(data[-1:]) and not any('%' in line for line in data):
            return True
        return False

    def add_local_user(self, username, password, password_code=0, *args, **kwargs):
        kwarg_string = ' '.join([f'{key} {value}' for key, value in kwargs.items()])
        command_string = f'username {username} {" ".join(args)} {kwarg_string} secret {password_code} {password}'
        self.cli_to_config_mode()
        return self.transport.send_command_get_output(command_string)

    def delete_local_user(self, username):
        self.cli_to_config_mode()
        self.transport.send_command(f'no username {username}')
        return self.transport.send_command_get_output('')