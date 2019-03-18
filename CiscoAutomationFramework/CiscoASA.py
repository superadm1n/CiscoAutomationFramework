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

===========================================================================

This Module contains the code that is specific to issuing commands to ASA's
'''


from .CiscoIOS import *
from . import CustomExceptions
from .BaseCommandMethods import CommandMethods
import time


not_implemented_text = 'This Method is not implemented in the CiscoASA Module'

class ASATerminalCommands(TerminalCommands):

    def __init__(self, transport_object):
        TerminalCommands.__init__(self, transport_object)
        self.transport = transport_object
        self.enable_password = self.transport.enable_password

    def terminal_length(self, number=0):
        self.check_and_exit_config_t()

        self.priv_exec()

        # checks if terminal length that the user is requesting is already set and if it has been it breaks out of the function.
        if self.transport.terminal_length_value == str(number):
            return 'Terminal length already set to proper value'

        self.transport.terminal_length_value = str(number)

        return self.transport.send_command_expect_same_prompt('terminal pager {}'.format(number))


class ASA(ASATerminalCommands, CommandMethods):

    def __init__(self, transport_object):
        ASATerminalCommands.__init__(self, transport_object)
        self.transport = transport_object
        self.ios = IOS(transport_object)

    def get_uptime(self):
        output = ''

        self.terminal_length()
        device_output = self.transport.send_command_expect_same_prompt('show version')

        for line in device_output.splitlines():

            if '{} up'.format(self.transport.hostname.lower()) in line.lower():
                output += line
                break

        return output

    def show_run(self):

        return self.ios.show_run()

    def show_run_interface(self, interface):

        return self.ios.show_run_interface(interface)

    def get_local_users(self):

        return self.ios.get_local_users()

    def delete_local_user(self, username):

        return self.ios.delete_local_user(username)

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
        return self.physical_port_inventory_longname()

    def physical_port_inventory_longname(self):

        port_list = []
        self.terminal_length()

        # issues 'show interfaces' command on device
        for line in self.transport.send_command_expect_same_prompt('show interface').splitlines()[1:][:-1]:
            # Only uses lines that begin with an f, g, t, or e for ten gig, gig, fast and eth interfaces and appends
            # the first column to a list
            if len(line) >= 1:

                if line[0].lower() == 'i':
                    line = line.split()[1]

                    if line[:2].lower() == 'vl' or line[:2].lower() == 'po':
                        pass
                    else:
                        port_list.append(line)

                    #if line[0].lower() == 'f' or line[0].lower() == 'g' or line[0].lower() == 't' or line[0].lower() == 'e':
                    #    port_list.append(line)

        return port_list

    def port_status(self):
        port_list = []
        self.terminal_length()

        output = ''

        # issues 'show interfaces' command on device
        for line in self.transport.send_command_expect_same_prompt('show interface').splitlines()[1:][:-1]:
            # Only uses lines that begin with an f, g, t, or e for ten gig, gig, fast and eth interfaces and appends
            # the first column to a list
            if len(line) >= 1:

                if line[0].lower() == 'i':
                    if 'up' in line.lower():
                        line += ' connected'
                    if 'down' in line.lower():
                        line += ' notconnected'

                    output += '{}\n'.format(line)
        return output

    def power_inline(self, summary):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def list_ospf_configuration(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def list_eigrp_configuration(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def list_down_ports(self):

        # This method gets placed into the proper CLI prompt by the self.port_status() method so no manual
        # handling is needed

        output = []

        for line in self.port_status().splitlines():

            if line.split()[1][:2].lower() == 'vl' or line.split()[1][:2].lower() == 'po':
                pass
            elif 'down' in line.lower():
                output.append(line.split()[1])

        return output

    def list_configured_vlans(self):

        self.terminal_length()  # sets the length of the terminal to infinite

        commandOutput = self.transport.send_command_expect_same_prompt('show switch vlan', return_as_list=True)[:-1]

        sanitizedOutput = []
        startflag = False
        for line in commandOutput:

            # captures the line of output only after there has been a line of dashes
            if startflag is True:
                sanitizedOutput.append(line)

            # if there is a line of dashes we will begin capturing the output after the line of dashes
            if '----' in line:
                startflag = True

        # takes the first column for each line of output only if it is greater than 1 character when split
        # and also is a digit and puts it into a list for return out of the method
        vlans = [x.split()[0] for x in sanitizedOutput if len(x.split()) >= 1 if x.split()[0].isdigit()]
        return vlans

    def last_input_and_output(self, interface):

        return [interface, 'stats unavailable on ASA', 'stats unavailable on ASA']

    def global_last_input_and_output(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def find_mac_address(self, mac_address):
        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def mac_address_table(self):

        mac_list = []

        self.terminal_length()

        device_output = self.transport.send_command_expect_same_prompt('show switch mac-address-table').splitlines()[1:][:-1]

        flag = 0
        for line in device_output:
            line = line.split('|')

            if flag == 1:
                if len(line) > 1:
                    mac_list.append([line[1].strip(), line[0].strip(), line[2].strip(), line[4].strip()])

            if '--' in line[0]:
                flag = 1

        return mac_list

    def cdp_neighbor_table(self):
        '''
        Command is not supported on ASA, Unable to generate pseudo command.

        :return: Soft Error message in the format the Programmer is expecting
        '''
        raise CustomExceptions.MethodNotSupported('This method is not supported on ASA')

    def arp_table(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def show_interface_status(self):
        # TODO: Generate Psudo command for this method as its not contained within the firmware directly
        raise CustomExceptions.MethodNotSupported('This command is not supported')

    def show_interface_description(self):
        '''
        This is a pseudo command because it does not exist on the ASA this method will use other commands and
        analyze their output to generate the data needed. It then will create a list of lists with that information
        the same way the method would for a regular IOS device

        :return: list of lists formatted by the following
        [[interface name, admin status, protocol status, description], etc.]
        '''

        def extract_interface_status(element, working_list):

            # checks if the element contains the word down
            if 'down' in element.lower():

                # checks to see if the interface is admin down
                if 'admin' in element.lower():
                    # extracts the words 'Administratively down' and appends them to the list
                    line = element.strip().strip('is').strip()
                    working_list.append(line)
                else:
                    # this code should only be run if the port is down but NOT admin down
                    working_list.append('down')

            # if the port is in an up state it will extract the text here and add it to our list
            if 'up' in element.lower():
                working_list.append(element[-2:])

            return working_list

        def gather_interface_description(working_list):

            # gathers the description of the interface (if there is one)
            flag = 0
            for line in self.show_run_interface(int).splitlines():
                if 'description' in line.lower():
                    flag = 1
                    line = line.strip().split()[1:]
                    working_list.append(' '.join([i for i in line]))

            # if no description was found it inserts a blank string for the description
            if flag == 0:
                working_list.append('')

            return working_list

        self.priv_exec()

        master_list = []

        for int in self.physical_port_inventory_longname():
            interface_list = []

            data = self.transport.send_command_expect_same_prompt('show interface {}'.format(int)).splitlines()[1:][:-2]

            line = data[0].split(',')

            # Grabs interface name
            interface_list.append(line[0].strip().split()[1])

            # gathers the status of the interface (down, admin down, up)
            for n in range(1, 3):
                interface_list = extract_interface_status(line[n], interface_list)

            # gathers the description of the interface (if there is one)
            interface_list = gather_interface_description(interface_list)

            # at this point the interface_list should consist of [int name, up/down, up/down, description]
            # and we can now append it to our master list
            master_list.append(interface_list)

        return master_list

    def show_routes(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

    def show_configured_syslog_server(self):
        '''Returns the value configured for syslog

        :return:
        '''

        '''
        Need to sort out issues with the show run command and utilizing code in the IOS module for this to work
        for now leaving it to throw an error
        
        
        runningConfig = self.show_run()

        servers = []
        for line in runningConfig.splitlines():
            if len(line.split()) > 0:
                if line.split()[0] == 'logging' and line.split()[1] == 'host':
                    servers.append(line.split()[-1:][0])

        if len(servers) == 0:
            return [None]
        else:
            return servers
        '''

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)



    def write_mem(self):

        raise CustomExceptions.MethodNotImplemented(not_implemented_text)

