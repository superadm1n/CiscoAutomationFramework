class CDPparser:

    def __init__(self, raw_cdp_data):
        if type(raw_cdp_data) is not list:
            raw_cdp_data.splitlines()
        self.raw_cdp_data = raw_cdp_data[2:-2]

    def _entry_device_id(self, section_data):
        for line in section_data:
            if line.lower().startswith('device id'):
                return line.split(':')[1].strip()

    def _entry_ip_address(self, section_data):
        for line in section_data:
            if 'ip' in line.lower() and 'address' in line.lower():
                return line.split(':')[1].strip()

    def _entry_platform(self, section_data):
        for line in section_data:
            if line.lower().startswith('platform'):
                return line.split(':')[1].split(',')[0].strip()

    def _entry_local_interface(self, section_data):
        for line in section_data:
            if line.lower().startswith('interface') and 'address' not in line:
                return line.split(':')[1].split(',')[0].strip()

    def _entry_remote_interface(self, section_data):
        for line in section_data:
            if line.lower().startswith('interface') and 'address' not in line:
                return line.split(':')[-1].strip()

    def _entry_version(self, section_data):
        for index, line in enumerate(section_data):
            if line.lower().startswith('version:'):
                return section_data[index+1]

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
        data = []
        for sec in self._entries():
            data.append({'device_id': self._entry_device_id(sec), 'ip_address': self._entry_ip_address(sec),
                         'platform': self._entry_platform(sec), 'local_interface': self._entry_local_interface(sec),
                         'remote_interface': self._entry_remote_interface(sec), 'version': self._entry_version(sec)})
        return data