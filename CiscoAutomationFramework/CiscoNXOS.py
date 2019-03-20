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
'''

import time
from . import CustomExceptions
from .BaseCommandMethods import CommandGetMethods, CommandConfigMethods

not_implemented_text = 'This method has not been implemented in the CiscoNXOS module'

class TerminalCommands:

    def __init__(self, transport_object):
        self.transport = transport_object

    def terminal_length(self, number='0'):
        '''
        Sets Terminal length to infinite by default or to user specification
        Note: Does not require a specific admin role on device
        :return: Output from command
        '''

        # checks if terminal length that the user is requesting is already set and if it has been it breaks out of the function.
        if self.transport.terminal_length_value == str(number):
            return 'Terminal length already set to proper value'

        self.transport.terminal_length_value = str(number)

        return self.transport.send_command_expect_same_prompt('terminal length {}'.format(number))

    def terminal_width(self, number=511):
        '''
        Sets Terminal length to infinite by default or to user specification
        Note: Does not require a specific admin role on device
        :return: Output from command
        '''

        # makes sure the number specified is within the minimum and maximum parameters accepted by NXOS
        if int(number) > 511:
            number = 511

        if int(number) < 24:
            number = 24

        # checks if terminal length that the user is requesting is already set and if it has been it breaks out of the function.
        if self.transport.terminal_width_value == str(number):
            return 'Terminal length already set to proper value'

        self.transport.terminal_width_value = str(number)

        return self.transport.send_command_expect_same_prompt('terminal width {}'.format(number))

    def priv_exec(self):
        raise CustomExceptions.MethodNotSupported


class NXOS(TerminalCommands, CommandGetMethods):

    def __init__(self, transport_object):
        TerminalCommands.__init__(self, transport_object)
        self.config = NXOSConfigMethods(transport_object)
        self.transport = transport_object
        self.terminal_width(200)
        self.roles = self.get_user_roles()

    def check_admin_role(self):

        if 'vdc-admin' in self.roles.lower():
            return True
        else:
            return False

    def get_current_user(self):
        '''
        :return: Username of current user logged in
        '''
        output = self.transport.send_command_expect_same_prompt('show users')

        for line in output.splitlines():
            if '*' in line:
                return line.split()[0]

        return 'Unable to Determine Current User'

    def get_user_roles(self):
        roles = ''
        user = self.get_current_user()

        self.terminal_length()

        output = self.transport.send_command_expect_same_prompt('show user-account')

        flag = 0
        for line in output.splitlines():

            if 'user:{}'.format(user) in line:
                flag = 1

            if flag == 1:
                if 'roles' in line:
                    line = line.split(':')
                    for entry in line[1:]:
                        roles += '{} '.format(str(entry).strip())

                    return roles

        print('something failed')

    def get_uptime(self):
        '''
        This command does not require a specific privlege or admin role
        :return: uptime of device
        '''
        output = ''

        self.terminal_length()

        device_output = self.transport.send_command_expect_same_prompt('show version')

        for line in device_output.splitlines():

            if 'kernel uptime' in line.lower():
                output += '{} {}'.format(self.transport.hostname, line)
                break

        return output

    def show_run(self):
        if self.check_admin_role() is False:
            return 'VDC-Admin role required'

        self.terminal_length()

        device_output = self.transport.send_command_expect_same_prompt('show running-config').splitlines()

        output = ''
        for line in device_output[3:][:-2]:
            output += '{}\n'.format(line)

        return output

    def show_run_interface(self, interface):
        return super().show_run_interface(interface)

    def get_local_users(self):
        users = []

        output = self.show_run()

        for line in output.splitlines():
            if 'username' in line:
                users.append(line.split()[1])

        return users

    def power_cycle_port(self, interface, delay):

        return super().power_cycle_port(interface, delay)

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):

        return super().configure_router_lan_subinterface(
            physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses
        )

    def physical_port_inventory(self):

        data = []

        interfaces = self.physical_port_inventory_longname()
        for x in interfaces:
            beginning = x[:3]
            end = ''.join([y for y in x if not y.isalpha()])
            data.append('{}{}'.format(beginning, end))

        return data

    def physical_port_inventory_longname(self):
        self.terminal_length()

        interfaces = []

        for line in self.transport.send_command_expect_same_prompt('show interface', buffer_size=200, return_as_list=True)[1:][:-1]:
            if len(line) < 1:
                continue

            if line[0].isalpha() and line.split()[0] != 'admin':
                if 'port-channel' in line or 'Vlan' in line or 'loop' in line or 'mgmt' in line:
                    continue
                #print(line)
                interfaces.append(line.split()[0])
        return interfaces

    def port_status(self):
        return super().port_status()

    def power_inline(self, summary):
        return super().power_inline(summary)

    def list_ospf_configuration(self):

        ospf_config = ''
        running_config = self.show_run()
        flag = 0

        for line in running_config.splitlines():
            line = str(line)

            # after the entry statement for OSPF has been found this if statement will gather te rest of the OSPF configuration then
            # resets the flag so this if statement will not run again unless triggered below (which should not happen)
            if flag == 1:
                if len(line) >= 1:
                    if line[0] == ' ':
                        ospf_config += '{}\n'.format(line)
                    else:
                        flag = 0

            # Finds the entry statement for the ospf configuration and triggers the flag for the previous if statement to start
            if len(line.split()) >= 2:
                if 'router ospf' in '{[0]} {[1]}'.format(line.split(), line.split()):
                    flag = 1
                    ospf_config += '{}\n'.format(line)

        # returns if there was no OSPF process found in the running config
        if len(ospf_config) == 0:
            return 'No OSPF process configured'

        return ospf_config

    def list_eigrp_configuration(self):
        output = ''
        running_config = self.show_run()
        flag = False
        for line in running_config.splitlines():
            if len(line.split()) < 1:
                continue

            if 'router' in line.split()[0].lower() and 'eigrp' in line.split()[1].lower():
                flag = True
                output += '{}\n'.format(line)
                continue

            if flag is True:

                if not line[0].isalpha():
                    output += '{}\n'.format(line)
                else:
                    flag = False

        if len(output) == 0:
            output = 'No EIGRP process configured'

        return output

    def list_down_ports(self):
        self.terminal_length()

        output = []

        for line in self.transport.send_command_expect_same_prompt('show interface status', return_as_list=True, buffer_size=100):
            if len(line.split()) < 1:
                continue
            if 'Vlan' in line.split()[0]:
                continue
            if 'Po' in line.split()[0]:
                continue
            if 'Lo' in line.split()[0]:
                continue

            if 'down' in line or 'disabled' in line:
                output.append(line.split()[0])

        return output

    def list_configured_vlans(self):


        self.terminal_length()

        output = []
        startflag = False
        for line in self.transport.send_command_expect_same_prompt('show vlan brief', return_as_list=True):


            # captures the line of output only after there has been a line of dashes
            if startflag is True:
                output.append(line)

            # if there is a line of dashes we will begin capturing the output after the line of dashes
            if '----' in line:
                startflag = True

        # splits each line of output and only takes the first element (vlan number)
        output = [x.split()[0] for x in output if len(x.split()) >= 1 if x.split()[0].isdigit()]

        # returns output
        return output


    def last_input_and_output(self, interface):
        return super().last_input_and_output(interface)

    def last_input_and_output_all(self):

        return super().global_last_input_and_output()

    def find_mac_address(self, mac_address, mac_table):
        if not mac_table:
            mac_table = self.mac_address_table()

        return [item for item in mac_table if item['mac'] == mac_address]


    def mac_address_table(self):

        self.terminal_length()
        data = self.transport.send_command_expect_different_prompt('show mac address-table', return_as_list=True, buffer_size=200)[:-1]

        clean_data = []
        capture_flag = False
        for line in data:
            if len(line.split()) == 0:
                continue
            if '----' in line:
                capture_flag = True
                continue
            if capture_flag is True:
                tmp = line.split()
                clean_data.append({'vlan': tmp[1], 'mac': tmp[2], 'type': tmp[3], 'ports': tmp[-1]})

        return clean_data

    def cdp_neighbor_table(self):
        self.terminal_length()
        cdp_output = self.transport.send_command_expect_same_prompt('show cdp neighbors detail', return_as_list=True, buffer_size=200)
        data = []
        tmp = {}
        for line in cdp_output[2:]:
            if 'device id' in line.lower():
                tmp['deviceid'] = line.split(':')[1].strip()
            if 'interface' in line.lower() and 'outgoing' in line.lower():
                tmp['localinterface'] = line.split(',')[0].split(':')[1].strip()
                tmp['remoteinterface'] = line.split(',')[1].split(':')[1].strip()

            if 'platform' in line.lower():
                tmp['platform'] = line.split(',')[0].split(':')[1].strip()

            if 'ipv4 address' in line.lower():
                try:
                    tmp['remoteip']
                except KeyError:
                    tmp['remoteip'] = line.split(':')[1].strip()

            if '-----' in line:
                data.append(tmp)
                tmp = {}

        return data

    def arp_table(self):
        # [{'protocol': str, 'address': str, 'age': str, 'mac': str, 'type': str, 'interface': str}]
        self.terminal_length()

        data = []

        flag = False
        output = self.transport.send_command_expect_same_prompt('show ip arp', buffer_size=200, return_as_list=True)
        for line in output[:-1]:
            if 'mac address' in line.lower():
                flag = True
                continue

            if flag is True:
                x = line.split()
                try:
                    data.append({'protocol': None, 'address': x[0], 'age': x[1], 'mac': x[2], 'type': False, 'interface': x[3]})
                except IndexError:
                    pass

        return data

    def show_interface_status(self):
        return super().show_interface_status()

    def show_interface_description(self):
        return super().show_interface_description()

    def show_routes(self):
        return super().show_routes()


    def show_configured_syslog_server(self):
        '''Returns the value configured for syslog

        :return:
        '''
        runningConfig = self.show_run()

        servers = []
        for line in runningConfig.splitlines():
            if len(line.split()) > 0:
                if line.split()[0] == 'logging' and line.split()[1] == 'server':
                    servers.append(line.split()[2:][0])

        if len(servers) == 0:
            return [None]
        else:
            return servers


    def write_mem(self):

        if self.check_admin_role() is False:
            return 'VDC-Admin role required'
        # sends the command to copy run start and grabs the output from that command
        output = self.transport.send_command_expect_same_prompt('copy running-config startup-config')

        # Parses the output and checks for the line that will say 'copy complete' if the copy was successful
        # and returns a friendly success message to the user
        if 'copy complete' in output.lower():
            return 'Running config save successful!'

        # if the copy was not successful it returns the raw output from the server
        return output

class NXOSConfigMethods(CommandConfigMethods, TerminalCommands):

    def __init__(self, transport_object):
        TerminalCommands.__init__(self, transport_object)

    def delete_local_user(self, username):

        return super().delete_local_user(username)

    def configure_description(self, interface, description):

        return super().configure_description(interface, description)

    def configure_access_vlan(self, interface, vlan):

        return super().configure_access_vlan(interface, vlan)