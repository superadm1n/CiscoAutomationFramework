import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
from Base import TestingSSHEngine, factory
import long_nxos_responses, long_ios_responses, long_iosxe_responses
from unittest import TestCase

from CiscoAutomationFramework import IOS, IOSXE, NXOS, ASA, CustomExceptions


class test_get_uptime(TestCase):

    def test_ios(self):
        ssh = TestingSSHEngine()
        ssh.response_one = 'blah\nblah\ntest_sw 1day_stuff uptime\nblah\nblah'
        ssh_obj = factory(ssh, IOS)
        self.assertEqual('test_sw 1day_stuff uptime', ssh_obj.get_uptime())
        #print(self.ssh_obj.get_uptime())

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = 'blah\nblah\ntest_sw 1day_stuff uptime\nblah\nblah'
        ssh_obj = factory(ssh, IOSXE)
        self.assertEqual('test_sw 1day_stuff uptime', ssh_obj.get_uptime())

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = 'blah\nblah\nkernel uptime is 15251\nblah\nblah'
        ssh_obj = factory(ssh, NXOS)
        self.assertEqual(' kernel uptime is 15251', ssh_obj.get_uptime())


class get_local_users(TestCase):

    def test_ios(self):
        '''Tests logging in, setting terminal length, then getting running config'''
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nusername me password badpass\nblah\nblah'
        ssh_obj = factory(ssh, IOS)
        self.assertEqual(['me'], ssh_obj.get_local_users())

    def test_ios_multiple_users(self):
        '''Tests logging in, setting terminal length, then getting running config'''
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nusername me password badpass\nusername you password badpass\nblah'
        ssh_obj = factory(ssh, IOS)
        self.assertEqual(['me', 'you'], ssh_obj.get_local_users())

    def test_ios_no_users(self):
        '''Tests logging in, setting terminal length, then getting running config'''
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nblah\nblah\nblah'
        ssh_obj = factory(ssh, IOS)
        self.assertEqual([], ssh_obj.get_local_users())

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nusername me password badpass\nblah\nblah'
        ssh_obj = factory(ssh, IOSXE)
        self.assertEqual(['me'], ssh_obj.get_local_users())

    def test_iosXE_multiple_users(self):
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nusername me password badpass\nusername you password badpass\nblah'
        ssh_obj = factory(ssh, IOSXE)
        self.assertEqual(['me', 'you'], ssh_obj.get_local_users())

    def test_iosXE_no_users(self):
        ssh = TestingSSHEngine()
        ssh.response_two = 'blah\nblah\nblah\nblah\nblah'
        ssh_obj = factory(ssh, IOSXE)
        self.assertEqual([], ssh_obj.get_local_users())

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\n\n\n\n\n\n\nblah\nblah\nusername me password badpass\nblah\nblah\n\n\n\n\n\n\n\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.get_local_users()
        self.assertEqual(['me'], t)

    def test_NXOS_multiple_users(self):
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\n\n\n\n\n\n\nblah\nblah\nusername me password badpass\nusername you password badpass\nblah\n\n\n\n\n\n\n\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.get_local_users()
        self.assertEqual(['me', 'you'], t)

    def test_NXOS_no_users(self):
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\n\n\n\n\n\n\nblah\nblah\nblah\nblah\nblah\n\n\n\n\n\n\n\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.get_local_users()
        self.assertEqual([], t)

class show_run_interface(TestCase):

    def test_ios(self):
        '''Tests that the proper data is returned from the function and that the proper command is ran on the device'''
        ssh = TestingSSHEngine()
        ssh.response_two = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.show_run_interface('fa1/0/1')
        self.assertEqual('interface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n', t)
        self.assertEqual(ssh_obj.transport.commands_ran[-1], 'show running-config interface fa1/0/1')

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_two = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.show_run_interface('fa1/0/1')
        self.assertEqual('interface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n', t)
        self.assertEqual(ssh_obj.transport.commands_ran[-1], 'show running-config interface fa1/0/1')

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.show_run_interface('fa1/0/1')



class power_cycle_port(TestCase):
    pass





class physical_port_inventory(TestCase):

    def test_ios(self):
        '''Tests that the proper data is returned from the function and that the proper command is ran on the device'''
        ssh = TestingSSHEngine()
        ssh.response_one = '''show int desc
        Interface                      Status         Protocol Description
        Vl1                            admin down     down
        Vl2100                         up             up
        Fa0                            admin down     down
        Gi1/0/1                        up             up   
        Gi1/0/2                        up             up   
        Gi1/0/3                        up             up
        Gi1/0/4                        down           down 
        Gi1/0/5                        down           down
        \n\n\n\n'''
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.physical_port_inventory()
        self.assertEqual(['Fa0', 'Gi1/0/1', 'Gi1/0/2', 'Gi1/0/3', 'Gi1/0/4', 'Gi1/0/5'], t)
        self.assertEqual(ssh_obj.transport.commands_ran, ['terminal length 0', 'show interface description'])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = '''show int desc
        Interface                      Status         Protocol Description
        Vl1                            admin down     down
        Vl2100                         up             up
        Fa0                            admin down     down
        Gi1/0/1                        up             up   
        Gi1/0/2                        up             up   
        Gi1/0/3                        up             up
        Gi1/0/4                        down           down 
        Gi1/0/5                        down           down
        \n\n\n\n'''
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.physical_port_inventory()
        self.assertEqual(['Fa0', 'Gi1/0/1', 'Gi1/0/2', 'Gi1/0/3', 'Gi1/0/4', 'Gi1/0/5'], t)
        self.assertEqual(ssh_obj.transport.commands_ran, ['terminal length 0', 'show interface description'])


    def test_NXOS(self):
        '''Tests that port channel and vlans are excluded but it still includes the physical interfaces'''
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.show_interfaces
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.physical_port_inventory()
        self.assertEqual(['Eth1/48'], t)




class physical_port_inventory_longname(TestCase):

    def test_ios(self):
        '''Tests that the proper data is returned from the function and that the proper command is ran on the device'''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_interfaces
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.physical_port_inventory_longname()
        self.assertEqual(['FastEthernet0', 'GigabitEthernet1/0/1'], t)
        #self.assertEqual(ssh_obj.transport.commands_ran, ['terminal length 0', 'show interface description'])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_interfaces
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.physical_port_inventory_longname()
        self.assertEqual(['FastEthernet0', 'GigabitEthernet1/0/1'], t)

    def test_NXOS(self):
        '''Tests that port channel and vlans are excluded but it still includes the physical interfaces'''
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.show_interfaces
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.physical_port_inventory_longname()
        self.assertEqual(['Ethernet1/48'], t)


class port_status(TestCase):
    pass


class power_inline(TestCase):
    pass


class list_ospf_configuration(TestCase):
    pass


class list_eigrp_configuration(TestCase):
    pass


class list_down_ports(TestCase):
    pass


class last_input_and_output(TestCase):
    pass


class last_input_and_output_all(TestCase):
    pass


class list_configured_vlans(TestCase):
    pass


class global_last_input_and_output(TestCase):
    pass


class mac_address_table(TestCase):
    pass


class find_mac_address(TestCase):
    pass


class cdp_neighbor_table(TestCase):
    pass


class arp_table(TestCase):
    pass


class show_routes(TestCase):
    pass


class show_interface_status(TestCase):
    pass


class show_interface_description(TestCase):
    pass


class show_configured_syslog_server(TestCase):
    pass


class show_vlan(TestCase):
    pass


class shutdown_interface(TestCase):
    pass


class no_shutdown_interface(TestCase):
    pass


class set_access_vlan_on_interface(TestCase):
    pass


class show_inventory_data(TestCase):
    pass


class show_hsrp_info(TestCase):
    pass


class write_mem(TestCase):
    pass


class configure_router_lan_subint(TestCase):
    pass

class delete_local_user(TestCase):

    def test_ios(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.config.delete_local_user('testuser')
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])
        self.assertEqual('no username testuser', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-3])

    def test_iosXE(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.config.delete_local_user('testuser')
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])
        self.assertEqual('', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('no username testuser', ssh_obj.transport.commands_ran[-3])
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-4])

    def test_NXOS(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.config.delete_local_user('testuser')



class configure_access_vlan(TestCase):

    def test_ios(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.config.configure_access_vlan('fa1/0/1', '400')
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-5])
        self.assertEqual('interface fa1/0/1', ssh_obj.transport.commands_ran[-4])
        self.assertEqual('switchport mode access', ssh_obj.transport.commands_ran[-3])
        self.assertEqual('switchport access vlan 400', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])

    def test_iosXE(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.config.configure_access_vlan('fa1/0/1', '400')
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-5])
        self.assertEqual('interface fa1/0/1', ssh_obj.transport.commands_ran[-4])
        self.assertEqual('switchport mode access', ssh_obj.transport.commands_ran[-3])
        self.assertEqual('switchport access vlan 400', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])

    def test_NXOS(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.config.configure_access_vlan('fa1/0/1', '400')



class configure_description(TestCase):

    def test_ios(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.config.configure_description('fa1/0/1', 'mydescription')
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-4])
        self.assertEqual('interface fa1/0/1', ssh_obj.transport.commands_ran[-3])
        self.assertEqual('description mydescription', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])

    def test_iosXE(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.config.configure_description('fa1/0/1', 'mydescription')
        self.assertEqual('configure terminal', ssh_obj.transport.commands_ran[-4])
        self.assertEqual('interface fa1/0/1', ssh_obj.transport.commands_ran[-3])
        self.assertEqual('description mydescription', ssh_obj.transport.commands_ran[-2])
        self.assertEqual('end', ssh_obj.transport.commands_ran[-1])

    def test_NXOS(self):
        '''Tests that the proper commands are run to configure a description on a specified interface'''
        ssh = TestingSSHEngine()
        ssh.response_four = '\n\ninterface FastEthernet 1/0/1\nswitchport mode access\nswitchport access vlan 10\n!\n\n\n'
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.config.configure_description('fa1/0/1', 'mydescription')