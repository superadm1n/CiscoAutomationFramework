#!/usr/bin/python3

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

========================================================================

This module contains the code that the user will interface with directly along with
the transport engines and the engine interfaces.
'''

import time
import logging

from . import CustomExceptions
from .CiscoIOSXE import IOSXE
from .CiscoIOS import IOS
from .CiscoNXOS import NXOS
from .CiscoASA import ASA
from .TransportEngines import TransportInterface


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

logFormatter = logging.Formatter('%(name)s:%(asctime)s:%(message)s')

debug_handler = logging.FileHandler('debug.log')
debug_handler.setFormatter(logFormatter)
debug_handler.setLevel(logging.DEBUG)

logger.addHandler(debug_handler)

class CommandInterface:

    '''
    This class is the interface between the firmware specific logic and the CAF class
    that the user interfaces with. It will call the proper module based on the previously
    detected firmware and issue commands from that module.
    '''

    def priv_exec(self):

        '''
        Enters privilege exec mode, will exit config T if you are in config t, and elevate from standard user mode
        if you are in standard user mode

        :return: Output from command
        '''
        try:
            return self.ssh.priv_exec()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def get_uptime(self):

        '''
        Gets the uptime of the remote device

        :return: str System uptime
        '''
        try:
            return self.ssh.get_uptime()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def show_run(self):
        '''
        Issues 'show running-config' command to to the remote router/switch

        :return: output from command
        '''
        # Detects if the session is in priv exec mode on the switch, if not it enters priv exec mode prior to
        # issuing the 'show running-config' command

        logger.debug('Command interface grabbing show run command')

        try:
            return self.ssh.show_run()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def show_run_interface(self, interface):

        '''

        :param interface: Interface to capture the running config of
        :return: Running Configuration of specified interface
        '''
        try:
            return self.ssh.show_run_interface(interface)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def get_local_users(self):
        '''
        Method to extract the local users configured on the system out of the running config

        :return: List of the users configured locally on the system
        '''
        try:
            return self.ssh.get_local_users()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def delete_local_user(self, username):

        '''

        :param username: Username to delete
        :return:
        '''
        try:
            return self.ssh.delete_local_user(username)

        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def configure_description(self, interface, description):

        '''

        :param interface: Interface to configure discription on
        :param description: str description to configure the interface with
        :return:
        '''

        try:
            return self.ssh.configure_description(interface, description)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def configure_access_vlan(self, interface, vlan):
        '''
        this method should be used when the user needs to configure an interface as an access port on a specific vlan

        :param interface: interface to configure ex. gi1/0/1, fa0/1, etc.
        :param vlan: Vlan number to configure
        :return: commands sent to server and their output
        '''

        try:
            return self.ssh.configure_access_vlan(interface, vlan)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def power_cycle_port(self, interface, delay=5):

        try:
            return self.ssh.power_cycle_port(interface, delay)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):

        try:
            return self.ssh.configure_router_lan_subinterface(physical_interface, vlan_number, ip_address, subnet_mask,
                                                              dhcp_servers_ip_addresses)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def physical_port_inventory(self):
        '''
        Gathers an inventory of physical ports on the remote device

        :return: List of physical interfaces on device
        '''

        try:
            return self.ssh.physical_port_inventory()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def physical_port_inventory_longname(self):

        '''
        Gathers an inventory of physical ports on the remote device with their full name ex. GigabitEthernet1/0/1
        vs their abbreviated name ex. Gi1/0/1

        :return: list of ports
        '''

        try:
            return self.ssh.physical_port_inventory_longname()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def port_status(self):

        '''


        :return:
        '''

        try:
            return self.ssh.port_status()
        except CustomExceptions.MethodNotImplemented as E:
            return E

    def power_inline(self, summary=False):

        '''
        Method to get the power inline statics for remote POE device

        :param summary: bool if set to true it will get the overview information and not the individual port information
        :return: list of lists containing the power inline details
        '''

        try:

            return self.ssh.power_inline(summary)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def list_ospf_configuration(self):

        '''

        :return: OSPF Configuration
        '''

        try:

            return self.ssh.list_ospf_configuration()

        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def list_eigrp_configuration(self):
        '''

        :return: EIGRP Configuration
        '''

        try:

            return self.ssh.list_eigrp_configuration()

        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def list_down_ports(self):
        '''
        Issues show interface description command, skips any vlan or port channel interfaces, also skips any interfaces that are not 'down'
        all others are considered physical interfaces in an 'up' status and will add those interface names to a list to return that list
        to the user

        :return: List of physical interfaces in an 'up' status
        '''

        try:
            return self.ssh.list_down_ports()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def last_input_and_output(self, interface):
        '''

        :param interface: Interface you wish to check the last input & output on
        :return: a list [Interface, Last Input, Last Output]
        '''

        try:
            return self.ssh.last_input_and_output(interface)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def list_configured_vlans(self):
        return self.ssh.list_configured_vlans()

    def global_last_input_and_output(self):

        try:
            return self.ssh.global_last_input_and_output()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def find_mac_address(self, mac_address):
        '''
        Searches the MAC address table for a MAC address entry

        :param mac_address: MAC address or partial MAC address to search for
        :return: List [Mac Address, Interface ]
        '''

        # TODO: Add in this method for Cisco ASA and NXOS
        # TODO: Test against IOSXE
        try:
            return self.ssh.find_mac_address(mac_address)
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def mac_address_table(self):
        '''

        :return: List of lists containing the MAC address table and its contents
        '''
        try:
            return self.ssh.mac_address_table()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def cdp_neighbor_table(self):

        # TODO: Add support for ASA, and NXOS and test IOSXE
        try:
            return self.ssh.cdp_neighbor_table()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def arp_table(self):

        # TODO: Test against IOSXE, add support for NXOS and ASA

        try:
            return self.ssh.arp_table()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def show_interface_status(self):

        '''

        :return:
        '''

        try:
            return self.ssh.show_interface_status()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def show_interface_description(self):
        '''
        Sets terminal length to infinite, issues show interface description command, gathers output from remote device,
        split in a list by line

        :return: List of output, split by line in output
        '''

        try:
            return self.ssh.show_interface_description()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def show_routes(self):
        ''''
        Returns list of lists containing the routing table.
        '''

        # TODO: add support for NXOS & ASA and test IOSXE
        try:
            return self.ssh.show_routes()
        except CustomExceptions.MethodNotImplemented as E:
            raise E

    def write_mem(self):

        '''
        Saves the running configuration to startup configuration

        :return:
        '''
        try:
            return self.ssh.write_mem()
        except CustomExceptions.MethodNotImplemented as E:
            raise E
    '''
    def test(self):
        return self.ssh.test()      
    '''


class CAF(TransportInterface, CommandInterface):

    '''
    This is the class that the user will interface with, this class is responsible for detecting
    the firmware of the device and then issuing commands based on that firmware version.
    '''

    def __init__(self, engine='ssh'):

        '''

        :param engine: Transport Engine to use (ssh or serial)

        '''

        TransportInterface.__init__(self, engine)
        CommandInterface.__init__(self)

        self.engine = engine
        self.enable_password = None
        self.terminal_length_value = None
        self.terminal_width_value = None
        self.firmware_version = None
        self.ssh = None

    def instantiate_object(self):

        '''
        Sets up self.ssh to reference the proper module based on the IOS version of the devicve

        :return: SSH object to interface with remote device
        :rtype: object
        '''

        if self.firmware_version == 'IOS':
            return IOS(self)

        elif self.firmware_version == 'IOSXE':
            return IOSXE(self)

        elif self.firmware_version == 'NXOS':
            return NXOS(self)

        elif self.firmware_version == 'ASA':
            return ASA(self)

        else:
            raise CustomExceptions.OsDetectionFailure('Unable to detect OS for device')

    def detect_firmware(self):

        '''
        Detects the firmware running on the remote device by counting the number of times specific keywords are
        called out in the 'show version' command and tallies them up and returns the one with the highest result

        :return: str IOSXE, IOS, NXOS, ASA
        '''

        self.transport.send_command(self, command='show version')
        time.sleep(.2)
        for n in range(1, 4):
            self.transport.send_command(self, ' ')
            time.sleep(.1)


        output = self.transport.send_command_expect_same_prompt(self, ' ', detecting_firmware=True, return_as_list=True,
                                                                timeout=10)

        # defines counter variable to keep track of the number of times a string is found
        iosxe = 0
        ios = 0
        nxos = 0
        asa = 0

        # parses the first 10 lines looking for 4 specific strings
        for line in output[:10]:

            if 'ios-xe' in line.lower() or 'ios xe' in line.lower():
                iosxe += 1

            elif 'ios' in line.lower():
                ios += 1

            elif 'nx-os' in line.lower():
                nxos += 1

            elif 'adaptive security appliance' in line.lower():
                asa += 1

        # puts the results in a dictionary
        results = {'IOSXE': iosxe, 'IOS': ios, 'NXOS': nxos, 'ASA': asa}

        # stores the key with the highest value in a variable
        firmware_version = max(results, key=results.get)

        # returns variable (Firmware version) from the function
        return firmware_version

    def connect(self, destination, username, password, enable_password=None):

        # This needs to be called before instansiating an SSH object because
        # the enable password will not properly get passed to those objects if it is not
        self.enable_password = enable_password

        self.connect_to_server(destination, username, password)  # makes connection
        self.firmware_version = self.detect_firmware()  # detects firmware
        self.ssh = self.instantiate_object()  # instantiates object to send commands with

