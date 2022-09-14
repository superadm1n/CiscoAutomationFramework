from CiscoAutomationFramework.util import is_ipv4


class EntryParser:

    def __init__(self, entry_data):
        if not type(entry_data) == list:
            self.data = entry_data.split()
        else:
            self.data = entry_data

    @property
    def is_apipa(self):
        """
        True/False if the IP address in the entry is an APIPA address.

        :return: True/False
        :rtype: bool
        """
        return self.ip_address.startswith('169.254')

    @property
    def ip_address(self):
        """
        IP address of the IP device tracking entry

        :return: IP address
        :rtype: str
        """
        return self.data[0]

    @property
    def mac_address(self):
        """

        :return: MAC Address
        :rtype: str
        """
        return self.data[1]

    @property
    def vlan(self):
        """

        :return: Vlan
        :rtype: str
        """
        return self.data[2]

    @property
    def interface(self):
        """

        :return: Switch Interface
        :rtype: str
        """
        return self.data[3]

    @property
    def probe_timeout(self):
        """

        :return: Probe Timeout
        :rtype: str
        """
        return self.data[4]

    @property
    def state(self):
        """

        :return: State
        :rtype: str
        """
        return self.data[5]

    @property
    def source(self):
        """

        :return: Source
        :rtype: str
        """
        return self.data[6]


class DeviceTrackingOutputParser:

    def __init__(self, output_from_device):
        if not type(output_from_device) == list:
            self.output = output_from_device.splitlines()
        else:
            self.output = output_from_device

    @property
    def entries(self):
        """
        Extracts the entires from the table and returns them as a list
        :return: List of table entries as EntryParser instances
        :rtype: list[EntryParser]
        """
        data = []
        for line in self.output:
            line = line.split()
            if len(line) < 1:
                continue
            if not is_ipv4(line[0]):
                continue
            data.append(EntryParser(line))
        return data


