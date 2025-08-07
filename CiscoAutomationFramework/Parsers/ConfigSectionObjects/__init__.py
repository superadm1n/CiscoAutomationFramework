from CiscoAutomationFramework.util import convert_config_tree_to_list


class TreeConfigSection:
    def __init__(self, section, config):
        self.section = section
        self.config = config

    def _config(self, tree=None, indent=0, indent_step=1):
        if not tree:
            tree = {self.section: self.config}
        return convert_config_tree_to_list(tree, indent, indent_step)

    def __iter__(self):
        for line in self._config():
            yield line

    def __eq__(self, other):
        if isinstance(other, type(self)) and {self.section: self.config} == {other.section: other.config}:
            return True
        return False


class ConfigSection:
    def __init__(self, raw_config):
        self.raw_config = raw_config

    def __iter__(self):
        for line in self.raw_config:
            yield line

    def __eq__(self, other):
        if isinstance(other, type(self)) and self.raw_config == other.raw_config:
            return True
        return False
