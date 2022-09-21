

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
