from CiscoAutomationFramework.Parsers.ConfigSectionTypes import InterfaceConfig, IPAccessControlList, RouteMap,\
    PrefixList
from CiscoAutomationFramework.Parsers.ConfigSectionObjects.StaticRoute import StaticRoute


class ConfigParser:

    def __init__(self, running_config):
        self.running_config = running_config.splitlines()

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




