from CiscoAutomationFramework.Parsers.ConfigSectionTypes import InterfaceConfig, IPAccessControlList


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

    def has_global_config(self, config_string):
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


