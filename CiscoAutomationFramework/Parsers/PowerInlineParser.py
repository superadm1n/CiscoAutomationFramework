
interface_abbrivs = ('fa', 'gi', 'te', 'fo', 'eth')


class PowerInlineInterface:

    def __init__(self, interface_data):
        self._interface_data = interface_data

    @property
    def name(self):
        return self._interface_data.split()[0]

    @property
    def admin(self):
        return self._interface_data.split()[1]

    @property
    def oper(self):
        return self._interface_data.split()[2]

    @property
    def watts(self):
        return float(self._interface_data.split()[3])

    @property
    def detected_device(self):
        return ' '.join(self._interface_data.split()[4:-2])

    @property
    def poe_class(self):
        return self._interface_data.split()[-2]

    @property
    def max_watts(self):
        return float(self._interface_data.split()[-1])


class PowerInlineParser:

    def __init__(self, sh_power_inline):
        self._data = sh_power_inline

    @property
    def interfaces(self):
        return [PowerInlineInterface(line)
                for line in self._data if any([line.lower().startswith(x) for x in interface_abbrivs])]

