import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
from tests.test_Transport_Engines.Base import TestableSSHEngine
from unittest import TestCase

resp1 = '''
*********************
*********************
WARNING:  This system is for the use of authorized clients only.
Individuals using the computer network system without authorization,
or in excess of their authorization, are subject to having all their
activity on this computer network system monitored and recorded by
system personnel.  To protect the computer network system from
unauthorized use and to ensure the computer network system is
functioning properly, system administrators monitor this system.
Anyone using this computer network system expressly consents to such
monitoring and is advised that if such monitoring reveals possible
conduct of criminal activity, system personnel may provide the
evidence of such activity to law enforcement officer.
Access is restricted to authorized users only.  Unauthorized access
is a violation of state and federal, civil and criminal laws.
===========================================
===========================================

BMH-ED-SW2#
'''
resp2 = ['welcome to the switch', 'you are in', 'switch#']

# class TestConnectToServer(TestCase):
#
#     def test_successful_connection(self):
#         ssh = TestableSSHEngine(resp1)
#         t = ssh.connect_to_server('192.168.10.1', 'user', 'password')
#         self.assertEqual('Connection Successful', t)
#
#
#     def test_successful_connection_2(self):
#         ssh = TestableSSHEngine(['1#', '2#'])
#         t = ssh.connect_to_server('192.168.10.1', 'user', 'password')
#         self.assertEqual('Connection Successful', t)
#
#     def test_send_command(self):
#         ssh = TestableSSHEngine(['%'])
#         t = ssh.send_command('my bad command')
#         print(t)

