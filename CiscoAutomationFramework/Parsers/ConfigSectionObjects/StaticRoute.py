from CiscoAutomationFramework.util import is_ipv4
from ipaddress import IPv4Network


class StaticRoute:

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @property
    def vrf(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if word.lower() == 'vrf':
                return data[idx+1]

    @property
    def network(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if is_ipv4(word):
                subnet = word
                mask = data[idx+1]
                return f'{subnet}/{mask}'

    @property
    def subnet(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if is_ipv4(word):
                return word

    @property
    def mask(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if is_ipv4(word):
                return data[idx + 1]

    @property
    def cidr(self):
        return str(IPv4Network(f'0.0.0.0/{self.mask}').prefixlen)

    @property
    def destination(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if is_ipv4(word):
                return data[idx + 2]

    @property
    def description(self):
        data = self.raw_data.split()
        for idx, word in enumerate(data):
            if word == 'name':
                return data[idx + 1]

