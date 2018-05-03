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

not_implemented_text = 'This method has not been implemented in the CiscoNXOS module'

class TerminalCommands:

    def __init__(self, ssh_object):
        self.ssh = ssh_object

    def terminal_length(self, number='0'):
        '''
        Sets Terminal length to infinite by default or to user specification
        Note: Does not require a specific admin role on device
        :return: Output from command
        '''

        # checks if terminal length that the user is requesting is already set and if it has been it breaks out of the function.
        if self.ssh.terminal_length_value == str(number):
            return 'Terminal length already set to proper value'

        self.ssh.terminal_length_value = str(number)

        return self.ssh.send_command_expect_same_prompt('terminal length {}'.format(number))

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
        if self.ssh.terminal_width_value == str(number):
            return 'Terminal length already set to proper value'

        self.ssh.terminal_width_value = str(number)

        return self.ssh.send_command_expect_same_prompt('terminal width {}'.format(number))

    def priv_exec(self):
        raise CustomExceptions.MethodNotSupported


class NXOS(TerminalCommands):

    def __init__(self, ssh_object):
        TerminalCommands.__init__(self, ssh_object)
        self.ssh = ssh_object
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
        output = self.ssh.send_command_expect_same_prompt('show users')

        for line in output.splitlines():
            if '*' in line:
                return line.split()[0]

        return 'Unable to Determine Current User'

    def get_user_roles(self):
        roles = ''
        user = self.get_current_user()

        self.terminal_length()

        output = self.ssh.send_command_expect_same_prompt('show user-account')

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

        device_output = self.ssh.send_command_expect_same_prompt('show version')

        for line in device_output.splitlines():

            if 'kernel uptime' in line.lower():
                output += '{} {}'.format(self.ssh.hostname, line)
                break

        return output

    def show_run(self):
        if self.check_admin_role() is False:
            return 'VDC-Admin role required'

        self.terminal_length()

        device_output = self.ssh.send_command_expect_same_prompt('show running-config').splitlines()

        output = ''
        for line in device_output[3:][:-2]:
            output += '{}\n'.format(line)

        return output

    def show_run_interface(self, interface):
        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def get_local_users(self):
        users = []

        output = self.show_run()

        for line in output.splitlines():
            if 'username' in line:
                users.append(line.split()[1])

        return users

    def delete_local_user(self, username):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def configure_description(self, interface, description):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def configure_access_vlan(self, interface, vlan):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def power_cycle_port(self, interface, delay):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def physical_port_inventory(self):
        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def physical_port_inventory_longname(self):
        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def port_status(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def power_inline(self, summary):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

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

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def list_down_ports(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def list_configured_vlans(self):


        self.terminal_length()

        output = []
        startflag = False
        for line in self.ssh.send_command_expect_same_prompt('show vlan brief', return_as_list=True):


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

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def global_last_input_and_output(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def find_mac_address(self, mac_address):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def mac_address_table(self, mac_address):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def cdp_neighbor_table(self, mac_address):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def arp_table(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def show_interface_status(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def show_interface_description(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def show_routes(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def write_mem(self):

        if self.check_admin_role() is False:
            return 'VDC-Admin role required'
        # sends the command to copy run start and grabs the output from that command
        output = self.ssh.send_command_expect_same_prompt('copy running-config startup-config')

        # Parses the output and checks for the line that will say 'copy complete' if the copy was successful
        # and returns a friendly success message to the user
        if 'copy complete' in output.lower():
            return 'Running config save successful!'

        # if the copy was not successful it returns the raw output from the server
        return output
