from unittest import TestCase
from CiscoAutomationFramework.IOS import IOS
from CiscoAutomationFramework.Exceptions import EnablePasswordError
from tests.test_ios.Engines import IdealNoDelayGetOutput


class TestUptime(TestCase):

    def setUp(self) -> None:
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname#')
        engine.load_canned_response('terminal length 0\nmyhostname#')
        engine.load_canned_response('show version\nmyhostname uptime is 5 days, 13 hours, 17 minutes\nmyhostname#')
        self.ssh = IOS(engine)

    def test_sends_correct_commands(self):
        expected = ['terminal length 0', 'show version']
        _ = self.ssh.uptime
        self.assertEqual(expected, self.ssh.transport.all_commands_sent)

    def test_extracts_uptime(self):
        self.assertEqual('5 days, 13 hours, 17 minutes', self.ssh.uptime)

    def test_raises_exception_if_no_enable_password_and_not_in_priv_exec(self):
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname>')
        engine.load_canned_response('terminal length 0\nmyhostname>')
        engine.load_canned_response('enable\n')
        engine.load_canned_response('show version\nmyhostname uptime is 5 days, 13 hours, 17 minutes\nmyhostname>')
        ssh = IOS(engine)
        # need to wrap in a function so it can be called by assertRaises
        def wrap():
            _ = ssh.uptime
        self.assertRaises(EnablePasswordError, wrap)

class TestInterfaces(TestCase):

    def setUp(self) -> None:
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname#')
        engine.load_canned_response('terminal length 0\nmyhostname#')
        engine.load_canned_response('show interfaces\nline1\nline2\nline3\nline4\nmyhostname#')
        self.ssh = IOS(engine)

    def test_sends_correct_commands(self):
        expected = ['terminal length 0', 'show interfaces']
        _ = self.ssh.interfaces
        self.assertEqual(expected, self.ssh.transport.all_commands_sent)

    def test_omits_command_issued_in_output(self):
        self.assertNotIn('show interfaces', ''.join(self.ssh.interfaces))

    def test_omits_first_line_after_command_issued_in_output(self):
        self.assertNotIn('line1', ''.join(self.ssh.interfaces))

    def test_omits_prompt_in_output(self):
        self.assertNotIn('myhostname#', ''.join(self.ssh.interfaces))

    def test_omits_line_before_prompt_in_output(self):
        self.assertNotIn('line4', ''.join(self.ssh.interfaces))

    def test_raises_exception_if_no_enable_password_and_not_in_priv_exec(self):
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname>')
        engine.load_canned_response('terminal length 0\nmyhostname>')
        engine.load_canned_response('enable\n')
        engine.load_canned_response('show interfaces\nline1\nline2\nline3\nline4\nmyhostname>')
        ssh = IOS(engine)

        # need to wrap in a function so it can be called by assertRaises
        def wrap():
            _ = ssh.interfaces

        self.assertRaises(EnablePasswordError, wrap)
