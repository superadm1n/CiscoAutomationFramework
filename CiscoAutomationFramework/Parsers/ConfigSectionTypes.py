from CiscoAutomationFramework.Parsers.ConfigSectionObjects import ConfigSection, TreeConfigSection
from CiscoAutomationFramework.util import search_config_tree, trees_are_equal


class InterfaceConfig(TreeConfigSection):

    @property
    def interface_name(self):
        return self.section.split()[-1]

    def has_config(self, config_line, case_sensitive=False, full_match=False):
        results = search_config_tree({self.section: self.config}, config_line, case_sensitive=case_sensitive,
                                     full_match=full_match)
        if results:
            return True
        return False

    def __repr__(self):
        return f'{type(self).__name__}({self.interface_name})'


class IPAccessControlList(ConfigSection):

    @property
    def name(self):
        return self.raw_config[0].split()[-1]

    @property
    def type(self):
        return self.raw_config[0].split()[2]

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'


class PrefixListEntry:

    """
    Object used to parse out the single prefix list line entry.
    It should be provided with data similer to below
    ip prefix-list MY-PREFIX-LIST seq 5 permit 10.0.0.0/8 le 32
    -- or --
    ip prefix-list MY-PREFIX-LIST seq 5 permit 10.0.0.0/8

    DO NOT provide it with multiple lines

    """

    def __init__(self, raw_entry):
        self.raw_data = raw_entry
        self.split_raw_data = raw_entry.split()

    @property
    def sequence_number(self):
        return self.split_raw_data[4]

    @property
    def action(self):
        return self.split_raw_data[5]

    @property
    def prefix(self):
        return self.split_raw_data[6]

    @property
    def entire_prefix(self):
        return ' '.join(self.split_raw_data[6:])

    @property
    def prefix_cidr(self):
        return self.prefix.split('/')[-1]

    @property
    def less_than_equal_to(self):
        return 'le' in self.entire_prefix

    @property
    def greater_than_equal_to(self):
        return 'ge' in self.entire_prefix


class PrefixList():

    """
    Object containing the raw data of the entire prefix list. Example data below

    ['ip prefix-list MY-PREFIX-LIST seq 5 permit 10.0.0.0/8 le 32',
     'ip prefix-list MY-PREFIX-LIST seq 10 permit 192.168.0.0',
    ]

    This object provides an interface to parse out the prefix list and get relevent data

    """

    def __init__(self, name, config):
        self._name = name
        self._config = config

    def __eq__(self, other):
        if not isinstance(other, PrefixList):
            raise TypeError('other MUST be an instance of PrefixList')

        return all([self._name == other._name, self._config == other._config])

    @property
    def name(self):
        """
        Name of prefix list
        """
        return self._name

    @property
    def num_rules(self):
        """
        Total number of rules in prefix list
        """
        return len(self._config)

    @property
    def rules(self):
        """
        List of the rules (in entry parser object) that the prefix list has configured
        """
        return [PrefixListEntry(config_line) for config_line, _ in self._config.items()]

    @property
    def sequence_numbers(self):
        """
        All the sequence numbers used in the prefix list
        """
        return [x.sequence_number for x in self.rules]

    def get_rule(self, sequence_number):
        """
        Get a specific rule from the prefix list by the sequence number
        """
        for rule in self.rules:
            if rule.sequence_number == sequence_number:
                return rule
        return None

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    def __str__(self):
        return self.name


class RouteMapRule:
    """
    Object to be used for each rule in a route map
    """

    def __init__(self, definition, rule_config_tree):
        self.definition = definition
        self.rule_config_tree = rule_config_tree

    def _extract_line(self, match_string):
        for key, sub_tree in self.rule_config_tree.items():
            if match_string in key:
                return key
            elif sub_tree:
                data = self._extract_line(match_string)
                if data:
                    return data
        return ''

    def _extract_lines(self, match_string):
        return_data = []
        for key, sub_tree in self.rule_config_tree.items():
            if match_string in key:
                return_data.append(key)
            elif sub_tree:
                data = self._extract_line(match_string)
                if data:
                    return_data.append(data)
        return return_data

    @property
    def sequence_number(self):
        """
        Rule Sequence Number
        """
        return self.definition.split()[-1]

    @property
    def action(self):
        """
        Rule action: permit/deny
        """
        return self.definition.split()[2]

    @property
    def match_clause(self):
        """
        Match clause configured in route map (if any configured)
        """
        return self._extract_line('match')

    @property
    def set_clause(self):
        """
        Set clause configured in route map (if any configured)
        """
        return self._extract_lines('set')

    @property
    def description(self):
        """
        Description configured in route map (if any configured)
        """
        data = self._extract_line('description')
        if data:
            return ' '.join(data.split()[1:])
        return data

    def __repr__(self):
        return f'{type(self).__name__}({self.sequence_number})'


class RouteMap:

    """
    Parser for entire route map. Responsible for parsing out each rule and providing access
    to all rules, a single rule, and high level information about the route map.
    """

    def __init__(self, rm_name, config):
        self.rm_name = rm_name
        self.config = config

    @property
    def config_tree(self):
        return {self.rm_name: self.config}

    @property
    def name(self):
        """
        Name of route map
        """
        return self.rm_name

    @property
    def num_rules(self):
        """
        Total number of rules in route map
        """
        return len(self.config)

    @property
    def rules(self):
        """
        List of all rules in route map, each rule is in a RouteMapRule object
        """
        return [RouteMapRule(definition, config) for definition, config in self.config.items()]

    @property
    def configured_sequence_numbers(self):
        return [x.sequence_number for x in self.rules]

    def get_rule(self, sequence_number):
        """
        Return a single rule based on its sequence number
        """
        for rule in self.rules:
            if rule.sequence_number == sequence_number:
                return rule
        return None

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, RouteMap):
            return False
        return trees_are_equal(other.config_tree, self.config_tree)