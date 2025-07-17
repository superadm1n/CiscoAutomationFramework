from unittest import TestCase
from CiscoAutomationFramework.Exceptions import ForbiddenError
from Engines import TestableNonConfTEngine

def generate_abbreviations(cmd1, cmd2):
    abbreviations = []
    for i in range(1, len(cmd1) + 1):  # At least 1 character
        for j in range(1, len(cmd2) + 1):
            abbreviations.append(f"{cmd1[:i]} {cmd2[:j]}")
    return abbreviations


class TestGettingOutput(TestCase):

    def setUp(self):
        self.engine = TestableNonConfTEngine()

    def test_cant_enter_config_t(self):
        """Tests to make sure any combination of configure terminal will result in an error"""
        combos = generate_abbreviations("configure", "terminal")
        for command in combos:
            self.assertRaises(ForbiddenError, self.engine._send_command, command)

    def test_cant_write_erase(self):
        '''Test to make sure any combo of "write erase" will throw an error'''
        combos = generate_abbreviations('write', 'erase')
        for command in combos:
            self.assertRaises(ForbiddenError, self.engine._send_command, command)

    def test_cant_reload(self):
        '''Test to make sure any combo of "reload" will throw an error'''
        cmd = 'reload'
        combos = [cmd[:x] for x in range(1, len(cmd)+1)]
        for command in combos:
            self.assertRaises(ForbiddenError, self.engine._send_command, command)

    def test_can_issue_show_command(self):
        '''Test to make sure you can still send a show command'''
        try:
            self.engine._send_command('show ip int br')
        except ForbiddenError:
            self.fail('Unable to issue a show command')
