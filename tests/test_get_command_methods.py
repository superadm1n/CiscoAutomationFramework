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
        ''''''
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
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.show_interfaces
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.physical_port_inventory_longname()
        self.assertEqual(['Ethernet1/48'], t)


class port_status(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_interface_status
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.port_status()

        self.assertEqual(
            {'port': 'Gi1/0/2', 'vlan': '400', 'name': 'exampledescrip', 'speed': 'auto', 'type': '10/100/1000BaseTX', 'status': 'notconnect', 'duplex': 'auto'}, t[1])
        self.assertEqual(
            {'port': 'Gi1/0/18', 'vlan': 'connected', 'name': 'To switch', 'speed': 'a-full', 'type': 'a-100', 'status': 'switch', 'duplex': 'trunk'}, t[-1])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_interface_status
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.port_status()
        self.assertEqual(
            {'port': 'Gi1/0/2', 'vlan': '400', 'name': 'exampledescrip', 'speed': 'auto', 'type': '10/100/1000BaseTX', 'status': 'notconnect', 'duplex': 'auto'}, t[1])
        self.assertEqual(
            {'port': 'Gi1/0/18', 'vlan': 'connected', 'name': 'To switch', 'speed': 'a-full', 'type': 'a-100', 'status': 'switch', 'duplex': 'trunk'}, t[-1])

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.port_status()


class power_inline(TestCase):
    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_power_inline
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.power_inline()
        self.assertEqual({'admin': 'auto', 'class': '1', 'max': '30.0', 'oper': 'on', 'watts': '4.0', 'interface': 'Gi1/0/1', 'device': 'Ieee PD'}, t[0])
        self.assertEqual({'interface': 'Gi1/0/42', 'oper': 'off', 'max': '30.0', 'watts': '0.0', 'admin': 'auto', 'device': 'n/a', 'class': 'n/a'}, t[2])
        self.assertEqual({'interface': 'Gi1/0/43', 'oper': 'on', 'max': '30.0', 'watts': '30.0', 'admin': 'auto', 'device': 'AIR-AP3802I-B-K9', 'class': '4'}, t[3])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_power_inline
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.power_inline()
        self.assertEqual(
            {'watts': '0.0', 'device': 'n/a', 'max': '60.0', 'admin': 'auto', 'class': 'n/a', 'oper': 'off', 'interface': 'Gi1/0/1'},
            t[0]
        )
        self.assertEqual(
            {'admin': 'auto', 'interface': 'Gi1/0/11', 'max': '60.0', 'watts': '4.0', 'class': '1', 'device': 'Ieee PD', 'oper': 'on'},
            t[10]
        )
        self.assertEqual(
            {'admin': 'auto', 'interface': 'Gi2/0/40', 'max': '60.0', 'watts': '30.0', 'class': '4', 'device': 'AIR-AP3802I-B-K9', 'oper': 'on'},
            t[-8]
        )

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.power_inline()



class list_ospf_configuration(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_two = long_ios_responses.ospf_runing_config
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.list_ospf_configuration()
        self.assertIn('network 2.2.2.2 0.0.0.0 area 25', t)
        self.assertIn('router ospf 2', t)
        self.assertIn('router ospf 1', t)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_two = long_iosxe_responses.ospf_runing_config
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.list_ospf_configuration()
        self.assertIn('network 2.2.2.2 0.0.0.0 area 25', t)
        self.assertIn('router ospf 2', t)
        self.assertIn('router ospf 1', t)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.ospf_running_config
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.list_ospf_configuration()
        self.assertIn('router ospf 1', t)
        self.assertIn('router-id 10.255.242.4', t)
        self.assertIn('network 10.1.10.0/23 area 0.0.0.0', t)
        self.assertNotIn('router eigrp 100', t)



class list_eigrp_configuration(TestCase):
    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_two = long_ios_responses.ospf_runing_config
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.list_eigrp_configuration()
        self.assertIn('router eigrp 1', t)
        self.assertIn('eigrp stub connected summary', t)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_two = long_iosxe_responses.ospf_runing_config
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.list_eigrp_configuration()
        self.assertIn('router eigrp 1', t)
        self.assertIn('eigrp stub connected summary', t)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.ospf_running_config
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.list_eigrp_configuration()
        self.assertIn('router eigrp 100', t)
        self.assertIn('distance 100 100', t)


class list_down_ports(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_interface_description
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.list_down_ports()
        ports = ['Gi1/0/2', 'Gi1/0/4', 'Gi1/0/5', 'Gi1/0/6', 'Gi1/0/8', 'Gi1/0/10', 'Gi1/0/12', 'Gi1/0/13', 'Gi1/0/14', 'Gi1/0/16']
        self.assertEqual(t, ports)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_interface_description
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.list_down_ports()
        ports = ['Gi1/0/2', 'Gi1/0/4', 'Gi1/0/5', 'Gi1/0/6', 'Gi1/0/8', 'Gi1/0/10', 'Gi1/0/12', 'Gi1/0/13', 'Gi1/0/14', 'Gi1/0/16']
        self.assertEqual(t, ports)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.show_interface_status
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.list_down_ports()
        self.assertEqual(['Eth2/17'], t)


class last_input_and_output(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_interface_1
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.last_input_and_output('gi1/0/1')
        self.assertEqual(['gi1/0/1', '00:00:17', '00:00:00'], t)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_interface_1
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.last_input_and_output('gi1/0/2')
        self.assertEqual(['gi1/0/2', '00:00:01', 'never'], t)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.last_input_and_output('gi1/0/2')



class last_input_and_output_all(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_interfaces
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.last_input_and_output_all()
        self.assertEqual({'output': '00:00:01', 'input': '00:09:20', 'interface': 'GigabitEthernet1/0/1'}, t[-1])
        self.assertEqual({'output': '00:00:00', 'input': '00:00:00', 'interface': 'Vlan2100'}, t[0])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_interfaces
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.last_input_and_output_all()
        self.assertEqual({'input': '00:00:00', 'output': '00:00:00', 'interface': 'Vlan2100'}, t[0])
        self.assertEqual({'input': '00:09:20', 'output': '00:00:01', 'interface': 'GigabitEthernet1/0/1'}, t[-1])

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'

        # To catch the exception properly it needs to be contained in a wrapper, explained at the link below
        # https://ongspxm.github.io/blog/2016/11/assertraises-testing-for-errors-in-unittest/
        with self.assertRaises(CustomExceptions.MethodNotImplemented):
            ssh_obj.last_input_and_output_all()


class list_configured_vlans(TestCase):
    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_vlan_brief
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.list_configured_vlans()
        expectedOutput = ['1', '400', '410', '600', '601', '912', '950', '1002', '1003', '1004', '1005']
        self.assertEqual(expectedOutput, t)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_vlan_brief
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.list_configured_vlans()
        expectedOutput = ['1', '400', '410', '600', '601', '912', '950', '1002', '1003', '1004', '1005']
        self.assertEqual(expectedOutput, t)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        ssh.response_four = long_nxos_responses.show_vlan_brief
        t = ssh_obj.list_configured_vlans()
        expectedOutput = ['1', '16', '25']
        self.assertEqual(expectedOutput, t)


class mac_address_table(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.mac_address_table
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.mac_address_table()
        self.assertEqual({'vlan': 'All', 'type': 'STATIC', 'ports': 'CPU', 'mac': 'aaaa.aaaa.aaaa'}, t[0])
        self.assertEqual({'mac': 'iiii.iiii.iiii', 'ports': 'Po1', 'type': 'DYNAMIC', 'vlan': '1'}, t[-1])

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.mac_address_table
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.mac_address_table()
        self.assertEqual({'vlan': 'All', 'type': 'STATIC', 'ports': 'CPU', 'mac': 'aaaa.aaaa.aaaa'}, t[0])
        self.assertEqual({'mac': 'iiii.iiii.iiii', 'ports': 'Po1', 'type': 'DYNAMIC', 'vlan': '1'}, t[-1])

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        ssh.response_four = long_nxos_responses.mac_address_table
        t = ssh_obj.mac_address_table()
        self.assertEqual({'mac': 'aaaa.aaaa.aaaa', 'vlan': '1', 'type': 'static', 'ports': 'sup-eth1(R)'}, t[0])
        self.assertEqual({'mac': 'eeee.eeee.eeee', 'vlan': '2499', 'type': 'dynamic', 'ports': 'Po11'}, t[-1])


class find_mac_address(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.mac_address_table
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.find_mac_address('aaaa.aaaa.aaaa')
        self.assertEqual([{'type': 'STATIC', 'vlan': 'All', 'mac': 'aaaa.aaaa.aaaa', 'ports': 'CPU'}], t)

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.mac_address_table
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.find_mac_address('aaaa.aaaa.aaaa')
        self.assertEqual([{'type': 'STATIC', 'vlan': 'All', 'mac': 'aaaa.aaaa.aaaa', 'ports': 'CPU'}], t)

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        ssh.response_four = long_nxos_responses.mac_address_table
        t = ssh_obj.find_mac_address('aaaa.aaaa.aaaa')
        self.assertEqual([{'mac': 'aaaa.aaaa.aaaa', 'vlan': '1', 'type': 'static', 'ports': 'sup-eth1(R)'}], t)



class cdp_neighbor_table(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_two = long_ios_responses.cdp_neighbor_detail
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.cdp_neighbor_table()
        self.assertEqual(
            {'deviceid': 'dev1', 'remoteip': '1.1.1.1', 'remoteinterface': 'GigabitEthernet1/1/4', 'localinterface': 'GigabitEthernet1/1/1',
             'platform': 'cisco WS-C3750X-48P'}, t[0]
        )
        self.assertEqual(
            {'deviceid': 'dev2', 'remoteip': '2.2.2.2', 'remoteinterface': 'GigabitEthernet0', 'localinterface': 'GigabitEthernet1/0/44',
             'platform': 'cisco AIR-AP3802I-B-K9'}, t[1]
        )

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_two = long_iosxe_responses.cdp_neighbor_detail
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.cdp_neighbor_table()
        self.assertEqual(
            {'deviceid': 'dev1', 'remoteip': '1.1.1.1', 'remoteinterface': 'GigabitEthernet1/1/4', 'localinterface': 'GigabitEthernet1/1/1',
             'platform': 'cisco WS-C3750X-48P'}, t[0]
        )
        self.assertEqual(
            {'deviceid': 'dev2', 'remoteip': '2.2.2.2', 'remoteinterface': 'GigabitEthernet0', 'localinterface': 'GigabitEthernet1/0/44',
             'platform': 'cisco AIR-AP3802I-B-K9'}, t[1]
        )

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = long_iosxe_responses.cdp_neighbor_detail
        ssh_obj = factory(ssh, NXOS)
        ssh_obj.roles = 'vdc-admin'
        t = ssh_obj.cdp_neighbor_table()
        self.assertEqual(
            {'remoteinterface': 'GigabitEthernet1/1/4', 'platform': 'cisco WS-C3750X-48P', 'localinterface': 'GigabitEthernet1/1/1',
             'deviceid': 'dev1'}, t[0]
        )
        self.assertEqual(
            {'remoteinterface': 'GigabitEthernet0', 'platform': 'cisco AIR-AP3802I-B-K9', 'localinterface': 'GigabitEthernet1/0/44',
             'deviceid': 'dev2'}, t[1]
        )


class arp_table(TestCase):

    def test_ios(self):
        ''''''
        ssh = TestingSSHEngine()
        ssh.response_one = long_ios_responses.show_ip_arp
        ssh_obj = factory(ssh, IOS)
        t = ssh_obj.arp_table()
        self.assertEqual(
            {'protocol': 'Internet', 'type': 'ARPA', 'age': '99', 'address': '2.2.2.2', 'mac': 'aaaa.aaaa.aaaa', 'interface': 'Vlan1'},
            t[0]
        )
        self.assertEqual(
            {'protocol': 'Internet', 'type': 'ARPA', 'age': '0', 'address': '7.7.7.7', 'mac': 'ffff.ffff.ffff', 'interface': 'Vlan1'},
            t[-1]
        )

    def test_iosXE(self):
        ssh = TestingSSHEngine()
        ssh.response_one = long_iosxe_responses.show_ip_arp
        ssh_obj = factory(ssh, IOSXE)
        t = ssh_obj.arp_table()
        self.assertEqual(
            {'protocol': 'Internet', 'type': 'ARPA', 'age': '99', 'address': '2.2.2.2', 'mac': 'aaaa.aaaa.aaaa', 'interface': 'Vlan1'},
            t[0]
        )
        self.assertEqual(
            {'protocol': 'Internet', 'type': 'ARPA', 'age': '0', 'address': '7.7.7.7', 'mac': 'ffff.ffff.ffff', 'interface': 'Vlan1'},
            t[-1]
        )

    def test_NXOS(self):
        ssh = TestingSSHEngine()
        ssh.response_four = long_nxos_responses.show_ip_arp
        ssh_obj = factory(ssh, NXOS)
        t = ssh_obj.arp_table()
        self.assertEqual(
            {'address': '1.1.1.1', 'mac': 'aaaa.aaaa.aaaa', 'interface': 'Ethernet1/2', 'type': False, 'age': '00:13:32', 'protocol': None},
            t[0]
        )
        self.assertEqual(
            {'address': '8.8.8.8', 'mac': 'hhhh.hhhh.hhhh', 'interface': 'Ethernet1/14', 'type': False, 'age': '00:04:20', 'protocol': None},
            t[-1]
        )

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