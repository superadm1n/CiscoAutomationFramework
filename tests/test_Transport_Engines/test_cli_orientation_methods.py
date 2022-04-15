from unittest import TestCase
from tests.test_Transport_Engines.Engines import TestableSendCommand


class TestPrivilegeExecDetection(TestCase):

    def setUp(self) -> None:
        self.ssh = TestableSendCommand()

    def test_passes_when_prompt_ends_in_hashtag_without_parentheses(self):
        self.ssh.prompt = 'myprompt#'
        self.assertEqual(True, self.ssh.in_privileged_exec_mode)

    def test_fails_when_prompt_ends_in_hashtag_with_parentheses(self):
        self.ssh.prompt = 'myprompt(config)#'
        self.assertEqual(False, self.ssh.in_privileged_exec_mode)

    def test_fails_when_prompt_ends_in_greater_than(self):
        self.ssh.prompt = 'myprompt>'
        self.assertEqual(False, self.ssh.in_privileged_exec_mode)


class TestConfigModeDetection(TestCase):
    def setUp(self) -> None:
        self.ssh = TestableSendCommand()

    def test_passes_when_prompt_ends_in_hashtag_with_parentheses(self):
        self.ssh.prompt = 'myprompt(config)#'
        self.assertEqual(True, self.ssh.in_configuration_mode)

    def test_fails_when_prompt_ends_in_greater_than(self):
        self.ssh.prompt = 'myprompt>'
        self.assertEqual(False, self.ssh.in_configuration_mode)

    def test_fails_when_prompt_ends_in_hashtag_without_parentheses(self):
        self.ssh.prompt = 'myprompt#'
        self.assertEqual(False, self.ssh.in_configuration_mode)


class TestUserExecModeDetection(TestCase):

    def setUp(self) -> None:
        self.ssh = TestableSendCommand()

    def test_passes_when_prompt_ends_in_greater_than(self):
        self.ssh.prompt = 'myprompt>'
        self.assertEqual(True, self.ssh.in_user_exec_mode)

    def test_fails_when_prompt_ends_with_hashtag(self):
        self.ssh.prompt = 'myprompt#'
        self.assertEqual(False, self.ssh.in_user_exec_mode)

    def test_fails_when_prompt_ends_in_number(self):
        self.ssh.prompt = 'myprompt5'
        self.assertEqual(False, self.ssh.in_user_exec_mode)

    def test_fails_when_prompt_ends_in_char(self):
        self.ssh.prompt = 'myprompt'
        self.assertEqual(False, self.ssh.in_user_exec_mode)

    def test_fails_when_prompt_ends_in_parentheses(self):
        self.ssh.prompt = 'myprompt(config)'
        self.assertEqual(False, self.ssh.in_user_exec_mode)

