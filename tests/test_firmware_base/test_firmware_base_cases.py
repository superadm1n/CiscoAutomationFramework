from unittest import TestCase
from tests.test_firmware_base.Engines import IdealNoDelayGetOutput
from CiscoAutomationFramework.IOS import IOS
from CiscoAutomationFramework.Exceptions import EnablePasswordError

"""
It is important to note that even tho we are using the IOS object to instantiate here, that is just
because we need an object that is gaurinteed to have the proper abstract methods defined.
In none of these tests will we be running anything that is defined in the IOS class. Instead
we will be running and testing the methods that are defined in the abstract CiscoFirmware base class.
"""


class BaseTest(TestCase):

    @property
    def engine_at_std_user_prompt(self):
        ssh = IdealNoDelayGetOutput('myhostname', 'myhostname>')
        return IOS(ssh)

    @property
    def engine_at_priv_exec_prompt(self):
        ssh = IdealNoDelayGetOutput('myhostname', 'myhostname#')
        return IOS(ssh)

    @property
    def engine_at_config_mode_prompt(self):
        ssh = IdealNoDelayGetOutput('myhostname', 'myhostname(config)#')
        return IOS(ssh)


class TestNavigateCLIToConfigMode(BaseTest):

    def test_proper_commands_from_std_user(self):
        ssh = self.engine_at_std_user_prompt
        ssh.transport.enable_password = 'mypass'
        ssh.transport.load_canned_response('enable\n')
        ssh.transport.load_canned_response('myhostname#\n')
        ssh.transport.load_canned_response('config t\nmyhostname(config)#\n')
        expected_commands = ['enable', 'mypass', 'config t']
        ssh.cli_to_config_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_configuration_mode)

    def test_raises_exception_if_no_enable_from_std_user(self):
        ssh = self.engine_at_std_user_prompt
        ssh.transport.load_canned_response('enable\n')
        ssh.transport.load_canned_response('myhostname#\n')
        ssh.transport.load_canned_response('config t\nmyhostname(config)#\n')
        self.assertRaises(EnablePasswordError, ssh.cli_to_config_mode)

    def test_proper_commands_from_priv_exec(self):
        ssh = self.engine_at_priv_exec_prompt
        ssh.transport.load_canned_response('config t\nmyhostname(config)#\n')
        expected_commands = ['config t']
        ssh.cli_to_config_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_configuration_mode)

    def test_proper_commands_from_config_mode(self):
        ssh = self.engine_at_config_mode_prompt
        expected_commands = []
        ssh.cli_to_config_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_configuration_mode)


class TestNaviateCLIToPrivExec(BaseTest):

    def test_proper_commands_from_std_user(self):
        ssh = self.engine_at_std_user_prompt
        ssh.transport.enable_password = 'mypass'
        ssh.transport.load_canned_response('enable\n')
        ssh.transport.load_canned_response('myhostname#\n')
        expected_commands = ['enable', 'mypass']
        ssh.cli_to_privileged_exec_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_privileged_exec_mode)

    def test_raises_exception_if_no_enable_from_std_user(self):
        ssh = self.engine_at_std_user_prompt
        ssh.transport.load_canned_response('enable\n')
        ssh.transport.load_canned_response('myhostname#\n')
        self.assertRaises(EnablePasswordError, ssh.cli_to_privileged_exec_mode)

    def test_proper_commands_from_priv_exec(self):
        ssh = self.engine_at_priv_exec_prompt
        ssh.transport.enable_password = 'mypass'
        expected_commands = []
        ssh.cli_to_privileged_exec_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_privileged_exec_mode)

    def test_proper_commands_from_config_mode(self):
        ssh = self.engine_at_config_mode_prompt
        ssh.transport.load_canned_response('myhostname#\n')
        expected_commands = ['end']
        ssh.cli_to_privileged_exec_mode()
        self.assertEqual(expected_commands, ssh.transport.all_commands_sent)
        self.assertEqual(True, ssh.transport.in_privileged_exec_mode)

class TestPrompt(BaseTest):

    def test_returns_prompt_from_transport_engine(self):
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname#')
        ssh = IOS(engine)
        self.assertEqual(ssh.transport.prompt, ssh.prompt)
        # change the prompt in the transport engine and retest to confirm
        ssh.transport.prompt = 'mynewprompt#'
        self.assertEqual('mynewprompt#', ssh.prompt)

class TestHostname(BaseTest):
    def test_returns_hostname_from_transport_engine(self):
        engine = IdealNoDelayGetOutput('myhostname', 'myhostname#')
        ssh = IOS(engine)
        self.assertEqual(ssh.transport.hostname, ssh.hostname)
        # change the prompt in the transport engine and retest to confirm
        ssh.transport.hostname = 'mynewhostname'
        self.assertEqual('mynewhostname', ssh.hostname)


class TestSendQuestion(BaseTest):

    def setUp(self) -> None:
        self.ssh = self.engine_at_priv_exec_prompt
        self.ssh.transport.load_canned_response('my command question ?\noutput\nmy command question ')
        self.ssh.transport.load_canned_response('')
        self.ssh.send_question_get_output('my command question')


    def test_appends_question_mark_with_space(self):
        command_auctually_sent = ''.join(self.ssh.transport._unit_test_commands_sent[0])
        self.assertEqual('my command question ?', command_auctually_sent)

    def test_second_command_is_deleting_the_command_that_was_returned(self):
        second_command_auctually_sent = ''.join(self.ssh.transport._unit_test_commands_sent[1])
        expected_second_command = ''.join([chr(8) for x in range(len('my command question') + 1)])
        self.assertEqual(expected_second_command, second_command_auctually_sent)

    def test_sends_2_total_commands(self):
        second_command_auctually_sent = ''.join(self.ssh.transport._unit_test_commands_sent[1])
        expected_second_command = ''.join([chr(8) for x in range(len('my command question') + 1)])
        self.assertEqual(expected_second_command, second_command_auctually_sent)

    def test_strips_question_if_one_is_provided(self):
        ssh = self.engine_at_priv_exec_prompt
        ssh.transport.load_canned_response('my command question ?\noutput\nmy command question ')
        ssh.transport.load_canned_response('')
        ssh.send_question_get_output('my command question?')
        # take list of tuples and join everything together to make a single string
        all_commands_sent_string = ''.join([f'{cmd}{ending}' for cmd, ending in ssh.transport._unit_test_commands_sent])
        # count number of question marks in string it should be one
        total_question_marks = sum(1 for char in all_commands_sent_string if char == '?')
        self.assertEqual(1, total_question_marks)


