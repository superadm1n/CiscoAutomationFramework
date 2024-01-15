

class ConfigSection:
    def __init__(self, raw_config):
        self.raw_config = raw_config

    def __eq__(self, other):
        if isinstance(other, type(self)) and self.raw_config == other.raw_config:
            return True
        return False


class InterfaceConfig(ConfigSection):

    @property
    def interface_name(self):
        return self.raw_config[0].split()[-1]

    def has_config(self, config_line):
        for line in self.raw_config:
            if config_line.lower() in line.lower():
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
    def less_than_equal_to(self):
        return 'le' in self.entire_prefix

    @property
    def greater_than_equal_to(self):
        return 'ge' in self.entire_prefix


class PrefixList(ConfigSection):

    """
    Object containing the raw data of the entire prefix list. Example data below

    ['ip prefix-list MY-PREFIX-LIST seq 5 permit 10.0.0.0/8 le 32',
     'ip prefix-list MY-PREFIX-LIST seq 10 permit 192.168.0.0',
    ]

    This object provides an interface to parse out the prefix list and get relevent data

    """

    @property
    def name(self):
        """
        Name of prefix list
        """
        return self.raw_config[0].split()[2]

    @property
    def num_rules(self):
        """
        Total number of rules in prefix list
        """
        return len(self.raw_config)

    @property
    def rules(self):
        """
        List of the rules (in entry parser object) that the prefix list has configured
        """
        return [PrefixListEntry(x) for x in self.raw_config]

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

class RouteMapRule:
    """
    Object to be used for each rule in a route map
    """
    def __init__(self, raw_rule_config):
        self.raw_config = raw_rule_config

    def _extract_line(self, match_string):
        for line in self.raw_config:
            if match_string in line:
                return line
        return ''

    @property
    def sequence_number(self):
        """
        Rule Sequence Number
        """
        return self.raw_config[0].split()[-1]

    @property
    def action(self):
        """
        Rule action: permit/deny
        """
        return self.raw_config[0].split()[2]

    @property
    def match_clause(self):
        """
        Match clause configured in route map (if any configured)
        """
        data = self._extract_line('match')
        if data:
            return data.strip()
        return data

    @property
    def set_clause(self):
        """
        Set clause configured in route map (if any configured)
        """
        data = self._extract_line('set')
        if data:
            return data.strip()
        return data

    @property
    def description(self):
        """
        Description configured in route map (if any configured)
        """
        data = self._extract_line('description')
        if data:
            return ' '.join(data.split()[1:])
        return data


class RouteMap(ConfigSection):

    """
    Parser for entire route map. Responsible for parsing out each rule and providing access
    to all rules, a single rule, and high level information about the route map.
    """

    def _nextline_startswith_space(self, current_line_index):
        try:
            if self.raw_config[current_line_index + 1].startswith(' '):
                return True
        except IndexError:
            return False
        else:
            return False

    @property
    def _raw_parsed_rules(self):
        data = []
        section_data = []
        for index, line in enumerate(self.raw_config):
            if self._nextline_startswith_space(index):
                section_data.append(line)
            else:
                if len(section_data) > 0:
                    section_data.append(line)
                    data.append(section_data)
                    section_data = []
        return data

    @property
    def name(self):
        """
        Name of route map
        """
        return self.raw_config[0].split()[1]

    @property
    def num_rules(self):
        """
        Total number of rules in route map
        """
        return len([x for x in self.raw_config if 'route-map' in x])

    @property
    def rules(self):
        """
        List of all rules in route map, each rule is in a RouteMapRule object
        """
        return [RouteMapRule(x) for x in self._raw_parsed_rules]

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

