from unittest import TestCase
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser
from CiscoAutomationFramework.Parsers.ConfigSectionTypes import RouteMap, RouteMapRule
from CiscoAutomationFramework.Parsers.PowerInlineParser import PowerInlineInterface, PowerInlineParser

parser_canned_output = """
!
route-map MULTI-SET permit 10 
 description abcdefg
 match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2
 set local-preference 800
 set community 12345
!         
route-map MULTI-RULES deny 10 
 description abcdefg
 match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2
!
route-map MULTI-RULES permit 1000 
 description Allow Everything Else

devicehostname#
"""

class ConfigParserRouteMapExtractorTests(TestCase):

    def setUp(self):
        self.parser = ConfigParser(parser_canned_output)

    def test_returns_list_of_parsers(self):
        self.assertTrue(all([True for x in self.parser.route_maps if type(x) == RouteMap]))

    def test_detects_correct_number_of_route_maps(self):
        self.assertEqual(len(self.parser.route_maps), 2)

    def test_able_to_extract_specific_route_map(self):
        self.assertEqual(self.parser.get_route_map('MULTI-RULES').name, 'MULTI-RULES')


class RouteMapParserTests(TestCase):
    def setUp(self):
        self.parser1 = RouteMap(
            ['route-map MULTI-SET permit 10',
             ' description abcdefg',
             'match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2',
             ' set local-preference 800',
             ' set community 12345']
        )
        self.parser2 = RouteMap(
            [
                'route-map MULTI-RULES deny 10',
                ' description abcdefg',
                ' match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2',
                'route-map MULTI-RULES permit 1000',
                ' description Allow Everything Else'
            ]
        )

    def test_detects_name(self):
        self.assertEqual(self.parser1.name, 'MULTI-SET')

    def test_detects_num_rules(self):
        self.assertEqual(self.parser1.num_rules, 1)
        self.assertEqual(self.parser2.num_rules, 2)


class RouteMapRuleParserTests(TestCase):

    def setUp(self):
        self.parser = RouteMapRule(
            ['route-map MULTI-SET permit 10',
             ' description abcdefg',
             ' match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2',
             ' set local-preference 800',
             ' set community 12345']
        )

    def test_extracts_sequence_num(self):
        self.assertEqual(self.parser.sequence_number, '10')

    def test_extracts_action(self):
        self.assertEqual(self.parser.action, 'permit')

    def test_extracts_match_clause(self):
        self.assertEqual(self.parser.match_clause, 'match ip address prefix-list PREFIX-LIST-1 PREFIX-LIST-2')

    def test_extracts_set_clause(self):
        self.assertEqual(self.parser.set_clause, ['set local-preference 800', 'set community 12345'])

    def test_extracts_description(self):
        self.assertEqual(self.parser.description, 'abcdefg')


