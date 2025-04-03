from CiscoAutomationFramework.Parsers.ConfigSectionTypes import InterfaceConfig, IPAccessControlList, RouteMap,\
    PrefixList
from CiscoAutomationFramework.Parsers.ConfigSectionObjects.StaticRoute import StaticRoute
from CiscoAutomationFramework.util import (convert_config_tree_to_list, search_config_tree,
                                           search_and_modify_config_tree)
from collections import OrderedDict


def matches_search_terms(key, search_terms, case_sensitive, full_match):
    """Checks if the key matches any search term based on given options."""
    if not case_sensitive:
        key = key.lower()
        search_terms_lower = [term.lower() for term in search_terms]
    else:
        search_terms_lower = search_terms

    for term in search_terms_lower:

        if full_match:
            if key == term:  # Exact match
                return True
        else:
            if term in key:  # Partial match
                return True
    return False


class ConfigParser:

    def __init__(self, running_config):
        if isinstance(running_config, str):
            self.running_config = running_config.splitlines()
        else:
            self.running_config = running_config
        self._config_tree = {}

    @property
    def config_tree(self):
        '''
        The running config that was passed in, parsed into a string format

        :return: dictionary tree
        :rtype: dict
        '''
        if self._config_tree:
            return self._config_tree
        else:
            tree = OrderedDict()
            stack = [(0, tree)]

            for line in self.running_config:
                if not line.strip():
                    continue

                text = line.lstrip()
                indent = len(line) - len(text)

                current_node = {}
                # If we're at the top level (no indentation), always attach to root
                if indent == 0:
                    parent = tree
                    stack = [(0, tree)]  # Reset stack to this level
                else:
                    while stack and stack[-1][0] >= indent:
                        stack.pop()

                    if not stack:
                        raise ValueError(f"Invalid indentation or format at line: {line}")

                    parent = stack[-1][1]

                parent[text] = current_node
                stack.append((indent, current_node))
            self._config_tree = tree
            return tree

    def search_config_tree(self, search_terms, case_sensitive=True, full_match=False, min_search_depth=0, max_search_depth=0, tree=None):
        """
        Searches the config tree for a set of search terms and returns the path to root for that match. Note: the
        search will not return child branches after the match, just parent branches back to the root.

        You may also specify if you want your search to be case sensitive, and you may also specify if you want
        a full or partial match. For example if I do a full match for "description" but the line of configuration
        is "description example" it will NOT match. Also if I do a partial match (by setting full match to false) for
        "descrip", and the line is "description example" it WILL match.

        :param search_terms: List of search terms to search for.
        :type search_terms: list
        :param case_sensitive: Whether the search is case-sensitive.
        :type case_sensitive: bool
        :default case_sensitive: True
        :param full_match: If True, matches the whole word exactly; else, allows partial matches.
        :type full_match: bool
        :param tree: The configuration tree to search, Do not specify this, its only used for recursion.
        :type tree: dict or None
        :default tree: None

        :return: A dictionary containing matched and modified results.
        :rtype: dict
        """
        if not tree:
            tree = self.config_tree
        return search_config_tree(tree, search_terms, case_sensitive, full_match, min_search_depth, max_search_depth)

    def search_and_modify_config_tree(self, search_terms, case_sensitive=True, full_match=False, min_search_depth=0,
                                      max_search_depth=0, prepend_text='', append_text='', replace_tuple=('',''),
                                      tree=None):
        """
        Searches the config tree for a set of search terms, and if specified will run each line that matches
        a search term through a modification algorithm to prepend, append, and find/replace specified text on that line.

        Modification will ONLY occur to lines that CONTAIN a match! if you search for "description example" it will
        also return in the tree the interface name ex. interface GigabitEthernet1/0/1, however that line will NOT
        be eligible for the string modification because it does not contain "description example".

        Additionally using that same interface example, the interface will likely have other config besides the
        description, but if you search for the description, all other commands in that layer of the tree will
        not be returned, just the path up to the root which in this case is the interface name.

        You may also specify if you want your search to be case sensitive, and you may also specify if you want
        a full or partial match. For example if I do a full match for "description" but the line of configuration
        is "description example" it will NOT match. Also if I do a partial match (by setting full match to false) for
        "descrip", and the line is "description example" it WILL match.

        :param search_terms: List of search terms to search for.
        :type search_terms: list
        :param case_sensitive: Whether the search is case-sensitive.
        :type case_sensitive: bool
        :default case_sensitive: True
        :param full_match: If True, matches the whole word exactly; else, allows partial matches.
        :type full_match: bool
        :default full_match: False
        :param prepend_text: Text to prepend to matches.
        :type prepend_text: str
        :default prepend_text: ""
        :param append_text: Text to append to matches.
        :type append_text: str
        :default append_text: ""
        :param replace_tuple: A tuple (old_text, new_text) for replacing matches.
        :type replace_tuple: tuple or None
        :default replace_tuple: None
        :param tree: The configuration tree to search. Do not specify this, its only used for recursion
        :type tree: dict or None
        :default tree: None

        :return: A dictionary containing matched and modified results.
        :rtype: dict
        """
        if not tree:
            tree = self.config_tree
        return search_and_modify_config_tree(tree, search_terms, case_sensitive, full_match, min_search_depth,
                                             max_search_depth, prepend_text, append_text, replace_tuple)

    def config_tree_to_list(self, tree=None, indent=0, indent_step=0):
        """
        Converts a tree representation of the configuration into a list that can be pasted
        into a device

        :param tree: Tree representation of a configuration file
        :type tree: dict
        :param indent: number of spaces to indent root with
        :type indent: int
        :param indent_step: number of indent spaces to increment when going from a root to a branch (default 0, no indent)

        :return: List representation of config tree
        :rtype: list
        """

        if not tree:
            tree = self.config_tree

        return convert_config_tree_to_list(tree=tree, indent=indent, indent_step=indent_step)

    def _nextline_startswith_space(self, current_line_index):
        try:
            if self.running_config[current_line_index + 1].startswith(' '):
                return True
        except IndexError:
            return False
        else:
            return False

    @property
    def _config_sections(self):
        """
        Parses running config for any first level configuration sections for example below would be a section

        router eigrp 1
          network 1.1.1.1 0.0.0.0
          network 2.2.2.2 0.0.0.0

        """
        data = []
        section_data = []
        for index, line in enumerate(self.running_config):
            if self._nextline_startswith_space(index):
                section_data.append(line)
            else:
                if len(section_data) > 0:
                    section_data.append(line)
                    data.append(section_data)
                    section_data = []
        return data

    @property
    def __global_config_lines(self):
        """
        !!Not for external use!!
        Only local to this object at this time.

        Will return a list of lines of configuration that DO NOT have any nested config.
        Because the way Cisco IOS works when outputing the config, there may be instances
        that an interface gets looped in as a blank interface will look like a global
        line of config.

        Until I find a better way of parsing to account for these edge cases in a comprehensive way,
        I think its best to leave this to internal use
        """
        lines = []
        for config, sub_tree in self.config_tree.items():
            if not sub_tree:
                lines.append(config)
        return lines


    def sections_config_referenced_in(self, config_match, prepend_space_in_search=True):
        """
        Searches through all detected 'sections' of config for the supplied config_match string.
        If it finds it nested in the section (in the indented section) it will return the first line of
        that config section in a list with other matches.
        """
        search_string = f' {config_match}' if prepend_space_in_search else config_match

        sections = []
        for section in self._config_sections:
            if any(search_string in x for x in section[1:]):
                sections.append(section[0])

        return sections


    def get_config_section(self, title_startswith, return_all=True):
        """
        Extracts a specific configuration section whos first line starts with your variable.
        Because we search if the title startswith your variable you could have multiple results
        so instead of always returning the first one, I give the option to return all

        :param title_startswith: Text that the first line of the section starts with (ex. line vty)
        :type title_startswith: str
        :param return_all: If there are multiple matches return all if True (default True)
        :type return_all: bool
        :return: list of lists containing the sections of config
        :rtype: list
        """
        data = []
        for section in self._config_sections:
            if section[0].startswith(title_startswith):
                if return_all:
                    data.append(section)
                else:
                    return section
        return data

    def has_global_config(self, config_string):
        """
        True/False if in the global configuration the string is found. The line must NOT start with a space
        so if it is nested it will not be found

        :param config_string:
        :return:
        """
        for line in self.running_config:
            if config_string in line and not line.startswith(' '):
                return True
        return False

    def interfaces_that_have_config(self, config_string, full_match=False, case_sensitive=True):
        interfaces = []
        for interface in self.interface_configs:
            if interface.has_config(config_string, full_match=full_match, case_sensitive=case_sensitive):
                interfaces.append(interface)
        return interfaces

    @property
    def version(self):
        for line in self.__global_config_lines:
            if 'version' in line:
                return line.split()[1]
        return ''

    @property
    def local_users(self):
        users = []
        for line in self.__global_config_lines:
            if 'username' in line:
                users.append(line.split()[1])
        return users

    @property
    def interface_configs(self):
        return [InterfaceConfig(name, config) for name, config in self.search_config_tree('interface ').items()]

    @property
    def ip_access_control_lists(self):
        return [IPAccessControlList(x) for x in self._config_sections if x[0].startswith('ip access-list')]

    @property
    def numbered_access_control_lists(self):
        data = []
        acl_data = []
        acl_num = None

        for line in self.running_config:
            if line.startswith('access-list'):
                num = line.split()[1]
                if num != acl_num:
                    if len(acl_data) > 0:
                        data.append(acl_data)
                        acl_data = []
                    acl_num = num
                    acl_data.append(line)

                else:
                    acl_data.append(line)
        if len(acl_data) > 0:
            data.append(acl_data)
        return data

    @property
    def route_maps(self):

        data = {}
        for cfg_line, nested_config in self.config_tree.items():
            if 'route-map' in cfg_line:
                name = cfg_line.split()[1]
                if name not in data.keys():
                    data[name] = {}
                data[name].update({cfg_line: nested_config})

        return [RouteMap(name, config) for name, config in data.items()]

    @property
    def unused_route_maps(self):
        all_route_maps = {rm.name: {} for rm in self.route_maps}

        for name in all_route_maps.keys():
            results = self.search_config_tree(name, full_match=False, case_sensitive=True)
            syntactic_usages = [f'{name} in', f'{name} out', f'{name} export', f'{name} import', f'map {name}']
            all_route_maps[name] = search_config_tree(results, syntactic_usages, min_search_depth=1)

        return [self.get_route_map(name) for name, config in all_route_maps.items() if not config]

    @property
    def prefix_lists(self):

        data = {}
        for config, sub_tree in self.config_tree.items():
            if config.startswith('ip prefix-list'):
                name = config.split()[2]
                if name not in data.keys():
                    data[name] = {}
                data[name].update({config: sub_tree})

        return [PrefixList(name, config) for name, config in data.items()]

    @property
    def static_routes(self):
        static_routes = []
        for line in self.running_config:
            if line.startswith('ip route'):
                static_routes.append(StaticRoute(line))
        return static_routes

    def get_prefix_list(self, name):
        for list in self.prefix_lists:
            if list.name == name:
                return list
        return None

    def get_route_map(self, name):
        for map in self.route_maps:
            if map.name == name:
                return map
        return None




