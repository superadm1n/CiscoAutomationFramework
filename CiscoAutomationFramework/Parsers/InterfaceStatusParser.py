class LineParser:
    def __init__(self, raw_line):
        self.raw_line = raw_line
        self.index_offset = -1 if self.not_present else 0

    @property
    def not_present(self):
        """
        Returns True/False if the text "not present" in the lowercase line

        :return: True/False
        :rtype: bool
        """
        return 'not present' in self.raw_line.lower()

    @property
    def name(self):
        """
        Name of the interface ex. Gi1/0/1

        :return: Interface Name abbriviated
        :rtype: str
        """
        return self.raw_line.split()[0]

    @property
    def type(self):
        """
        Interface Type ex. 10/100/1000BaseTX, Not Present

        :return: Interface Type
        :rtype: str
        """
        if self.not_present:
            return ' '.join(self.raw_line.split()[-2:])
        return self.raw_line.split()[-1]

    @property
    def speed(self):
        """
        Interface Operating Speed ex. auto, a-100, a-1000

        :return: Interface Speed
        :rtype: str
        """
        return self.raw_line.split()[-2+self.index_offset]

    @property
    def duplex(self):
        """
        Interface duplex settings ex. auto, a-full a-half

        :return: Duplex Setting
        :rtype: str
        """
        return self.raw_line.split()[-3 + self.index_offset]

    @property
    def vlan(self):
        """
        Vlan configuration of interface ex. 1, 100, trunk, routed

        :return: vlan configuration
        :rtype: str
        """
        return self.raw_line.split()[-4 + self.index_offset]

    @property
    def status(self):
        """
        Status of interface ex. connected, notconnected, disabled, err-disable, etc

        :return: interface status
        :rtype: str
        """
        return self.raw_line.split()[-5 + self.index_offset]

    @property
    def description(self):
        """
        Description set on interface

        :return: Confiured Description
        :rtype: str
        """

        return ' '.join(self.raw_line.split()[1:-5 + self.index_offset])


class InterfaceStatusOutputParser:
    """
    Provide the output directly from the device after issuing the command 'show interface status' to
    this object to parse it
    """
    interface_beginnings = ('fa', 'gi', 'te', 'fo')

    def __init__(self, raw_table):
        if not isinstance(raw_table, list):
            self.raw_table = raw_table.split()
        else:
            self.raw_table = raw_table

    @property
    def interfaces(self):
        """
        Parses the raw output from the command and provides a list of all entries from the table

        :return: LineParser
        :rtype: list[LineParser]
        """
        data = []
        for line in self.raw_table:
            if any([line.lower().startswith(x) for x in self.interface_beginnings]) and len(line.split()) > 3:
                data.append(LineParser(line))
        return data
