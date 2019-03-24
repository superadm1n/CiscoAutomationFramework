import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
from .Base import TestableSSHEngine
from unittest import TestCase

class TestConnectToServer(TestCase):

    def test_successful_connection(self):
        ssh = TestableSSHEngine(['1#', '2#'])
        t = ssh.connect_to_server('192.168.10.1', 'user', 'password')
        self.assertEqual('Connection Successful', t)


