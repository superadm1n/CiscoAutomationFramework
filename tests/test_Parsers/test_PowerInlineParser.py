from unittest import TestCase
from CiscoAutomationFramework.Parsers.PowerInlineParser import PowerInlineInterface, PowerInlineParser

canned_output = """sh power in

Module   Available     Used     Remaining
          (Watts)     (Watts)    (Watts)
------   ---------   --------   ---------
1           740.0       96.3       643.7
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi1/0/1   auto   off        0.0     n/a                 n/a   30.0
Gi1/0/2   auto   off        0.0     n/a                 n/a   30.0
Gi1/0/3   auto   on         15.4    Ieee PD             0     30.0
Gi1/0/13  auto   on         6.3     IP Phone 7941       2     30.0
Gi1/0/32  auto   on         6.5     Poly VVX D230       2     30.0
Gi1/0/33  auto   off        0.0     n/a                 n/a   30.0

devicehostname#
"""


class PowerInlineTableParserTests(TestCase):

    def setUp(self) -> None:
        self.parser = PowerInlineParser(canned_output.splitlines())

    def test_splits_a_string_by_lines(self):
        parser = PowerInlineParser(canned_output)
        self.assertEqual(type(parser._data), list)

    def test_accepts_list(self):
        self.assertEqual(type(self.parser._data), list)

    def test_returns_line_parsers(self):
        all_parsers = all([isinstance(x, PowerInlineInterface) for x in self.parser.interfaces])
        self.assertEqual(all_parsers, True)

    def test_returns_proper_number(self):
        num = len(self.parser.interfaces)
        self.assertEqual(num, 6)

    def test_throws_value_error_if_command_missing(self):
        canned_data = '\nGlobal DeviceTracking = Enabled\nhostname#'
        self.assertRaises(ValueError, PowerInlineParser, (canned_data))

    def test_allows_pipe_in_command(self):
        canned_data = 'show power inline | inc 1/0/17\nGlobal DeviceTracking = Enabled\nhostname#'
        try:
            _ = PowerInlineParser(canned_data)
        except ValueError:
            self.fail('Instantiation of DeviceTrackingOutputParser raised ValueError when command contained a pipe')

    def test_throws_value_error_if_wrong_command_output(self):
        canned_data = 'show ip device tracking all\nGlobal DeviceTracking = Enabled\nhostname#'
        self.assertRaises(ValueError, PowerInlineParser, (canned_data))


class LineParserTests(TestCase):
    def setUp(self) -> None:
        self.multi_word = PowerInlineInterface('Gi1/0/13  auto   on         6.3     IP Phone 7941       2     30.0')
        self.single_word = PowerInlineInterface('Gi1/0/2   auto   off        0.0     n/a                 n/a   30.0')


    def test_extracts_name(self):
        self.assertEqual(self.multi_word.name, 'Gi1/0/13')
        self.assertEqual(self.single_word.name, 'Gi1/0/2')

    def test_extracts_admin(self):
        self.assertEqual(self.multi_word.admin, 'auto')
        self.assertEqual(self.single_word.admin, 'auto')

    def test_extracts_oper(self):
        self.assertEqual(self.multi_word.oper, 'on')
        self.assertEqual(self.single_word.oper, 'off')

    def test_extracts_watts(self):
        self.assertEqual(self.multi_word.watts, 6.3)
        self.assertEqual(self.single_word.watts, 0.0)

    def test_extracts_detected_device(self):
        self.assertEqual(self.multi_word.detected_device, 'IP Phone 7941')
        self.assertEqual(self.single_word.detected_device, 'n/a')

    def test_extracts_poe_class(self):
        self.assertEqual(self.multi_word.poe_class, '2')
        self.assertEqual(self.single_word.poe_class, 'n/a')

    def test_extracts_max_watts(self):
        self.assertEqual(self.multi_word.max_watts, 30.0)
        self.assertEqual(self.single_word.max_watts, 30.0)




