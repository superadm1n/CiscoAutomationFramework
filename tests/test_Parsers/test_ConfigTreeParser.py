from unittest import TestCase
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser

canned_output = """interface GigabitEthernet1/0/1
 description Test
 switchport mode trunk
 switchport trunk allowed vlan 10,11,12
!
router bgp 65000
 template peer-policy TEST
  route-map INBOUND_RM in
  route-map OUTBOUND_RM out
 exit-peer-policy
 !
template peer-session TEST
  remote-as 65100
  log-neighbor-changes
 exit-peer-session
 !
 bgp router-id 10.121.63.11
 neighbor 10.50.50.1 remote-as 65300
 !
 address-family ipv4 vrf MYVRF
  network 10.0.0.0
  redistribute connected
 !
 address-family ipv4 vrf OTHERVRF
  network 172.16.0.0
  redistribute connected
"""


class ConfigParserTreeTests(TestCase):

    def setUp(self) -> None:
        simplified_output = '''a
                 b
                  d
                  e
                 c
                  f
                  g
                   h'''
        self.parser = ConfigParser(canned_output)
        self.simplified_output_parser = ConfigParser(simplified_output)

    def test_search_accepts_a_string(self):
        output = self.simplified_output_parser.search_config_tree('h')
        expected = {'a': {'c': {'g': {'h': {}}}}}
        self.assertEqual(output, expected)

    def test_search_accepts_a_list(self):
        output = self.simplified_output_parser.search_config_tree(['f', 'e'])
        expected = {'a': {'b': {'e': {}}, 'c': {'f': {}}}}
        self.assertEqual(output, expected)

    def test_splits_a_string_by_lines(self):
        expected_tree = {'a': {'b': {'d': {}, 'e': {}}, 'c': {'f': {}, 'g': {'h': {}}}}}
        self.assertEqual(self.simplified_output_parser.config_tree, expected_tree)

    def test_searches_leaf(self):
        """
        When searching for a leaf element in a tree, it should return that leaf element AND everything upstream,
        It should NOT return any other equal leaf elements
        """
        output = self.parser.search_config_tree('redistribute connected')
        expected_tree = {'template peer-session TEST': {'address-family ipv4 vrf MYVRF': {'redistribute connected': {}}, 'address-family ipv4 vrf OTHERVRF': {'redistribute connected': {}}}}
        self.assertEqual(output, expected_tree)

    def test_searches_top_level_root(self):
        '''
        When searching for a root element in a tree, it should return ALL child elements
        '''

        output = self.parser.search_config_tree('interface GigabitEthernet1/0/1')
        expected_tree = {'interface GigabitEthernet1/0/1': {'description Test': {}, 'switchport mode trunk': {}, 'switchport trunk allowed vlan 10,11,12': {}}}
        self.assertEqual(output, expected_tree)

    def test_searches_branch(self):
        '''
        When searching for something at the root of a branch in a tree, it should return everything within that branch,
        It should NOT return anything above the branch root
        '''
        output = self.parser.search_config_tree('address-family ipv4 vrf MYVRF')
        expected_tree = {'template peer-session TEST': {'address-family ipv4 vrf MYVRF': {'network 10.0.0.0': {}, 'redistribute connected': {}}}}
        self.assertEqual(output, expected_tree)

    def test_collapses_tree_to_list_no_indent(self):
        '''
        Tests that by default it will just collapse the tree to a list without any indentation
        '''
        output = self.simplified_output_parser.config_tree_to_list()
        expected = ['a', 'b', 'd', 'e', 'c', 'f', 'g', 'h']
        self.assertEqual(output, expected)

    def test_collapses_tree_to_list_with_indent(self):
        """
        Tests that it will properly indent when specified to
        """
        output = self.simplified_output_parser.config_tree_to_list(indent_step=1)
        expected = ['a', ' b', '  d', '  e', ' c', '  f', '  g', '   h']
        self.assertEqual(output, expected)
