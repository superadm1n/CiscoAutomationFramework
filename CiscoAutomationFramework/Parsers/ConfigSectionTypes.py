'''
Copyright 2021 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


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
