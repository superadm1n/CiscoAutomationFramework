from unittest import TestCase
from CiscoAutomationFramework.Parsers.IpDeviceTrackingParser import DeviceTrackingOutputParser, EntryParser

canned_output = """Global IP Device Tracking for clients = Enabled
Global IP Device Tracking Probe Count = 3
Global IP Device Tracking Probe Interval = 30
Global IP Device Tracking Probe Delay Interval = 0
-----------------------------------------------------------------------------------------------
  IP Address    MAC Address   Vlan  Interface           Probe-Timeout      State    Source
-----------------------------------------------------------------------------------------------
10.17.5.24      a4bc.31a9.b73f 17   GigabitEthernet1/0/10  30              ACTIVE   ARP
10.17.5.25      4c1c.32a8.3d98 17   GigabitEthernet1/0/9   30              ACTIVE   ARP
10.14.5.11      69c2.6355.ebe2 14   GigabitEthernet1/0/23  30              ACTIVE   ARP
10.17.5.14      9053.74f0.74b9 17   GigabitEthernet1/0/12  30              ACTIVE   ARP
169.254.83.20   8661.bf9e.c2a4 17   GigabitEthernet1/0/17  30              ACTIVE   ARP

Total number interfaces enabled: 24
Enabled interfaces:
  Gi1/0/1, Gi1/0/2, Gi1/0/3, Gi1/0/4, Gi1/0/5, Gi1/0/6, Gi1/0/7,
  Gi1/0/8, Gi1/0/9, Gi1/0/10, Gi1/0/11, Gi1/0/12, Gi1/0/13, Gi1/0/14,
  Gi1/0/15, Gi1/0/16, Gi1/0/17, Gi1/0/18, Gi1/0/19, Gi1/0/20, Gi1/0/21,
  Gi1/0/22, Gi1/0/23, Gi1/0/24
hosthame#"""


class TestOutputParser(TestCase):

    def setUp(self) -> None:
        self.parser = DeviceTrackingOutputParser(canned_output.splitlines())

    def test_accepts_string_or_list(self):
        l_parser = DeviceTrackingOutputParser(canned_output.splitlines())
        s_parser = DeviceTrackingOutputParser(canned_output)

        self.assertEqual(type(l_parser.output), list)
        self.assertEqual(type(s_parser.output), list)

    def test_returns_entry_parsers(self):
        test = all([isinstance(x, EntryParser) for x in self.parser.entries])
        self.assertEqual(test, True)

    def test_returns_proper_number(self):
        self.assertEqual(len(self.parser.entries), 5)


class TestEntryParser(TestCase):
    non_apipa_entry = '10.17.5.14      9053.74f0.74b9 17   GigabitEthernet1/0/12  30              ACTIVE   ARP'
    apipa_entry = '169.254.83.20   8661.bf9e.c2a4 17   GigabitEthernet1/0/17  30              ACTIVE   ARP'

    def setUp(self) -> None:
        self.non_apipa = EntryParser(self.non_apipa_entry)
        self.apipa = EntryParser(self.apipa_entry)

    def test_detects_apipa_properly(self):
        self.assertEqual(self.apipa.is_apipa, True)
        self.assertEqual(self.non_apipa.is_apipa, False)

    def test_extracts_ip(self):
        self.assertEqual(self.non_apipa.ip_address, '10.17.5.14')

    def test_extracts_mac(self):
        self.assertEqual(self.non_apipa.mac_address, '9053.74f0.74b9')

    def test_extracts_vlan(self):
        self.assertEqual(self.non_apipa.vlan, '17')

    def test_extracts_interface(self):
        self.assertEqual(self.non_apipa.interface, 'GigabitEthernet1/0/12')

    def test_extracts_probe_timeout(self):
        self.assertEqual(self.non_apipa.probe_timeout, '30')

    def test_extracts_state(self):
        self.assertEqual(self.non_apipa.state, 'ACTIVE')

    def test_extracts_source(self):
        self.assertEqual(self.non_apipa.source, 'ARP')



