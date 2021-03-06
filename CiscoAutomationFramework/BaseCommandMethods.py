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

This module contains the code of the abstract API class that the user will
interface with when writing their automation scripts
'''

from .CustomExceptions import MethodNotImplemented

class CommandGetMethods:

    '''
    These are the API calls that will most often be used when gathering data from a Cisco device in an automation script.
    Each of these calls are abstract ways of sending specific commands to a switch, gathering the output, and parsing
    that output so that it is in a format that is digestable to the rest of the script. As a network
    administrator, worry less about what exact command it is sending to the switch and focus more
    on the data that it is returning to you. These calls are powerfull because of how it parses
    the CLI commands and presents just the relevant data to you vs the raw data as it is output from
    the Cisco device.

    notes to any code contributer:
    This is the generic class that all other command classes should inherit from. When a new method
    is added it should be added here first, documentation for each method should be held here.
    Whenever a new method is implemented all reasonable efforts
    should be attempted to have it return a list of dictionaries as its output if it is gathering data
    and true/false if it is performing an action to keep the data returned from methods as consistent
    as possible for anyone using the package.
    If it is not possible to return the data in that format or is unreasonable to do so, it should be
    clearly documented as to the format and why it is returning that way in the docstring in this class
    of the method.

    :TODO: Break out the methods that modify configuration into a different class from this one
    '''

    def get_uptime(self):
        '''Method to return the current uptime of the remote device.

        :return: Uptime of device.
        :rtype: str
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_run(self):
        '''Returns the running config of the remote device

        :return:
        :rtype: str
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def get_local_users(self):
        '''Gathers the local users that are configured on the Cisco device

        :return: list of local users configured
        :rtype: list
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_run_interface(self, interface):
        '''Gathers the running configuration for a specific interface on the remote device.

        :param interface: Interface to gather the running config for
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def power_cycle_port(self, interface, delay):
        '''Power cycles a specific port, leaving it in an admin down state for a
        specified amount of time

        :param interface: Interface to cycle
        :type interface: str
        :param delay: Time in seconds to leave off
        :type delay: int
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):
        '''Method to configure a sub interface on a Cisco router

        *warning* This method will most likely be removed in the near future because it doesnt necessarily fit in the framework.

        :param physical_interface:
        :param vlan_number:
        :param ip_address:
        :param subnet_mask:
        :param dhcp_servers_ip_addresses:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def physical_port_inventory(self):
        '''Gathers the physical ports of the device and returns them as a list of strings

        :return: List of strings
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def physical_port_inventory_longname(self):
        '''Very similar to the physical port inventory but instead of returning the
        abbreviated name `fa1/0/1` it returns the whole name `FastEthernet1/0/1`

        :return: List of strings
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def port_status(self):
        '''Method to return the status of the ports on the Cisco device

        :return: List of dictionaries
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def power_inline(self):
        '''Method to return the data that corresponds to the power output of the Cisco device

        :return: List of dictionaries
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def list_ospf_configuration(self):
        '''Method to return the OSPF section(s) of the running configuration of the Cisco device

        :return: OSPF running configuration
        :rtype: str
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def list_eigrp_configuration(self):
        '''Method to return the EIGRP section(s) of the running configuration of the Cisco device

        :return: EIGRP running configuration
        :rtype: str
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def list_down_ports(self):
        '''Method to return a list of all of the down ports on a Cisco device

        :return: List of down ports
        :rtype: list
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def last_input_and_output(self, interface):
        '''Method to return the last input and last output of a specific interface on a Cisco device.

        :param interface: Interface to return the data on
        :return: List in the format of [Interface, Last Input, Last Output]
        :rtype: list
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def last_input_and_output_all(self):
        '''Method to return the last input and last output of every interface on the Cisco device vs
        just a single one. When you need to gather several interfaces this is a MUCH faster way to
        get the data as the Cisco device only needs to compile the data a single time and returns it all
        to the script.

        :return: Last I/O for all of the interfaces on a Cisco device
        :rtype: list of dicts
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def list_configured_vlans(self):
        '''

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def mac_address_table(self):
        '''Method to return the data of the MAC address table on the Cisco device.

        :return: MAC address table
        :rtype: list of dicts
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def find_mac_address(self, mac_address, mac_table=None):
        '''

        :param mac_address:
        :param mac_table:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def cdp_neighbor_table(self):
        '''Method to return the data in the CDP Neighbor table in the following format.

        [{deviceid: 'str', localinterface: 'str', remoteinterface: 'str', platform: 'str', remoteip: 'str'}, etc.]

        :return: CDP neighbor table
        :rtype: list of dicts in the format

        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def arp_table(self):
        '''Method to return the arp table data of the Cisco device in the following format.

        [{'protocol': str, 'address': str, 'age': str, 'mac': str, 'type': str, 'interface': str}]

        :return: Data from arp table
        :rtype: list of dicts
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_routes(self):
        '''

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_interface_status(self):
        '''Method to return the status of each interface on the Cisco device in the following format.

        [{'interface': str, 'status': notconnected/disabled/connected}]

        :return: status of each interface
        :rtype: list of dicts
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_interface_description(self):
        '''

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_configured_syslog_server(self):
        '''Method to return a list of configured syslog servers.
        This method has been implemented to return a simple list as it would not
        make sense to store that data in a dictionary

        :return: List of the configured syslog servers
        :rtype: list
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_vlan(self):
        '''Method to return all of the vlans configured on the Cisco device and the ports associated
        with them. Basically this is the output of the IOS command 'show vlan' but presented in a way
        that can be used in a programmatic way. When implemented this method should return data in the
        following format.

        [{vlan: str, description: str, interfaces [int1, int2, etc]}]

        :return: List of dictionaries with the data of the configured vlans on the Cisco device.
        :rtype: list of dicts
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def shutdown_interface(self, interface):
        '''Method to place an interface in admin down, example issuing the 'shutdown' command on IOS.

        :param interface: Interface to admin down.
        :return: Nothing at this point.
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def no_shutdown_interface(self, interface):
        '''Method to enable an interface, example issuing the 'no shutdown' command on IOS.

        :param interface: Interface to enable.
        :return: Nothing at this point.
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def set_access_vlan_on_interface(self, interface, vlan_number):
        '''

        :param interface:
        :param vlan_number:
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_inventory_data(self):
        '''Returns the data of the inventory data of a Cisco device, example the data of 'show inventory' IOS command

        :return: List of dictionaries containing the inventory data of the device
        :rtype: list
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def show_hsrp_info(self):
        '''Returns the data of show standby brief in  a list of dictionaries. This will alow the user to
        get information about HSRP such as the interfaces, group numbers, priority, status, Virtual IP's, etc.

        :raises: NotConfiguredError
        :return: List of dictionaries
        '''

        raise MethodNotImplemented('This method has not been implemented!')


    def write_mem(self):
        '''Method to save the running config into NVRAM on the Cisco device. Example write memory or copy run start on
        an IOS device.

        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')


class CommandConfigMethods:

    def configure_description(self, interface, description):
        '''Configures a description on a specific interface.

        :param interface: Interface to configure the description on
        :param description: Description to add
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def configure_access_vlan(self, interface, vlan):
        '''Configues a specific interface as an access vlan on
        the specified vlan

        :param interface: Interface to configure
        :type interface: str
        :param vlan: Vlan to configure
        :type vlan: str
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')

    def delete_local_user(self, username):
        '''Method to delete the specified local user

        :param username: User to delete
        :return:
        '''
        raise MethodNotImplemented('This method has not been implemented!')