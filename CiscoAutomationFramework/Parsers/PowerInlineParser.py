
interface_abbrivs = ('fa', 'gi', 'te', 'fo', 'eth')


class PowerInlineInterface:

    def __init__(self, interface_data):
        self._interface_data = interface_data

    @property
    def name(self):
        """
        Interface name ex. Gi1/0/5

        :return: Interface Name
        :rtype: str
        """
        return self._interface_data.split()[0]

    @property
    def admin(self):
        """
        Admin column of the entry ex. auto

        :return: Admin column
        :rtype: str
        """
        return self._interface_data.split()[1]

    @property
    def oper(self):
        """
        Oper column of the entry, off/on weather it is providing power or not

        :return: Operation status
        :rtype: str
        """
        return self._interface_data.split()[2]

    @property
    def watts(self):
        """
        Watts currently being drawn on port by connected device

        :return: Watts currently drawn
        :rtype: float
        """
        return float(self._interface_data.split()[3])

    @property
    def detected_device(self):
        """
        Detected device type of connected device

        :return: Detected device
        :rtype: str
        """
        return ' '.join(self._interface_data.split()[4:-2])

    @property
    def poe_class(self):
        """
        POE class of connected device ex. 0, 1, 2, 3, n/a

        :return: POE Class
        :rtype: str
        """
        return self._interface_data.split()[-2]

    @property
    def max_watts(self):
        """
        Max watts capable of being drawn on port

        :return: Max watts supported
        :rtype: float
        """
        return float(self._interface_data.split()[-1])


class PowerInlineParser:

    def __init__(self, sh_power_inline):
        if not isinstance(sh_power_inline, list):
            self._data = sh_power_inline.splitlines()
        else:
            self._data = sh_power_inline

        if not self.abbreviated_command.startswith('spi'):
            raise ValueError(f'The detected command {self.command} is not what is expected!')

    @property
    def abbreviated_command(self):
        return ''.join(x[0] for x in self.command.split())

    @property
    def command(self):
        return self._data[0]


    @property
    def interfaces(self):
        """
        Returns list of interfaces in the power inline table to extract the values from the entry

        :return: List of entries in the power inline table
        :rtype: list[PowerInlineInterface]
        """
        return [PowerInlineInterface(line)
                for line in self._data if any([line.lower().startswith(x) for x in interface_abbrivs])]

