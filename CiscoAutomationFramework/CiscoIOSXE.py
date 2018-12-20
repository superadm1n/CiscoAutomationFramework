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
from .CiscoIOS import IOS, TerminalCommands
from .BaseCommandMethods import CommandMethods


class IOSXE(TerminalCommands, CommandMethods):
    '''
    THis class is where the code resides for issuing commands to IOSXE devices. The majority of how you send commands and retrieve data to
    IOSXE and IOS devices are the same so most of the methods contained here simply use the code in the CiscoIOS Module.

    All of the Terminal Commands for IOS and IOSXE are the same so instead of rewriting the code I just reference the same class in the CiscoIOS
    module. If the need ever arises that the commands and everything are different I will need to create a new class specific to IOSXE
    '''

    def __init__(self, ssh_object):
        TerminalCommands.__init__(self, ssh_object)
        self.ssh = ssh_object

        self.ios = IOS(ssh_object)

    def get_uptime(self):
        self.ios.get_uptime()

    def show_run(self):
        '''
        Utilizes 'show_run' method for IOS as it is the same cadence
        :return:
        '''
        return self.ios.show_run()

    def show_run_interface(self, interface):
        # Detects if the session is in priv exec mode on the switch, if not it enters priv exec mode prior to
        # issuing the 'show running-config' command

        return self.ios.show_run_interface(interface)

    def get_local_users(self):
        '''
        Method to extract the local users configured on the system out of the running config
        :return: List of the users configured locally on the system
        '''

        return self.ios.get_local_users()

    def delete_local_user(self, username):

        raise CustomExceptions.MethodNotImplemented()
        output = ''

        output += self.ssh.config_t()

        output += self.ssh.send_command_expect_same_prompt('no username {}'.format(username))

        self.ssh.send_end()

        return output

    def configure_description(self, interface, description):
        raise CustomExceptions.MethodNotImplemented

        output = ''


        output += self.ssh.priv_exec()

        output += self.ssh.config_t()

        output += self.ssh.send_command_expect_different_prompt('interface {}'.format(interface))

        output += self.ssh.send_command_expect_same_prompt('description {}'.format(description))

        output += self.ssh.send_end()

        return output

    def configure_access_vlan(self, interface, vlan):
        return 'Method not configured for IOSXE, skel code is staged from IOS'
        '''
        this method should be used when the user needs to configure an interface as an access port on a specific vlan
        :param interface: interface to configure ex. gi1/0/1, fa0/1, etc.
        :param vlan: Vlan number to configure
        :return: commands sent to server and their output
        '''
        output = ''

        # get the terminal orientated where it needs to be to issue the commands
        output += self.priv_exec()
        output += self.config_t()

        # issues commands to configure the interface specified as an access vlan on the vlan specified
        output += self.ssh.send_command_expect_different_prompt('interface {}'.format(interface))
        output += self.ssh.send_command_expect_same_prompt('switchport mode access')
        output += self.ssh.send_command_expect_same_prompt('switchport access vlan {}'.format(vlan))

        output += self.send_end()


        return output

    def power_cycle_port(self, interface, delay):
        return self.ios.power_cycle_port(interface, delay)

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):
        return 'Method not configured for IOSXE, skel code is staged from IOS'
        '''

        :param physical_interface: Physical interface that the sub interface will belong under
        :param vlan_number: vlan number of sub interface
        :param dhcp_servers_ip_addresses: list of dhcp forwarders
        :return: output of commands
        '''
        output = ''

        self.ssh.config_t()

        output += self.ssh.send_command_expect_different_prompt('interface {}.{}\n'.format(physical_interface, vlan_number))
        output += self.ssh.send_command_expect_same_prompt('encapsulation dot1Q {}\n'.format(vlan_number))
        output += self.ssh.send_command_expect_same_prompt('ip address {} {}'.format(ip_address, subnet_mask))

        if len(dhcp_servers_ip_addresses) > 0:
            for ip in dhcp_servers_ip_addresses:
                output += self.ssh.send_command_expect_same_prompt('ip helper-address {}\n'.format(ip))
                #output += self.ssh.get_output()

        output += self.ssh.send_command_expect_same_prompt('ip directed-broadcast\n')

        self.ssh.send_end()

        return output

    def physical_port_inventory(self):
        '''
        Issues show interface description command, gathers the output, parses the output skipping any vlan or port channel interfaces
        all other interfaces are considered physical interfaces and are appended to a list 'output' to be returned to the user
        :return: List of physical interfaces on device
        '''

        return self.ios.physical_port_inventory()

    def physical_port_inventory_longname(self):

        return self.ios.physical_port_inventory_longname()

    def port_status(self):

        return self.ios.port_status()

    def power_inline(self, summary=False):

        # TODO: Have to configure the command if summary is false

        self.terminal_length()

        data_from_device = self.ssh.send_command_expect_same_prompt('show power inline', return_as_list=True)[3:][:-1]

        if summary is False:
            general_data = []
            for line in data_from_device:
                newline = []
                if len(line.split()) > 1:
                    line = line.split()

                    if len(line) >= 7:
                        if 'interface' in line[0].lower() or '----' in line[0].lower():
                            pass
                        else:
                            for element in line[:4]:
                                newline.append(element)
                                line.remove(element)

                            newline.append(' '.join([str(i) for i in line[:-2]]))

                            for element in line[-2:]:
                                newline.append(element)

                        if len(newline) == 7:
                            general_data.append(newline)

                            #general_data.append(line)

            return general_data

        elif summary is True:
            general_data = []
            for line in data_from_device:
                if len(line.split()) > 1:
                    line = line.split()

                    if len(line) == 4:
                        if 'module' in line[0].lower() or '----' in line[0].lower():
                            pass
                        else:
                            general_data.append(line)
            return general_data

    def list_ospf_configuration(self):

        return self.ios.list_ospf_configuration()

    def list_eigrp_configuration(self):

        return self.ios.list_eigrp_configuration()

    def list_down_ports(self):
        '''
        Issues show interface description command, skips any vlan or port channel interfaces, also skips any interfaces that are not 'down'
        all others are considered physical interfaces in an 'up' status and will add those interface names to a list to return that list
        to the user
        :return: List of physical interfaces in an 'up' status
        '''

        return self.ios.list_down_ports()

    def last_input_and_output(self, interface):
        '''

        :param interface: Interface you wish to check the last input & output on
        :return: a list [Interface, Last Input, Last Output]
        '''

        return self.ios.last_input_and_output(interface)

    def list_configured_vlans(self):

        return self.ios.list_configured_vlans()


    def global_last_input_and_output(self):

        return self.ios.global_last_input_and_output()

    def find_mac_address(self, mac_address):

        return self.ios.find_mac_address(mac_address)

    def mac_address_table(self):

        return self.ios.mac_address_table()

    def cdp_neighbor_table(self):

        return self.ios.cdp_neighbor_table()

    def arp_table(self):

        return self.ios.arp_table()

    def show_interface_status(self):

        return self.ios.show_interface_status()

    def show_interface_description(self):

        return self.ios.show_interface_description()

    def show_routes(self):

        return self.ios.show_routes()

    def show_configured_syslog_sever(self):
        '''Returns the value configured for syslog

        :return:
        '''
        return self.ios.show_configured_syslog_server()


    def write_mem(self):
        if '#' not in self.ssh.prompt:
            self.priv_exec()

        self.check_and_exit_config_t()

        self.ssh.send_command('copy run start\n')
        time.sleep(.2)
        self.ssh.send_command('')  # sends a return key

        return self.ssh.get_output()

    # END Functions used primarily by the User
