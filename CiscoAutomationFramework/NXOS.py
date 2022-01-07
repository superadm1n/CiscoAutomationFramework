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


class NXOS(CiscoFirmware):

    @property
    def uptime(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        device_output = self.transport.send_command_get_output('show version')
        for line in device_output.splitlines():
            if 'uptime' in line.lower():
                return ' '.join(line.split()[3:])

        return None

    @property
    def interfaces(self):
        possible_interface_prefixes = ('Eth', 'Po', 'Vl', 'mgm ', 'Gi', 'Te', 'Fo', 'Fa')
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_data = self.transport.send_command_get_output('show interface', buffer_size=50)
        try:
            parsed_data = [x.split()[0] for x in raw_data[2:-2] if len(x) > 1 and x.startswith(possible_interface_prefixes)]
        except IndexError as _:
            raise IndexError('Unexpected data from device, Unable to extract interface names from "show interfaces" command!')
        return parsed_data

    @property
    def mac_address_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_mac = self.transport.send_command_get_output('show mac address-table')
        return '\n'.join(raw_mac[8:-2])

    @property
    def arp_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_arp = self.transport.send_command_get_output('show ip arp')
        return '\n'.join(raw_arp[11:-2])

    @property
    def running_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        self.transport.send_command('show running-config')
        sleep(1.5)
        config = self.transport.get_output(buffer_size=100)
        return '\n'.join(config[2:-2])

    @property
    def startup_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        self.transport.send_command('show startup-config')
        sleep(1.5)
        config = self.transport.get_output(buffer_size=100)
        return '\n'.join(config[2:-2])

    def _terminal_length(self, n='0'):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output(f'terminal length {n}')

    def _terminal_width(self, n='0'):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output(f'terminal width {n}')

    def save_config(self):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output('copy running-config startup-config')

    def add_local_user(self, username, password, password_code=0, *args, **kwargs):
        if len(password) < 8:
            raise Exception('Password must be at least 8 characters!')
        kwarg_string = ' '.join([f'{key} {value}' for key, value in kwargs.items()])

        # if there is a space in the password, wrap it in quotes
        if ' ' in password:
            password = f'"{password}"'

        command_string = f'username {username} {" ".join(args)} {kwarg_string} password {password_code} {password}'
        self.cli_to_config_mode()
        return self.transport.send_command_get_output(command_string)

    def delete_local_user(self, username):
        self.cli_to_config_mode()
        self.transport.send_command(f'no username {username}')
        return self.transport.send_command_get_output('')