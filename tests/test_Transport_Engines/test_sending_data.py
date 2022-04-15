from unittest import TestCase
from tests.test_Transport_Engines.Engines import TestableSendCommand
from os import listdir
from os.path import isfile, join
from pathlib import Path
from time import perf_counter
import random


class TestSendingData(TestCase):


    def test_default_ending_is_newline(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command')
        self.assertEqual(ssh.unit_test_tracker_commands_sent[0], ('my_command', '\n'))

    def test_tracks_commands_sent(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command1')
        ssh.send_command('my_command2')
        ssh.send_command('my_command3')
        expected_tracking_list = ['my_command1', 'my_command2', 'my_command3']
        self.assertEqual(expected_tracking_list, ssh.all_commands_sent)

    def test_allows_ending_modification(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command1', end='\r')
        sent_command = ''.join(ssh.unit_test_tracker_commands_sent[0])
        self.assertEqual('my_command1\r', sent_command)

    def test_keeps_track_commands_after_output_get(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command1')
        ssh.send_command('my_command2')
        ssh.send_command('my_command3')
        expected_tracking_list = ['my_command1', 'my_command2', 'my_command3']
        ssh.get_output(timeout=.001)
        self.assertEqual(expected_tracking_list, ssh.all_commands_sent)

    def test_tracks_num_commands_sent_before_output_get(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command1')
        ssh.send_command('my_command2')
        ssh.send_command('my_command3')
        self.assertEqual(3, ssh.commands_sent_since_last_output_get)

    def test_clears_num_commands_sent_after_output_get(self):
        ssh = TestableSendCommand()
        ssh.send_command('my_command1')
        ssh.send_command('my_command2')
        ssh.send_command('my_command3')
        ssh.get_output(timeout=.001)
        self.assertEqual(0, ssh.commands_sent_since_last_output_get)

