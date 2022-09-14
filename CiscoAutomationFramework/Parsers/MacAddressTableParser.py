class MacEntryParser:
    def __init__(self, raw_entry):
        self.raw_entry = raw_entry
        self.split_entry = raw_entry.split()

    @property
    def is_nexus(self):
        """Searches the entire mac address table, checking if any of a set of keywords
        are in it"""
        return len(self.split_entry) > 4

    @property
    def mac_address(self):
        """
        MAC address from the row

        :return: MAC Address
        :rtype: str
        """
        if self.is_nexus:
            return self.split_entry[2]
        return self.split_entry[1]

    @property
    def vlan(self):
        """
         Vlan from the row

        :return: Vlan
        :rtype: str
        """
        if self.is_nexus:
            return self.split_entry[1]
        return self.split_entry[0]

    @property
    def type(self):
        """
        Address type from the row ex. dynamic, static

        :return: Address Type
        :rtype: str
        """
        if self.is_nexus:
            return self.split_entry[3]
        return self.split_entry[2]

    @property
    def interface(self):
        """
        Interface on device that the MAC address is on ex. Gi1/0/8

        :return: Interface on Device
        :rtype: str
        """
        return self.split_entry[-1]


class MacAddressTableParser:
    def __init__(self, raw_table):
        if isinstance(raw_table, str):
            self.table = raw_table.splitlines()
        else:
            self.table = raw_table

        if not self.abbreviated_command.startswith('sma'):
            raise ValueError(f'The detected command {self.command} is not what is expected!')

    @property
    def is_nexus(self):
        """
        Checks the raw table for specific key words to determine if it is a Nexus platform or not returning
        True if it is False if it is not

        :return: True/False
        :rtype: bool
        """
        table_as_string = ' '.join(self.table).lower()
        key_words = ['legend', 'vpc', 'peer']
        if any([word in table_as_string for word in key_words]):
            return True
        return False

    @property
    def abbreviated_command(self):
        return ''.join(x[0] for x in self.command.split())

    @property
    def command(self):
        return self.table[0]

    def _is_mac(self, x):
        avail_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        x = x.replace('.', '')
        if len(x) != 12:
            return False
        for char in x:
            if char.lower() not in avail_chars:
                return False
        return True

    def _mac_in_line(self, line):
        for section in line.split():
            if self._is_mac(section):
                return True
        return False

    @property
    def table_entries(self):
        """
        Parses the mac address table and returns a list of the entries

        :return: List of entries from the MAC address table
        :rtype: list[MacEntryParser]
        """
        data = []
        for line in self.table:
            if self._mac_in_line(line):
                data.append(MacEntryParser(line))
        return data

