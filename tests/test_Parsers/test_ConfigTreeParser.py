from unittest import TestCase
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser
from CiscoAutomationFramework.util import search_config_tree, search_and_modify_config_tree, trees_are_equal
from json import loads
from collections import OrderedDict
from copy import deepcopy

canned_output = """hostname MyRouter
!
vrf definition CORP
 rd 123:456
 !
 address-family ipv4
  import ipv4 unicast map VRF_RM
!
interface GigabitEthernet1/0/1
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
  redistribute ospfv3 1 match internal external 1 external 2 route-map RDIST_RM_USED
  redistribute connected
 exit-address-family
!
route-map unused_route_map permit 10
 description permit specific community
 match community 1
!
route-map unused_route_map deny 20
 description Deny everything else
!
route-map INBOUND_RM permit 10
 description Used Route Map
!
route-map OUTBOUND_RM permit 10
 description Used Route Map
!
route-map VRF_RM permit 10
 description Used Route Map
!
route-map RDIST_RM_USED permit 10
 description Used Route Map
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

    def test_search_returns_parser_object(self):
        output = self.parser.search_config_tree('h')
        self.assertIsInstance(output, ConfigParser)

    def test_search_accepts_a_string(self):
        output = self.simplified_output_parser.search_config_tree('h').config_tree
        expected = {'a': {'c': {'g': {'h': {}}}}}
        self.assertEqual(output, expected)

    def test_search_accepts_a_list(self):
        output = self.simplified_output_parser.search_config_tree(['f', 'e']).config_tree
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
        output = self.parser.search_config_tree('redistribute connected').config_tree
        expected_tree = {'template peer-session TEST': {'address-family ipv4 vrf MYVRF': {'redistribute connected': {}}, 'address-family ipv4 vrf OTHERVRF': {'redistribute connected': {}}}}
        self.assertEqual(output, expected_tree)

    def test_searches_top_level_root(self):
        '''
        When searching for a root element in a tree, it should return ALL child elements
        '''

        output = self.parser.search_config_tree('interface GigabitEthernet1/0/1').config_tree
        expected_tree = {'interface GigabitEthernet1/0/1': {'description Test': {}, 'switchport mode trunk': {}, 'switchport trunk allowed vlan 10,11,12': {}}}
        self.assertEqual(output, expected_tree)

    def test_searches_branch(self):
        '''
        When searching for something at the root of a branch in a tree, it should return everything within that branch,
        It should NOT return anything above the branch root
        '''
        output = self.parser.search_config_tree('address-family ipv4 vrf MYVRF').config_tree
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

    def test_finds_ununsed_route_maps(self):
        self.assertEqual(['unused_route_map'], [x.name for x in self.parser.unused_route_maps])


class RootParserSearchTests(TestCase):

    def setUp(self) -> None:
        self.parsed_config = OrderedDict({"hostname MyRouter": {}, "!": {}, "interface GigabitEthernet1/0/1": {"description InterfaceDescription": {}, "ip address 192.168.10.1 255.255.255.0": {}}, "archive": {"log config": {"logging enable": {}, "logging size 1000": {}, "notify syslog contenttype plaintext": {}}, "path bootflash:/backup": {}, "maximum 4": {}, "write-memory": {}}, "router bgp 65100": {"neighbor 192.168.10.2 remote-as 65200": {}, "!": {}, "address-family ipv4": {"network 10.100.0.0 mask 255.255.255.0": {}}, "address-family ipv4 vrf MyVRF": {"network 10.200.0.0 mask 255.255.255.0": {}, "neighbor 10.201.0.2 activate": {}, "neighbor 10.201.0.2 route-map from_neighbor in": {}}, "exit-address-family": {}}, "! ": {}, "route-map from_neighbor permit 10": {"description Permit select routes": {}, "match ip address prefix-list from_neighbor": {}}, "route-map from_neighbor deny 20": {"description Deny everything else": {}}, "route-map unused_route_map permit 10": {"description permit specific community": {}, "match community 1": {}}, "route-map unused_route_map deny 20": {"description Deny everything else": {}}, "ip prefix-list from_neighbor seq 10 permit 10.0.0.0/8 le 32": {}, "ip prefix-list from_neighbor seq 20 permit 192.168.0.0/24": {}, "ip prefix-list unused_pfx_list seq 10 permit 172.16.0.0/24 le 32": {}, "ip prefix-list unused_pfx_list seq 20 permit 172.17.0.0/24": {}})

    def test_accepts_list(self):
        try:
            search_config_tree(self.parsed_config, ['hostname'])
        except Exception:
            self.fail('Unable to accept list as a search term')

    def test_accepts_string(self):
        try:
            search_config_tree(self.parsed_config, 'hostname')
        except Exception:
            self.fail('Unable to accept string as a search term')

    def test_root_search(self):
        result = search_config_tree(self.parsed_config, 'hostname')
        self.assertEqual(result, {'hostname MyRouter': {}})

    def test_nested_search(self):
        result = search_config_tree(self.parsed_config, 'InterfaceDescription')
        self.assertEqual(result, {'interface GigabitEthernet1/0/1': {'description InterfaceDescription': {}}})

    def test_search_min_depth(self):
        result = search_config_tree(self.parsed_config, 'hostname', min_search_depth=1)
        self.assertEqual(result, {})

    def test_search_max_depth(self):
        result = search_config_tree(self.parsed_config, 'InterfaceDescription', max_search_depth=1)
        self.assertEqual(result, {})

    def test_returns_dict(self):
        result = search_config_tree(self.parsed_config, 'InterfaceDescription')
        self.assertIsInstance(result, dict)


class ConversionTests(TestCase):

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

    def test_converting_to_list_doesnt_return_full_config(self):
        '''Makes sure that the config parser will not return the full config when a match is not found'''
        new_parser = self.parser.search_config_tree('noexist')
        self.assertNotEquals(self.parser.config_tree, new_parser.config_tree)


class EqualityParserTests(TestCase):

    def setUp(self) -> None:
        self.t1 = OrderedDict({"hostname MyRouter": {}, "!": {}, "interface GigabitEthernet1/0/1": {"description InterfaceDescription": {}, "ip address 192.168.10.1 255.255.255.0": {}}})
        self.t2 = OrderedDict({"hostname MyRouter": {}, "!": {},
                               "interface GigabitEthernet1/0/1": {"description different_descriotion": {},
                                                                  "ip address 192.168.10.1 255.255.255.0": {}}})

    def test_able_to_exclude_key(self):
        result = trees_are_equal(self.t1, self.t2, exclude_keys=['description'])
        self.assertEqual(True, result)

    def test_detects_mismatch(self):
        result = trees_are_equal(self.t1, self.t2)
        self.assertEqual(False, result)

    def test_catches_additonal_key_in_first_tree(self):
        t1 = deepcopy(self.t1)
        t1['newkey'] = {}
        result = trees_are_equal(t1, self.t2)
        self.assertEqual(False, result)

    def test_catches_additonal_key_in_second_tree(self):
        t2 = deepcopy(self.t2)
        t2['newkey'] = {}
        result = trees_are_equal(self.t1, t2)
        self.assertEqual(False, result)
