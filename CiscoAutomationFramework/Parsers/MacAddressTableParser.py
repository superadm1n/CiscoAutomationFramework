
interface_abbrivs = ('fa', 'gi', 'te', 'fo', 'eth', 'po')


class MacAddressTableInterface:

    def __init__(self, name, mac_addresses):
        self._name = name
        self._mac_addresses = mac_addresses

    @property
    def name(self):
        return self._name

    @property
    def mac_addresses(self):
        return self._mac_addresses

    @property
    def num_of_macs(self):
        return len(self._mac_addresses)

    def has_mac(self, mac):
        return mac in self.mac_addresses

    def __repr__(self):
        return f'{type(self).__name__}({self.name}, num_of_macs: {self.num_of_macs})'


class MacAddressTableParser:

    def __init__(self, mac_address_table):
        self._table = mac_address_table

    @property
    def is_nexus(self):
        """Searches the entire mac address table, checking if any of a set of keywords
        are in it"""
        table_as_string = ' '.join(self._table).lower()
        key_words = ['legend', 'vpc', 'peer']
        if any([word in table_as_string for word in key_words]):
            return True
        return False

    def _extract_mac(self, line):
        """
        The MAC address on IOS is displayed in the 2nd column
         All    0100.0ccc.cccc    STATIC      CPU

        and on Nexus platform it is displayed in the 3rd column
        *    1     aaaa.bbbb.cccc   dynamic  0         F      F    Eth1/18

        so handle accordingly
        """
        if self.is_nexus:
            return line.split()[2]
        return line.split()[1]

    def _extract_interface(self, line):
        """
        The interface is displayed in the last column of output for both IOS and NXOS based on the
        systems I have used, No need to handle differently
        """
        return line.split()[-1]

    def _line_is_good_data(self, line):
        if self.is_nexus:
            if len(line.split()) == 8 and any(x in line.split()[-1].lower() for x in interface_abbrivs):
                return True
        else:
            if len(line.split()) == 4 and any(x in line.split()[-1].lower() for x in interface_abbrivs):
                return True
        return False

    def _parse(self):
        data = {}
        for line in self._table:
            # make sure we dont try to parse part of the header, a separator line, blank lines, or anything
            # that is not a mac address entry
            if not self._line_is_good_data(line):
                continue
            interface = self._extract_interface(line)
            mac = self._extract_mac(line)
            if any(interface.lower().startswith(x) for x in interface_abbrivs):
                if interface in data.keys():
                    data[interface].append(mac)
                else:
                    data[interface] = [mac]
        return data

    @property
    def table_entries(self):
        return [MacAddressTableInterface(interface, mac_addresses) for interface, mac_addresses in self._parse().items()]
