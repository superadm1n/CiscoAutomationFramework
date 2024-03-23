

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
