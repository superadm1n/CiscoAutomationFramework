from socket import inet_aton, error

__all__ = ['RoutingTableParser', 'Route', 'NexusRoute', 'IOSRoute']


def is_ip(string):
    # Must have 3 periods for ipv4 address
    num_periods = len([x for x in string if x == '.'])
    if num_periods != 3:
        return False
    # must be at least 7 characters (4 digits and 3 periods)
    if len(string) < 7:
        return False

    # rest of checking can be handled here
    try:
        inet_aton(string)
        return True
    except error:
        return False


class Route:
    def __init__(self, routing_table_entry):
        self.data = routing_table_entry


class NexusRoute(Route):

    @property
    def subnet(self):
        return self.data.split(',')[0].split('/')[0]

    @property
    def cidr(self):
        return self.data.split(',')[0].split('/')[1]

    @property
    def next_hops(self):
        ips = []
        for line in self.data.split('|')[1:]:
            ips.append(line.split()[1].replace(',', ''))

        return ips

    def tag(self, hop):
        for line in self.data.split('|'):
            if hop in line:
                for word in line.split(','):
                    if 'tag' in word.lower():
                        return line.split()[-1]
        return ''

    def preference(self, hop):
        for line in self.data.split('|'):
            if hop in line:
                for word in line.split(','):
                    if '[' in word:
                        return word.split('/')[0].replace('[', '').replace(']', '').strip()
        return ''

    def metric(self, hop):
        for line in self.data.split('|'):
            if hop in line:
                for word in line.split(','):
                    if '[' in word:
                        return word.split('/')[1].replace('[', '').replace(']', '').strip()
        return ''

    def __repr__(self):
        return f'{type(self).__name__}(Subnet: {self.subnet}/{self.cidr}, Num Next Hop:{len(self.next_hops)})'


class IOSRoute(Route):

    def _get_next_hops(self, flag_count=1):
        ips = []
        count = 0
        for line in self.data.split('|'):
            for word in line.split():
                word = word.replace(',', '')
                if is_ip(word):
                    count += 1
                if count > flag_count and is_ip(word):
                    ips.append(word)
        return ips


    @property
    def _subnet_with_cidr(self):
        for section in self.data.split():
            if is_ip(section.split('/')[0]):
                return section

    @property
    def subnet(self):
        return self._subnet_with_cidr.split('/')[0]

    @property
    def cidr(self):
        subnet_and_cidr = self._subnet_with_cidr.split('/')
        if len(subnet_and_cidr) < 2:
            return '32'
        else:
            return subnet_and_cidr[1]

    @property
    def next_hops(self):
        """
        Iterate over data, grabbing every IP address after the first (first one is the subnet) and excluding
        the address if 'subnetted' is in the same line of output which would not be a hop
        """
        ips = []
        count = 0
        for line in self.data.split('|'):
            for word in line.split():
                # remove any commas and if there is a CIDR notation, remove that
                word = word.replace(',', '')
                word = word.split('/')[0]
                if is_ip(word):
                    count += 1

                # if "subnetted" is in the line, it is notifying that the following output is a subnets of supernet
                # which means that the address in the line can be disregarded
                if count > 1 and is_ip(word) and 'subnetted' not in line:
                    ips.append(word)

        return ips

    def tag(self, hop):
        return ''

    def preference(self, hop):
        for line in self.data.split(','):
            if hop in line:
                return line.split('[')[1].split('/')[0]
        return ''

    def metric(self, hop):
        for line in self.data.split(','):
            if hop in line:
                return line.split(']')[0].split('/')[1]
        return ''

    def __repr__(self):
        return f'{type(self).__name__}(Subnet: {self.subnet}/{self.cidr})'


class RoutingTableParser:
    def __init__(self, raw_routing_table, is_nexus=False):
        if is_nexus:
            self._raw_data = self._parse_out_header_nexus(raw_routing_table)
        else:
            self._raw_data = self._parse_out_header_ios(raw_routing_table)
        self._is_nexus = is_nexus

    def _parse_out_header_ios(self, data):
        return_data = []
        flag = False
        for line in data:
            if 'gateway' in line.lower():
                flag = True
                continue
            if flag is True:
                return_data.append(line)
        return return_data

    def _parse_out_header_nexus(self, data):
        return_data = []
        flag = False
        for line in data:
            if line == '':
                flag = True
                continue
            if flag is True:
                return_data.append(line)

        return return_data

    def _str_startswith_char(self, string):
        if len(string) > 0:
            if string[0].isalnum():
                return True
        return False

    @property
    def structured_data(self):
        rightsized_lines = []
        tmp = ''
        for line in self._raw_data:
            if self._str_startswith_char(line):
                if tmp:
                    rightsized_lines.append(tmp)
                tmp = line
            else:
                if line:
                    tmp += f' |{line.strip()}'
        if tmp:
            rightsized_lines.append(tmp)
        return rightsized_lines

    @property
    def routes(self):
        if self._is_nexus:
            return [NexusRoute(x) for x in self.structured_data]
        else:
            return [IOSRoute(x) for x in self.structured_data]
