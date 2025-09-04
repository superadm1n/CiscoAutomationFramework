from unittest import TestCase
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser
from CiscoAutomationFramework.Parsers.ConfigSectionTypes import PrefixList, PrefixListEntry


parser_canned_output = """
!
ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 le 32
ip prefix-list first_prefix_list seq 20 permit 192.168.0.0/24
!
ip prefix-list second_prefix_list seq 10 permit 172.16.0.0/24 le 32
ip prefix-list second_prefix_list seq 20 permit 172.16.1.0/24
!
devicehostname#
"""


class ConfigParserPrefixListExtractorTests(TestCase):

    def setUp(self):
        self.parser = ConfigParser(parser_canned_output)

    def test_returns_list_of_parsers(self):
        self.assertTrue(all([True for x in self.parser.prefix_lists if type(x) == PrefixList]))

    def test_detects_correct_number_of_prefix_lists(self):
        self.assertEqual(len(self.parser.prefix_lists), 2)

    def test_able_to_extract_specific_prefix_lists(self):
        self.assertEqual(self.parser.get_prefix_list('first_prefix_list').name, 'first_prefix_list')


class PrefixListEntryParserTests(TestCase):
    pass


class PrefixListParserTests(TestCase):
    def setUp(self):
        self.parser = PrefixList(
            'first_prefix_list', {'ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 le 32': {}, 'ip prefix-list first_prefix_list seq 20 permit 192.168.0.0/24': {}}
        )

        self.parser_equal = PrefixList(
            'first_prefix_list', {'ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 le 32': {},
                                  'ip prefix-list first_prefix_list seq 20 permit 192.168.0.0/24': {}}
        )
        self.parser_not_equal = PrefixList(
            'first_prefix_list', {'ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 le 32': {},
                                  'ip prefix-list first_prefix_list seq 20 permit 192.168.10.0/24': {}}
        )

    def test_detects_name(self):
        self.assertEqual(self.parser.name, 'first_prefix_list')

    def test_detects_num_rules(self):
        self.assertEqual(self.parser.num_rules, 2)

    def test_detects_seq_numbers(self):
        self.assertEqual(self.parser.sequence_numbers, ['10', '20'])

    def test_able_to_compare_equality(self):
        self.assertEqual(self.parser, self.parser_equal)

    def test_able_to_compare_non_equality(self):
        self.assertNotEqual(self.parser, self.parser_not_equal)


class PrefixListEntryParserTests(TestCase):

    def setUp(self):
        self.parser = PrefixListEntry('ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 le 32')
        self.ge_parser = PrefixListEntry('ip prefix-list first_prefix_list seq 10 permit 10.0.0.0/8 ge 32')

    def test_extracts_sequence_num(self):
        self.assertEqual(self.parser.sequence_number, '10')

    def test_extracts_action(self):
        self.assertEqual(self.parser.action, 'permit')

    def test_extracts_prefix_not_le_ge_eq(self):
        self.assertEqual(self.parser.prefix, '10.0.0.0/8')

    def test_extracts_prefix_with_le_ge_eq(self):
        self.assertEqual(self.parser.entire_prefix, '10.0.0.0/8 le 32')

    def test_detects_ge(self):
        self.assertTrue(self.ge_parser.greater_than_equal_to)

    def test_no_false_positive_ge(self):
        self.assertFalse(self.parser.greater_than_equal_to)

    def test_detects_le(self):
        self.assertTrue(self.parser.less_than_equal_to)

    def test_no_false_positive_le(self):
        self.assertFalse(self.ge_parser.less_than_equal_to)

    def test_extracts_prefix_cidr(self):
        self.assertEqual(self.parser.prefix_cidr, '8')



