from CiscoAutomationFramework.Parsers.ConfigSectionTypes import InterfaceConfig, IPAccessControlList, RouteMap,\
    PrefixList
from CiscoAutomationFramework.Parsers.ConfigSectionObjects.StaticRoute import StaticRoute
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
        self.running_config = running_config.splitlines()
        self._treed_config = {}

    @property
    def treed_config(self):
        '''
        The running config that was passed in, parsed into a string format

        :return: dictionary tree
        :rtype: dict
        '''
        if self._treed_config:
            return self._treed_config
        else:
            root = OrderedDict()
            stack = [(0, root)]

            for line in self.running_config:
                if not line.strip():
                    continue

                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                key = stripped
                current_node = {}

                # If we're at the top level (no indentation), always attach to root
                if indent == 0:
                    parent = root
                    stack = [(0, root)]  # Reset stack to this level
                else:
                    while stack and stack[-1][0] >= indent:
                        stack.pop()

                    if not stack:
                        raise ValueError(f"Invalid indentation or format at line: {line}")

                    parent = stack[-1][1]

                parent[key] = current_node
                stack.append((indent, current_node))
            self._treed_config = root
            return root

    def search_config_tree(self, search_terms, case_sensitive=True, full_match=False, tree=None):
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
            tree = self.treed_config

        if not any([isinstance(search_terms, x) for x in (list, tuple)]):
            search_terms = [search_terms]
            #raise TypeError('search_terms MUST be a list or tuple')

        data = {}
        for key, sub_tree in tree.items():
            if matches_search_terms(key, search_terms, case_sensitive, full_match):
                data[key] = sub_tree
            elif isinstance(sub_tree, dict) and sub_tree:
                path = self.search_config_tree(search_terms, case_sensitive, full_match, tree=sub_tree)
                if path:
                    data[key] = path
        return data

    def search_and_modify_config_tree(self, search_terms, case_sensitive=True, full_match=False, prepend_text='', append_text='', replace_tuple=('',''), tree=None):
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
            tree = self.treed_config

        if not any([isinstance(search_terms, x) for x in (list, tuple)]):
            search_terms = [search_terms]
            # raise TypeError('search_terms MUST be a list or tuple')

        data = {}
        for key, sub_tree in tree.items():
            if matches_search_terms(key, search_terms, case_sensitive, full_match):
                data[f'{prepend_text}{key.replace(*replace_tuple)}{append_text}'] = sub_tree
            elif isinstance(sub_tree, dict) and sub_tree:
                path = self.search_and_modify_config_tree(search_terms, case_sensitive, full_match, prepend_text, append_text, replace_tuple, sub_tree)
                if path:
                    data[key] = path
        return data

    def config_tree_to_list(self, tree, indent=0, indent_step=0):
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
            tree = self.treed_config

        data = []
        for key, subtree in tree.items():
            data.append(f'{" " * (indent * indent_step)}{key}')
            if isinstance(subtree, dict) and subtree:
                data.extend(self.config_tree_to_list(subtree, indent + 1, indent_step))
        return data

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

    def interfaces_that_have_config(self, config_string):
        interfaces = []
        for interface in self.interface_configs:
            if interface.has_config(config_string):
                interfaces.append(interface)
        return interfaces

    @property
    def version(self):
        for line in self.running_config:
            if 'version' in line:
                return line.split()[1]
        return None

    @property
    def local_users(self):
        users = []
        for line in self.running_config:
            if line.lower().startswith('username'):
                users.append(line.split()[1])
        return users

    @property
    def interface_configs(self):
        return [InterfaceConfig(x) for x in self._config_sections if x[0].startswith('interface')]

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

        raw_route_maps = {}
        working_map = ''
        for line in self.running_config:
            if line.startswith('route-map'):
                # Start of a route map rule, set working_map so we will capture subsequent lines of configuration
                working_map = line.split()[1]
                if not working_map in raw_route_maps.keys():
                    raw_route_maps[working_map] = [line]
                else:
                    raw_route_maps[working_map].append(line)
                continue

            if line.startswith('!'):
                # Denotes the end of a route map rule, set working_map to an empty string to stop collecting config
                working_map = ''

            if working_map:
                # If working_map is not empty, This line must be in a route map, collect it
                raw_route_maps[working_map].append(line)

        return [RouteMap(raw_config) for _, raw_config in raw_route_maps.items()]

    @property
    def prefix_lists(self):
        lists = {}
        for line in self.running_config:
            if line.startswith('ip prefix-list'):
                name = line.split()[2]
                if not name in lists.keys():
                    lists[name] = [line]
                else:
                    lists[name].append(line)

        return [PrefixList(data) for _, data in lists.items()]

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




