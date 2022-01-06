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


import time


ctrl_c = chr(3)


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


def detect_firmware(transport):
    '''
    Detects the firmware running on the remote device by counting the number of times specific keywords are
    called out in the 'show version' command and tallies them up and returns the one with the highest result

    :return: str IOSXE, IOS, NXOS, ASA
    '''

    transport.send_command_get_output('terminal length 0')
    output = transport.send_command_get_output('show version', return_as_list=True)

    # defines counter variable to keep track of the number of times a string is found
    results = {'IOSXE': 0, 'IOS': 0, 'NXOS': 0, 'ASA': 0}

    # parses the first 10 lines looking for 4 specific strings
    for line in output[:10]:

        if 'ios-xe' in line.lower() or 'ios xe' in line.lower():
            results['IOSXE'] += 1

        elif 'ios' in line.lower():
            results['IOS'] += 1

        elif 'nx-os' in line.lower():
            results['NXOS'] += 1

        elif 'adaptive security appliance' in line.lower():
            results['ASA'] += 1

    # puts the results in a dictionary


    # stores the key with the highest value in a variable
    firmware_version = max(results, key=results.get)

    # returns variable (Firmware version) from the function
    return output, firmware_version


def extract_version_number_ios(sh_ver_output):
    '''Extracts the version number out of the show version command

    :param sh_ver_output: Full output of show version command
    :return: version number string
    '''
    version_line = [line for line in sh_ver_output[1:] if 'version' in line.lower() and 'boot' not in line.lower()][0]
    version_keyword = version_line.split(',')[-2].strip()
    return version_keyword.split()[-1]


def extract_version_number_iosxe(sh_ver_output):
    '''Extracts the version number out of the show version command

    :param sh_ver_output: Full output of show version command
    :return: version number string
    '''
    version_line = [line for line in sh_ver_output[1:] if 'version' in line.lower() and 'boot' not in line.lower()][0]
    version_keyword = version_line.split(',')[-1].strip()
    return version_keyword.split()[-1]


def extract_version_number_nxos(sh_ver_output):
    '''Extracts the version number out of the show version command

    :param sh_ver_output: Full output of show version command
    :return: version number string
    '''
    version_line = [line for line in sh_ver_output if 'system:' in line.lower()][0].split(':')[-1].strip()
    return version_line.split()[-1]
