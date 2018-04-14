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
