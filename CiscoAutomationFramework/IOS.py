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
from CiscoAutomationFramework.FirmwareType import CiscoFirmware
from CiscoAutomationFramework.CustomExceptions import ParserError


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
        raw_data = self.transport.send_command_get_output('show interfaces', buffer_size=50, return_as_list=True)
        try:
            parsed_data = [x.split()[0] for x in raw_data[2:-2] if not x.startswith(' ')]
        except IndexError as _:
            raise ParserError('Unexpected data from device, Unable to extract interface names from "show interfaces" command!')
        return parsed_data

    @property
    def mac_address_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_mac = self.transport.send_command_get_output('show mac address-table', buffer_size=50, return_as_list=True)
        return '\n'.join(raw_mac[6:-2])

    @property
    def arp_table(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        raw_arp = self.transport.send_command_get_output('show ip arp', buffer_size=50, return_as_list=True)
        return '\n'.join(raw_arp[2:-2])

    @property
    def running_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        running_config = self.transport.send_command_get_output('show running-config', buffer_size=50, timeout=15, return_as_list=True)
        return '\n'.join(running_config[2:-2])

    @property
    def startup_config(self):
        self.cli_to_privileged_exec_mode()
        self.terminal_length('0')
        running_config = self.transport.send_command_get_output('show startup-config', buffer_size=50, timeout=15, return_as_list=True)
        return '\n'.join(running_config[2:-2])

    def terminal_length(self, n='0'):
        self.cli_to_privileged_exec_mode()
        if self.transport.terminal_length_value == str(n):
            return

        self.transport.terminal_length_value = str(n)
        return self.transport.send_command_get_output(f'terminal length {n}')

    def terminal_width(self, n='0'):
        self.cli_to_privileged_exec_mode()
        if self.transport.terminal_width_value == str(n):
            return 'Terminal width already set to proper value'

        self.transport.terminal_width_value = str(n)

        return self.transport.send_command_get_output(f'terminal width {n}')

    def save_config(self):
        self.cli_to_privileged_exec_mode()
        return self.transport.send_command_get_output('copy running-config startup-config')