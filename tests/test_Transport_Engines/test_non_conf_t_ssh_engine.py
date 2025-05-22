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