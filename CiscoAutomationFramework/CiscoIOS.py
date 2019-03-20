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

This Module contains all the logic that pertains to issuing commands to a device that is running IOS firmware.
'''

import time
import logging
from .CustomExceptions import *
from .BaseCommandMethods import CommandGetMethods, CommandConfigMethods
from CiscoAutomationFramework import log_level

level = log_level
logFile = 'CiscoAutomationFramework.log'

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.propagate = False

logFormatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s')

if level <= 50:
    try:

        # file handler for debug logs
        if level <= 10:
            debug_handler = logging.FileHandler(logFile)
            debug_handler.setFormatter(logFormatter)
            debug_handler.setLevel(logging.DEBUG)
            logger.addHandler(debug_handler)

        # file handler for info logs
        if level <= 20:
            info_handler = logging.FileHandler(logFile)
            info_handler.setFormatter(logFormatter)
            info_handler.setLevel(logging.DEBUG)
            logger.addHandler(info_handler)

        # file handler for warning logs
        if level <= 30:
            warning_handler = logging.FileHandler(logFile)
            warning_handler.setFormatter(logFormatter)
            warning_handler.setLevel(logging.WARNING)
            logger.addHandler(warning_handler)

        # file handler for error logs
        if level <= 40:
            error_handler = logging.FileHandler(logFile)
            error_handler.setFormatter(logFormatter)
            error_handler.setLevel(logging.ERROR)
            logger.addHandler(error_handler)

        # file handler for critical logs
        if level <= 50:
            critical_handler = logging.FileHandler(logFile)
            critical_handler.setFormatter(logFormatter)
            critical_handler.setLevel(logging.CRITICAL)
            logger.addHandler(critical_handler)

    except PermissionError as E:
        print(E)
        print('CiscoAutomationFramework does not have permission to write log file, disabling logging')
        logger.disabled = True

    except:
        print('Unknown error occured when trying to setup logging, disabling logging!')
        logger.disabled = True


class TerminalCommands:
    '''
    This class contains the code that is used to have the framework both detect where it is located on the command line and
    maneuver through different prompts on the commands line.
    '''

    def __init__(self, transport_object):
        self.transport = transport_object
        self.enable_password = self.transport.enable_password


    def terminal_length(self, number='0'):
        '''
        Sets Terminal length to infinite by default or to user specification on a Cisco IOS router or switch
        :return: Output from command
        '''

        self.check_and_exit_config_t()

        # checks if terminal length that the user is requesting is already set and if it has been it breaks out of the function.
        if self.transport.terminal_length_value == str(number):
            return 'Terminal length already set to proper value'

        self.transport.terminal_length_value = str(number)

        return self.transport.send_command_expect_same_prompt('terminal length {}'.format(number))

    def terminal_width(self, number='0'):
        '''
        Sets Terminal width to infinite by default or to user specification on a Cisco IOS router or switch
        :return: Output from command
        '''
        self.check_and_exit_config_t()

        if self.transport.terminal_width_value == str(number):
            return 'Terminal width already set to proper value'

        self.transport.terminal_width_value = str(number)

        return self.transport.send_command_expect_same_prompt('terminal width {}'.format(number))

    def priv_exec(self):
        '''
        Issues the enable command and then types the enable password and send a return keystroke
        :return: output from command
        :raises NoEnablePassword: If the user doesnt populate the self.enable_password field and a method attempts \
        to elevate into enable mode it will raise this exception
        '''

        if '#' not in self.transport.prompt:

            if self.enable_password is None:
                logger.debug('No enable password supplied, exception raised')
                raise NoEnablePassword('There was no enable password supplied to the server')

            logger.debug('sending enable command')
            self.transport.send_command('enable')
            time.sleep(.5)
            return self.transport.send_command_expect_different_prompt(self.enable_password)

        elif '(config' in self.transport.prompt:
            return self.send_end()

        else:
            return 'Already in enable mode'

    def config_t(self):
        '''
        Method to enter Config T mode. If the shell is not in Privlege exec mode already it will enter privlege exec
        mode and then enter config t and then capture the output and return the output to the user
        :return:
        '''
        output = ''

        # Detects if the session is in priv exec mode on the switch, if not it enters priv exec mode prior to
        # issuing the 'show running-config' command
        if '#' not in self.transport.prompt:
            self.priv_exec()

        if '(config' not in self.transport.prompt:
            logger.debug('sending configure terminal command')
            output += self.transport.send_command_expect_different_prompt('configure terminal')

            return output
        else:
            logger.debug('already in config t mode')
            return 'Already in config mode'

    def check_and_exit_config_t(self):

        output = ''
        if '(config' in self.transport.prompt:
            logger.debug('in config T, backing out')
            output += self.send_end()

        return output

    def send_end(self):

        return self.transport.send_command_expect_different_prompt('end')


class IOS(TerminalCommands, CommandGetMethods):
    '''
    This class contains the code that is responsible for auctualy sending the commands to the remote device, retrieveing, and parsing the output.

    The code in this class is tailored to Devices running IOS
    '''

    def __init__(self, transport_object):
        TerminalCommands.__init__(self, transport_object)
        self.config = IOSConfigMethods(transport_object)

        self.transport = transport_object

    def get_uptime(self):

        output = ''

        self.terminal_length()
        device_output = self.transport.send_command_expect_same_prompt('show version')

        for line in device_output.splitlines():

            if '{} uptime'.format(self.transport.hostname.lower()) in line.lower():
                output += line
                break

        return output

    def show_run(self, timeout=15):
        '''
        Issues 'show running-config' command to to the remote router/switch
        :return: output from command
        '''
        # Detects if the session is in priv exec mode on the switch, if not it enters priv exec mode prior to
        # issuing the 'show running-config' command
        logger.debug('Issuing show run commands')
        self.priv_exec()
        self.check_and_exit_config_t()

        # sets terminal length to infinite so all the output is captured
        self.terminal_length()

        logger.debug('Sending show run command, expecting same prompt')
        output = self.transport.send_command_expect_same_prompt('show running-config', buffer_size=50, timeout=timeout)
        logger.debug('Output function returned.')

        return output

    def get_local_users(self):
        '''
        Method to extract the local users configured on the system out of the running config
        :return: List of the users configured locally on the system
        '''

        users = []

        running_config = self.show_run()

        # Finds a line that has the string 'username' in it, then splits the line by spaces and if the string 'username' is the
        # string in index 0 it appends index 1 to the output.
        for line in running_config.splitlines():
            if 'username' in line:
                if 'username' in line.split()[0]:
                    users.append(line.split()[1])

        return users

    def show_run_interface(self, interface):
        # Detects if the session is in priv exec mode on the switch, if not it enters priv exec mode prior to
        # issuing the 'show running-config' command

        self.priv_exec()
        self.check_and_exit_config_t()

        # sets terminal length to infinite so all the output is captured
        self.terminal_length()

        device_output = self.transport.send_command_expect_same_prompt('show running-config interface {}'.format(interface))

        cleanoutput = ''

        # Gets output from the server, cuts the first 2 and last 2 lines and puts it into a string to return
        for line in device_output.splitlines()[2:][:-2]:
            cleanoutput += str(line) + '\n'

        return cleanoutput

    def power_cycle_port(self, interface, delay):

        self.config_t()
        output = ''

        output += self.transport.send_command_expect_different_prompt('interface {}'.format(interface))
        output += self.transport.send_command_expect_same_prompt('shutdown')
        time.sleep(delay)
        output += self.transport.send_command_expect_same_prompt('no shutdown')

        self.send_end()

        return output

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):
        '''

        :param physical_interface: Physical interface that the sub interface will belong under
        :param vlan_number: vlan number of sub interface
        :param dhcp_servers_ip_addresses: list of dhcp forwarders
        :return: output of commands
        '''
        output = ''

        self.config_t()

        output += self.transport.send_command_expect_different_prompt('interface {}.{}\n'.format(physical_interface, vlan_number))
        output += self.transport.send_command_expect_same_prompt('encapsulation dot1Q {}\n'.format(vlan_number))
        output += self.transport.send_command_expect_same_prompt('ip address {} {}'.format(ip_address, subnet_mask))

        if len(dhcp_servers_ip_addresses) > 0:
            for ip in dhcp_servers_ip_addresses:
                output += self.transport.send_command_expect_same_prompt('ip helper-address {}\n'.format(ip))
                #output += self.transport.get_output()

        output += self.transport.send_command_expect_same_prompt('ip directed-broadcast\n')

        self.send_end()

        return output

    def physical_port_inventory(self):
        '''
        Issues show interface description command, gathers the output, parses the output skipping any vlan or port channel interfaces
        all other interfaces are considered physical interfaces and are appended to a list 'output' to be returned to the user
        :return: List of physical interfaces on device
        '''

        output = list()

        # This for loop will get the output from the switch and omit any vlan or port channel interfaces to only return the physical interfaces.
        for interface in self.show_interface_description():

            if 'vl' in interface[0].lower():  # removes vlan interfaces from output
                pass
            elif 'po' in interface[0].lower():  # removes port chanel interfaces from output
                pass
            else:
                output.append(interface[0])  # appends all other interfaces to list

        return output

    def physical_port_inventory_longname(self):

        port_list = []
        self.terminal_length()

        # issues 'show interfaces' command on device
        for line in self.transport.send_command_expect_same_prompt('show interfaces', return_as_list=True, buffer_size=200)[1:][:-1]:

            if line[0] is not ' ':

                # Omits port-channel and vlan interfaces, adds all the rest
                if line[:2].lower() == 'vl' or line[:2].lower() == 'po':
                    pass
                else:
                    port_list.append(line.split()[0])


        return port_list

    def port_status(self):
        self.terminal_length()
        switch_data = self.transport.send_command_expect_same_prompt('show interfaces status', return_as_list=True)

        flag = False
        usable_data = []
        header = []
        for line in switch_data:
            if 'port' in line.lower() and 'status' in line.lower():
                flag = True
                header = [x.lower() for x in line.split()]
                continue

            if flag == True:
                if len(line.split()) >= 7:
                    var = line.split()
                    usable_data.append(
                        {header[0]: var[0], header[1]: ' '.join(var[:-5][1:]), header[2]: var[2], header[3]: var[3], header[4]: var[4], header[5]: var[5],
                         header[6]: var[6]}
                    )
                elif len(line.split()) == 6:
                    var = line.split()
                    usable_data.append(
                        {header[0]: var[0], header[1]: '', header[2]: var[1], header[3]: var[2], header[4]: var[3], header[5]: var[4],
                         header[6]: var[5]}
                    )
        return usable_data

    def power_inline(self):

        def determine_flag(data):
            count = 0
            for line in data:
                if '---' in line:
                    count += 1

            if count == 1:
                return 1
            else:
                return 2


        self.terminal_length()

        data = self.transport.send_command_expect_same_prompt('show power inline', return_as_list=True)[3:][:-1]

        trigger_seperators = determine_flag(data)

        usable_data = []
        flag = 0
        for line in data:
            if '---' in line:
                flag += 1
                continue

            if flag == trigger_seperators:
                usable_data.append(line)

        returnable_data = []
        for x in usable_data:
            line = x.split()
            if len(line) == 7:
                returnable_data.append({'interface': line[0], 'admin': line[1], 'oper': line[2], 'watts': line[3], 'device': line[4], 'class': line[5], 'max': line[6]})
            else:
                returnable_data.append(
                {'interface': line[0], 'admin': line[1], 'oper': line[2], 'watts': line[3], 'device': ' '.join(line[4:][:-2]), 'class': line[-2], 'max': line[-1]})

        return returnable_data

    def list_ospf_configuration(self):

        output = ''
        running_config = self.transport.show_run()
        counter = 0
        for line in running_config.splitlines():

            if 'router ospf' in line.lower():
                counter = 1

            elif '!' in line:
                counter = 0

            if counter == 1:
                output += '{}\n'.format(line)

        if len(output) == 0:
            output = 'No OSPF process configured'

        return output

    def list_eigrp_configuration(self):
        output = ''
        running_config = self.transport.show_run()
        counter = 0
        for line in running_config.splitlines():

            if 'router eigrp' in line.lower():
                counter = 1

            elif '!' in line:
                counter = 0

            if counter == 1:
                output += '{}\n'.format(line)

        if len(output) == 0:
            output = 'No EIGRP process configured'

        return output

    def list_down_ports(self):
        '''
        Issues show interface description command, skips any vlan or port channel interfaces, also skips any interfaces that are not 'down'
        all others are considered physical interfaces in an 'up' status and will add those interface names to a list to return that list
        to the user
        :return: List of physical interfaces in an 'up' status
        '''

        output = []

        for interface in self.show_interface_description():

            if 'vl' in interface[0].lower():  # removes vlan interfaces from output
                pass
            elif 'po' in interface[0].lower():  # removes port chanel interfaces from output
                pass
            else:
                if interface[1].lower() == 'down':
                    output.append(interface[0])

        return output

    def last_input_and_output(self, interface):
        '''

        :param interface: Interface you wish to check the last input & output on
        :return: a list [Interface, Last Input, Last Output]
        '''

        output = []

        self.terminal_length()

        sw_output = self.transport.send_command_expect_same_prompt('show interface {}'.format(interface), buffer_size=200, return_as_list=True)



        for line in sw_output:

            if 'last input' in line.lower():
                line = line.split(',')

                last_input = line[0].strip().split()[-1:][0]
                last_output = line[1].strip().split()[-1:][0]

                output.append(interface)
                output.append(last_input)
                output.append(last_output)

                # Exits loop as we now will have the data we need
                break


        return output

    def last_input_and_output_all(self):
        '''Very similar to the last input output method, but instead returns all interfaces in a matter of seconds
        in a list of dictionaries'''
        self.terminal_length()
        sw_output = self.transport.send_command_expect_same_prompt('show interfaces', buffer_size=200, return_as_list=True)


        data = []
        tmp = {'interface': '', 'input': '', 'output': ''}
        for line in sw_output:
            if line[0].isalpha():
                tmp['interface'] = line.split()[0]

            if 'last input' in line.lower():
                tmp['input'] = line.lstrip().split()[2].strip(',')
                tmp['output'] = line.lstrip().split(',')[1].strip().split()[1]
                data.append(tmp)
                tmp = {}

        return data

    def list_configured_vlans(self):

        initial_term_width = self.transport.terminal_width_value
        self.terminal_width()  # sets terminal width to infinite

        commandOutput = self.transport.send_command_expect_same_prompt('show vlan brief', return_as_list=True)[:-1]


        # The reason this for loop is here is because instead of slicing off a predermined number of lines in output
        # I thought it better to begin capturing the output only after the line of dashes because I could see
        # the potential for  different firmware versions giving more or less lines of output before the VLANS
        output = []
        startflag = False
        for line in commandOutput:

            # captures the line of output only after there has been a line of dashes
            if startflag is True:
                output.append(line)

            # if there is a line of dashes we will begin capturing the output after the line of dashes
            if '----' in line:
                startflag = True

        # splits each line of output and only takes the first element (vlan number)
        output = [x.split()[0] for x in output]

        # returns output
        return output

    def mac_address_table(self):
        mac_table_list = []

        self.terminal_length()

        device_output = self.transport.send_command_expect_same_prompt('show mac address-table', buffer_size=200).splitlines()[1:][:-1]

        # This is needed as routers with a wic card require you to issue the command in priv exec mode with a dash in between
        # the words 'mac' and 'address'
        for line in device_output:
            if len(line) >= 1:
                if line[0] == '%':
                    self.priv_exec()
                    device_output = self.transport.send_command_expect_same_prompt('show mac-address-table', buffer_size=200).splitlines()[1:][:-1]
                    break
        flag = 0
        for line in device_output[:-1]:
            if len(line.split()) >= 4:
                if flag == 1:
                    tmp = line.strip('*').split()
                    mac_table_list.append(
                        {'vlan': tmp[0], 'mac':tmp[1], 'type': tmp[2], 'ports': tmp[-1]}
                    )
                    #mac_table_list.append(line.split())

            if len(line.split()) >= 1:
                if '--' in line.split()[0]:
                    flag = 1

        return mac_table_list

    def find_mac_address(self, mac_address, mac_table=None):
        if not mac_table:
            mac_table = self.mac_address_table()

        return [item for item in mac_table if item['mac'] == mac_address]

    def cdp_neighbor_table(self):

        '''

        :return: list of lists [hostname, remote device IP, local connected interface, remote connected interface]
        '''

        self.terminal_length()

        self.priv_exec()

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

            if 'ip address' in line.lower():
                try:
                    tmp['remoteip']
                except KeyError:
                    tmp['remoteip'] = line.split(':')[1].strip()

            if '-----' in line:
                data.append(tmp)
                tmp = {}

        return data

    def arp_table(self):

        self.terminal_length()

        output = []
        header = []
        flag = 0
        for line in self.transport.send_command_expect_same_prompt('show ip arp', return_as_list=True, buffer_size=40):
            if 'protocol' in line.lower() and 'address' in line.lower():
                header = line.split()
                flag += 1
                continue

            if flag == 1:
                if len(line.split()) == 6:
                    tmp = line.split()
                    output.append(
                        {'protocol': tmp[0], 'address': tmp[1], 'age': tmp[2], 'mac': tmp[3], 'type': tmp[4], 'interface': tmp[5]}
                    )
                elif flag > 1:
                    tmp = line.split()
                    output.append(
                        {'protocol': tmp[0], 'address': tmp[1], 'age': tmp[2], 'mac': tmp[3], 'type': tmp[4], 'interface': ''}
                    )

        return output

    def show_routes(self):

        self.terminal_length()

        routing_table = self.transport.send_command_expect_same_prompt('show ip route', return_as_list=True)
        flag = 0
        fixed_ouput = []
        tmp = ''
        # Sorts each line of the routing table, putting entries that belong together on the same line
        for line in routing_table:
            if len(line) <= 1:
                continue
            if 'last resort' in line:
                flag += 1

            if flag != 1:
                continue

            if line[0].isalpha() and line[1] == ' ':
                if tmp != '':
                    fixed_ouput.append(tmp)
                    tmp = ''
                tmp += line
            if line[0] == ' ' and 'subnetted' not in line:
                tmp += '| {}'.format(line)

        # Parses out data
        data = []
        for route in fixed_ouput:
            tmp = route.split()
            tmp_dict = {}
            codes = []
            for section in tmp:
                if section[0].isalpha():
                    codes.append(section)
                else:
                    network = section
                    break
            tmp_dict['codes'] = codes
            tmp_dict['subnet'] = network
            hoplist = []
            if 'directly' in route:
                td = {}
                td['nexthop'] = 'directly connected'
                td['nexthoplocation'] = route.split(',')[-1].strip()
                hoplist.append(td)
            else:
                tmp = route.split('|')
                td = {}
                for x in tmp:
                    try:
                        print(x.split('via'))
                        td['nexthop'] = x.split('via')[1].split(',')[0].strip()
                        td['nexthoplocation'] = x.split('via')[1].split(',')[-1].strip()
                        hoplist.append(td)
                    except IndexError:
                        continue
            tmp_dict['nexthops'] = hoplist
            data.append(tmp_dict)
        return data

    def show_interface_status(self):

        output = ''

        self.terminal_length()

        switch_output = self.transport.send_command_expect_same_prompt('show interfaces status', return_as_list=True)[1:]
        data = []
        for line in switch_output:
            if len(line.split()) <= 1:
                continue

            if 'Duplex' in line and 'Speed' in line:
                continue

            if 'notconnect' in line:
                data.append({'interface': line.split()[0], 'status': 'notconnected'})
            elif 'disabled' in line:
                data.append({'interface': line.split()[0], 'status': 'disabled'})
            else:
                data.append({'interface': line.split()[0], 'status': 'connected'})
        return data

    def show_interface_description(self):
        '''
        Issues 'show interface description' on device, then parses the output creating a list of lists that the
        nested lists contain the first, second, third, and 4th columns of the output of the command, this allows
        for a programmer to easily interface with the data returned and not have to parse it theirselves
        :return: List of Lists that consists of the output of the command
        '''

        self.terminal_length()

        masterlist = []

        for line in self.transport.send_command_expect_same_prompt('show interface description', return_as_list=True, buffer_size=200)[2:][:-1]:
            line = line.split()
            if len(line) < 3:
                continue

            # If the line is down with no description
            if len(line) == 3:
                masterlist.append([line[0], line[1], line[2], ''])

            else:
                # if 'admin' is in the second column of the entry (as in 'admin down')
                if line[1].lower() == 'admin':

                    # if there is a description
                    if len(line) > 4:
                        masterlist.append([line[0], '{} {}'.format(line[1], line[2]), line[3],
                                           ' '.join([i for i in line[4:]]).strip("'").strip('"')])
                    # if theres not a description
                    else:
                        masterlist.append([line[0], '{} {}'.format(line[1], line[2]), line[3], ''])

                # else 'admin' is NOT in the second column of the entry (as in the interface is admin up but down cause its unplugged)
                else:
                    masterlist.append(
                        [line[0], line[1], line[2], ' '.join([i for i in line[3:]])])

        return masterlist

    def show_configured_syslog_server(self):
        '''Returns the value configured for syslog

        :return:
        '''
        runningConfig = self.show_run()

        servers = []
        for line in runningConfig.splitlines():
            if len(line.split()) > 0:
                if line.split()[0] == 'logging' and line.split()[1] == 'host':
                    servers.append(line.split()[-1:][0])

        return servers

    def show_vlan(self):
        def gather_description(line):
            if line.split()[2] == 'active':
                return line.split()[1]
            else:
                return None

        def gather_vlan(line):
            return line.split()[0]

        def gather_interfaces(line):
            if line.split()[2] == 'active':
                return [x.strip(',') for x in line.split()[3:]]
            else:
                return [x.strip(',') for x in line.split()[2:]]

        # sets terminal length and width
        self.terminal_length()
        self.terminal_width()

        # grabs output of show vlan command
        data = self.transport.send_command_expect_same_prompt('show vlan', return_as_list=True, buffer_size=200)[2:][:-1]
        flag = 0
        returnable_data = []


        for x in data:
            # parses out all of the unneeded data
            if '--' in x:
                flag += 1
                continue
            if flag == 1:
                if len(x.split()) == 0:
                    continue
                elif x.split()[0].lower() == 'vlan':
                    continue
                elif 'act/unsup' in x.split()[-1].lower():
                    continue
                else:  # formats the needed data into a dictionary
                    returnable_data.append({'vlan': gather_vlan(x), 'description': gather_description(x), 'interfaces': gather_interfaces(x)})

        return returnable_data

    def shutdown_interface(self, interface):
        self.config_t()
        self.transport.send_command_expect_different_prompt('interface {}'.format(interface))
        self.transport.send_command_expect_same_prompt('shutdown')
        self.transport.send_command_expect_different_prompt('exit')

    def no_shutdown_interface(self, interface):
        self.config_t()
        self.transport.send_command_expect_different_prompt('interface {}'.format(interface))
        self.transport.send_command_expect_same_prompt('no shutdown')
        self.transport.send_command_expect_different_prompt('exit')

    def set_access_vlan_on_interface(self, interface, vlan_number):
        configured_vlans = [x['vlan'] for x in self.show_vlan()]
        if vlan_number not in configured_vlans:
            raise AttributeError('Vlan {} is not configured on the switch!'.format(vlan_number))
        self.config_t()
        self.transport.send_command_expect_different_prompt('interface {}'.format(interface))
        self.transport.send_command_expect_same_prompt('switchport access vlan {}'.format(vlan_number))
        self.transport.send_command_expect_different_prompt('exit')

    def show_inventory_data(self):
        self.terminal_width()
        self.terminal_length()
        output = self.transport.send_command_expect_same_prompt('show inventory raw', return_as_list=True)

        data = []
        tmp = ''
        # for loop takes the 2 lines of each output and combines them to one line, storing them in a list split
        # by each entry seperated by comma
        for line in output:
            if len(line) == 0:
                data.append(tmp[:-2].split(','))
                tmp = ''
                continue
            tmp += '{}, '.format(line)

        final_data = []
        for x in data[1:][:-1]:
            tmp_dict = {}
            for entry in x:
                tmp = entry.split(':')
                tmp_dict[tmp[0].lower().strip()] = tmp[1].strip().strip('"')
            final_data.append(tmp_dict)

        return final_data

    def show_hsrp_info(self):

        self.terminal_length()

        data = self.transport.send_command_expect_same_prompt('show standby brief', return_as_list=True)
        if len(data) == 2:
            raise NotConfigured('HSRP has not been configured! on the device!')
        user_data = []
        flag = False
        for line in data:
            if 'interface' in line.lower():
                flag = True
                continue
            if flag == True:
                x = line.split()

                if len(x) < 7:
                    # prevents any line from being interpreted if it has less than 7 columns
                    continue

                if len(x) == 7:
                    linedict = {'interface': x[0], 'group': x[1], 'priority': x[2], 'preempt': 'not configured', 'state': x[3],
                                'activerouter': x[4], 'standbyrouter': x[5], 'virtualip': x[6]}
                else:
                    linedict = {'interface': x[0], 'group': x[1], 'priority': x[2], 'preempt': 'configured', 'state': x[4],
                                'activerouter': x[5], 'standbyrouter': x[6], 'virtualip': x[7]}
                user_data.append(linedict)

        return user_data

    def write_mem(self):
        if '#' not in self.transport.prompt:
            self.priv_exec()

        self.check_and_exit_config_t()

        self.transport.send_command('copy run start\n')
        time.sleep(.2)
        self.transport.send_command('')  # sends a return key

        return self.transport.get_output()


class IOSConfigMethods(CommandConfigMethods, TerminalCommands):

    def __init__(self, transport_object):
        TerminalCommands.__init__(self, transport_object)

    def configure_description(self, interface, description):
        output = ''


        output += self.priv_exec()

        output += self.config_t()

        output += self.transport.send_command_expect_different_prompt('interface {}'.format(interface))

        output += self.transport.send_command_expect_same_prompt('description {}'.format(description))

        output += self.send_end()

        return output

    def configure_access_vlan(self, interface, vlan):
        '''
        this method should be used when the user needs to configure an interface as an access port on a specific vlan
        :param interface: interface to configure ex. gi1/0/1, fa0/1, etc.
        :param vlan: Vlan number to configure
        :return: commands sent to server and their output
        '''
        output = ''

        # get the terminal orientated where it needs to be to issue the commands
        #output += self.priv_exec()
        output += self.config_t()

        # issues commands to configure the interface specified as an access vlan on the vlan specified
        output += self.transport.send_command_expect_different_prompt('interface {}'.format(interface))
        output += self.transport.send_command_expect_same_prompt('switchport mode access')
        output += self.transport.send_command_expect_same_prompt('switchport access vlan {}'.format(vlan))

        output += self.send_end()


        return output

    def delete_local_user(self, username):
        output = ''

        output += self.config_t()

        output += self.transport.send_command_expect_same_prompt('no username {}'.format(username))

        self.send_end()

        return output
