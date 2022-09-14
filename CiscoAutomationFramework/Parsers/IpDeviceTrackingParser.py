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
        MAC address of the ip device tracking entry

        :return: MAC Address
        :rtype: str
        """
        return self.data[1]

    @property
    def vlan(self):
        """
        Extracts vlan of the ip device tracking entry

        :return: Vlan
        :rtype: str
        """
        return self.data[2]

    @property
    def interface(self):
        """
        Extracts interface of the ip device tracking entry

        :return: Switch Interface
        :rtype: str
        """
        return self.data[3]

    @property
    def probe_timeout(self):
        """
        Extracts probe timeout of the ip device tracking entry

        :return: Probe Timeout
        :rtype: str
        """
        return self.data[4]

    @property
    def state(self):
        """
        Extracts state of the ip device tracking entry

        :return: State
        :rtype: str
        """
        return self.data[5]

    @property
    def source(self):
        """
        Extracts source of the ip device tracking entry

        :return: Source
        :rtype: str
        """
        return self.data[6]


class DeviceTrackingOutputParser:

    def __init__(self, output_from_device):
        """
        Provide the raw output from the device, if getting directly from the frameworks get_output() methods
        it will contain everything needed, but if not, make sure the first line of output is the command that
        was entered, abbreviated for is ok (show ip device tracking all, sh ip de tr all)

        :param output_from_device: raw output from device, first line is command entered to get output
        :type output_from_device: Union[list, str]
        """
        if not type(output_from_device) == list:
            self.output = output_from_device.splitlines()
        else:
            self.output = output_from_device

        if not self.abbreviated_command.startswith('sidta'):
            raise ValueError(f'The detected command {self.command} is not what is expected!')

    @property
    def abbreviated_command(self):
        return ''.join(x[0] for x in self.command.split())

    @property
    def command(self):
        return self.output[0]

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


