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


'''
Code in the "Util.py" module contains various utilities that might need to be used along side an ssh connection such as
running a ping test to validate the host is up or an automated utility to check authentication against a Cisco device.
'''

import os
import subprocess
from getpass import getpass
import socket
from .Framework import CAF

# Exceptions used in this module

class NoIPAvailable(Exception):
    pass

class ListOfIPsNotProvided(Exception):
    pass

class IPAddressNotValid(Exception):
    pass

class PingTest:
    '''
    Class that contains code for doing ping tests against network devices
    '''

    @classmethod
    def validateIPaddress(cls, ipaddr):

        try:
            socket.inet_aton(ipaddr)
            return True
        except:
            return False

    @classmethod
    def ping(cls, ipaddr):
        '''

        Method that sends a basic ping to an IP address and returns true or false depending
        on if there was a response received.

        :param ipaddr: IP address to run a ping test against
        :type ipaddr: String
        :return: True if a response is received False if there is no response
        '''

        ipaddr = str(ipaddr)

        cls.validateIPaddress(ipaddr)

        if os.name == 'nt':
            status, result = subprocess.getstatusoutput("ping -n 1 -w 2 {}".format(ipaddr))

        else:
            status, result = subprocess.getstatusoutput("ping -c1 -w2 {}".format(ipaddr))

        if status == 0:

            return True
        else:
            return False

class CredCheck(PingTest):
    '''
    This class contains methods to test user authentication both to the switch/router and into enable mode.
    '''

    def __init__(self, transport, listofipsorserialinterface):
        '''

        :param transport: serial or ssh, the transport engine to use
        :type transport: str
        :param listofipsorserialinterface: this variable will either be a string or a list of strings, a list if ssh is the transport, a string \
        if serial is the transport
        :type listofipsorserialinterface: str/list
        '''

        self.transport = transport
        self.destination = None

        if transport == 'ssh':
            if type(listofipsorserialinterface) is not type(list()):
                raise ListOfIPsNotProvided('You did not provide a list of IP addresses')
            self.destination = self.decide_ip_to_use(listofipsorserialinterface)

        elif transport == 'serial':
            self.destination = listofipsorserialinterface
        else:
            pass


        '''
        if self.destination is None:
            raise CustomExceptions.NoHostPingable('None of the IP addresses provided ping. Addresses provided: {}'.format(', '.join(list_of_IOS_devices)))
        '''

    def decide_ip_to_use(self, list_of_IP_addresses):

        '''Cycles through list of IP addresses provided pinging each one and will return the first one that responds to ping

        :param list_of_IP_addresses: list of IP addresses that we can use to check authentication against
        :type list_of_IP_addresses: list
        :return: first IP that responds to ping
        '''

        ping = PingTest()

        for ip in list_of_IP_addresses:
            if ping.ping(ip) is True:
                return ip

        raise NoIPAvailable('No IP address is pingable in the list of IP addresss supplied: {}'.format(list_of_IP_addresses))

    def gather_user_pass(self):
        '''
        CLI method to gather a username and password

        :return: List containing username and password
        :rtype: list
        '''
        username = input('Enter Username: ')
        password = getpass('Enter Password: ')
        return [username, password]

    def gather_enable(self):
        '''
        CLI method to gather an enable password

        :return: Enable password entered by user
        :rtype: str
        '''
        enable_password = getpass('Enter enable password: ')
        return enable_password

    def test_user_pass(self, username, password):
        '''
        Method to test a username and password against a router or switch

        :param username: Username to supply to the device
        :type username: str
        :param password: Password to supply to the device
        :type password: str
        :return: True or False depending if the username and password were accepted
        :rtype: bool
        '''
        try:
            with CAF(self.transport) as ssh:
                ssh.connect(self.destination, username, password)
                pass
            return True

        except:
            return False

    def test_enable(self, username, password, enable_password):
        '''
        Method to test an enable password and validate it is able to elevate privilege into enable mode

        .. note:: The Username and Password supplied must be previously tested to have access

        :param username: Confirmed working username for the device
        :type username: str
        :param password: Confirmed working password that corresponds to the username
        :type password: str
        :param enable_password: Enable password to attempt authentication with
        :type enable_password: str
        :return: True/False depending on if the enable password is accepted or not
        :rtype: bool
        '''
        with CAF(self.transport) as ssh:
            ssh.connect(self.destination, username, password, enable_password=enable_password)
            output = ssh.priv_exec().lower()

        for line in output.splitlines():
            if 'denied' in line:
                return False

        return True

    def cli_run_no_enable(self):
        '''
        CLI utility to gather a username and password and test its authentication against a cisco device, this method will loop
        until a username and password combination is accepted

        :return: List containing username and password
        :rtype: list
        '''

        username, password = self.gather_user_pass()

        while self.test_user_pass(username, password) is False:
            print('Username or Password incorrect! Please try again\n')
            username, password = self.gather_user_pass()

        return [username, password]

    def cli_run_with_enable(self):
        '''
        CLI utility to gather both a username and password combination and an enable password, this will loop until a successful username and
        password combination and enable password is received.

        :return: List containing username, password, and enable password.
        :rtype: List
        '''
        username, password = self.gather_user_pass()

        while self.test_user_pass(username, password) is False:
            print('Username or Password incorrect! Please try again\n')
            username, password = self.gather_user_pass()

        enable_password = self.gather_enable()

        while self.test_enable(username, password, enable_password) is False:
            print('Enable password incorrect! Please try again\n')
            enable_password = self.gather_enable()

        return [username, password, enable_password]

class IPaddress:

    subnets = (('32', '255.255.255.255'),
               ('31', '255.255.255.254'),
               ('30', '255.255.255.252'),
               ('29', '255.255.255.248'),
               ('28', '255.255.255.240'),
               ('27', '255.255.255.224'),
               ('26', '255.255.255.192'),
               ('25', '255.255.255.128'),
               ('24', '255.255.255.0'),
               ('23', '255.255.254.0'),
               ('22', '255.255.252.0'),
               ('21', '255.255.248.0'),
               ('20', '255.255.240.0'),
               ('19', '255.255.224.0'),
               ('18', '255.255.192.0'),
               ('17', '255.255.128.0'),
               ('16', '255.255.0.0'),
               ('15', '255.254.0.0'),
               ('14', '255.252.0.0'),
               ('13', '255.248.0.0'),
               ('12', '255.240.0.0'),
               ('11', '255.224.0.0'),
               ('10', '255.192.0.0'),
               ('9', '255.128.0.0'),
               ('8', '255.0.0.0'),
               ('7', '254.0.0.0'),
               ('6', '252.0.0.0'),
               ('5', '248.0.0.0'),
               ('4', '240.0.0.0'),
               ('3', '224.0.0.0'),
               ('2', '192.0.0.0'),
               ('1', '128.0.0.0')
               )


    @classmethod
    def is_valid_addr(cls, ipaddr):
        '''Method to validate that a string that is passed in is a valid IP address

        :param ipaddr: IP address to check
        :type ipaddr: str
        :return: True if valid, False if invalid
        :rtype: bool
        '''

        try:
            socket.inet_aton(ipaddr)
            return True
        except:
            return False

    @classmethod
    def subnet_to_cidr(cls, subnet):

        '''Method to convert a subnet mask (255.255.255.0) to a cidr notation (24)

        :param subnet: Subnet mask ex.255.255.255.0
        :type subnet: str
        :return: CIDR notation of subnet mask
        :rtype: str
        '''

        # Generates a list of valid subnets
        validSubnets = [x[1] for x in cls.subnets]

        # throws error if the subnet submitted is not valid
        if subnet not in validSubnets:
            raise ValueError('Subnet mask {} that was submitted is not a valid subnet mask!'.format(subnet))

        # At this point we are assuming that the subnet that was submitted is a valid
        # subnet and is ready to be converted.

        # converts the subnet into CIDR notation
        cidr = None
        for validSub in cls.subnets:
            if validSub[1] == subnet:
                cidr = validSub[0]

        # returns the CIDR notation
        if cidr is not None:
            return cidr
        else:
            raise Exception('An unknown exception has occured with supplied subnet {}'.format(subnet))


    @classmethod
    def cidr_to_subnet(cls, cidr):

        '''Method to convert a CIDR notation ex. /24 into a subnet mask ex. 255.255.255.0

        :param cidr: CIDR notation, can be in format with or without preceeding slash ex. /24; 24
        :type cidr: str
        :return: Subnet mask of CIDR notation
        :rtype: str
        :raises ValueError: if the CIDR notation supplied was invalid.
        :raises Exception: if an unknown exception occured.
        '''

        valid_cidrs = [x[0] for x in cls.subnets]

        # removes a preceding slash if there is one
        if '/' in cidr:
            cidr = cidr.strip('/')

        # validates that there is no more than 2 digits
        if len(cidr) > 2:
            raise ValueError('The CIDR notation {} that you submitted is invalid'.format(cidr))

        # validats the CIDR notation is in fact a valid one
        if cidr not in valid_cidrs:
            raise ValueError('The CIDR notation {} that was submitted is invalid'.format(cidr))

        # By this point we are assuming that the CIDR notation has passed the proper
        # checks and is a valid CIDR notation.

        # grabs the corresponding subnet for the supplied CIDR
        subnet = None
        for entry in cls.subnets:
            if entry[0] == cidr:
                subnet = entry[1]

        # this if/else is here just in case there is an exception that has not been already accounted for.
        if subnet is not None:
            return subnet
        else:
            raise Exception('An unknown exception occurred with CIDR {}'.format(cidr))

