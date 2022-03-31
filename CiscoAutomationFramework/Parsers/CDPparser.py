
class CDPEntry:

    def __init__(self, entry_data):
        self._data = entry_data

    @property
    def device_id(self):
        for line in self._data:
            if line.lower().startswith('device id'):
                return line.split(':')[1].strip()

    @property
    def ip_address(self):
        for line in self._data:
            if 'ip' in line.lower() and 'address' in line.lower():
                return line.split(':')[1].strip()

    @property
    def platform(self):
        for line in self._data:
            if line.lower().startswith('platform'):
                return line.split(':')[1].split(',')[0].strip()

    @property
    def local_interface(self):
        for line in self._data:
            if line.lower().startswith('interface') and 'address' not in line:
                return line.split(':')[1].split(',')[0].strip()

    @property
    def remote_interface(self):
        for line in self._data:
            if line.lower().startswith('interface') and 'address' not in line:
                return line.split(':')[-1].strip()

    @property
    def version(self):
        for index, line in enumerate(self._data):
            if line.lower().startswith('version:'):
                return self._data[index+1]

class CDPparser:

    def __init__(self, raw_cdp_data):
        if type(raw_cdp_data) is not list:
            raw_cdp_data.splitlines()
        self.raw_cdp_data = raw_cdp_data[2:-2]

    @property
    def _entries(self):
        all_sections = []
        section = []
        for line in self.raw_cdp_data:
            if line.startswith('---------'):
                if section:
                    all_sections.append(section)
                    section = []
                continue
            section.append(line)
        if section:
            all_sections.append(section)
        return all_sections

    @property
    def number_of_entries(self):
        return len(self.cdp_entries)

    @property
    def cdp_entries(self):
        return [CDPEntry(x) for x in self._entries]