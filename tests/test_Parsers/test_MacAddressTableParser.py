from unittest import TestCase
from CiscoAutomationFramework.Parsers.MacAddressTableParser import MacAddressTableParser, MacEntryParser

canned_output_nexus = """sh mac address-table
Legend:
        * - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
        age - seconds since last seen,+ - primary entry using vPC Peer-Link,
        (T) - True, (F) - False, C - ControlPlane MAC, ~ - vsan
   VLAN     MAC Address      Type      age     Secure NTFY Ports
---------+-----------------+--------+---------+------+----+------------------
+    1     8459.5281.8d3e   dynamic  0         F      F    Po401
+    1     1bb7.341f.6167   dynamic  0         F      F    Po401
+    1     8d55.9a37.ecf4   dynamic  0         F      F    Po313
+    1     f2e9.8567.a852   dynamic  0         F      F    Po313
+    1     7383.63f9.1c79   dynamic  0         F      F    Po311
+    1     a9ca.324a.b181   dynamic  0         F      F    Po311
+    1     4699.6131.767a   dynamic  0         F      F    Po307
+    1     5e86.615b.ab92   dynamic  0         F      F    Po307
+    1     655c.144b.acef   dynamic  0         F      F    Po310
+    1     3fb2.abbd.77f1   dynamic  0         F      F    Po310
+    1     6d1f.80bf.7e99   dynamic  0         F      F    Po303
+    1     1ade.ecfa.7a90   dynamic  0         F      F    Po303
+    1     4c7e.54ab.776c   dynamic  0         F      F    Po312
+    1     dc4d.db7f.3ab8   dynamic  0         F      F    Po312
+    1     4733.2a95.11ee   dynamic  0         F      F    Po302
+    1     2fe9.b280.a886   dynamic  0         F      F    Po302
+    1     6dcc.c368.6316   dynamic  0         F      F    Po305
+    1     f3cf.5a51.99cc   dynamic  0         F      F    Po305
+    1     4c65.3455.80ef   dynamic  0         F      F    Po306
+    1     39cb.bc7a.bcf0   dynamic  0         F      F    Po306
+    1     5952.d79c.715c   dynamic  0         F      F    Po308

devicehostname#
"""
canned_output_ios = """sh mac address-table
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
 All    dc82.f363.2731    STATIC      CPU
 All    634f.dc9f.6260    STATIC      CPU
 All    bd88.cdda.a0fb    STATIC      CPU
   1    bbb8.fbf9.cfbc    STATIC      Gi1/0/23
   1    f029.be44.356f    STATIC      Gi1/0/37
   1    261b.3ac2.f8a5    DYNAMIC     Gi1/0/45
   1    1891.7e41.60d2    STATIC      Gi1/0/44
   1    8a5a.6934.9f67    STATIC      Gi1/0/22
   1    c8c0.8d80.2a9c    DYNAMIC     Gi1/0/48
   1    a98e.23a8.76bd    DYNAMIC     Gi1/0/45
   1    c269.4db1.8eca    DYNAMIC     Te1/0/1
   1    376a.875a.90f7    STATIC      Gi1/0/43
devicehostname#
"""


class InterfaceStatusOutputParserTests(TestCase):

    def setUp(self) -> None:
        self.ios_parser = MacAddressTableParser(canned_output_ios.splitlines())
        self.nexus_parser = MacAddressTableParser(canned_output_nexus.splitlines())

    def test_splits_a_string_by_lines(self):
        parser = MacAddressTableParser(canned_output_ios)
        self.assertEqual(type(parser.table), list)

    def test_returns_mac_parsers(self):
        all_parsers = all([isinstance(x, MacEntryParser) for x in self.ios_parser.table_entries])
        self.assertEqual(all_parsers, True)

    def test_returns_proper_number(self):
        iosnum = len(self.ios_parser.table_entries)
        nexusnum = len(self.nexus_parser.table_entries)
        self.assertEqual(iosnum, 12)
        self.assertEqual(nexusnum, 21)

    def test_detects_nexus(self):
        self.assertEqual(self.nexus_parser.is_nexus, True)

    def test_knows_ios_not_nexus(self):
        self.assertEqual(self.ios_parser.is_nexus, False)


class LineParserTests(TestCase):
    def setUp(self) -> None:
        self.ios_entry = MacEntryParser('   1    f029.be44.356f    STATIC      Gi1/0/23')
        self.nexus_entry = MacEntryParser('*    2     c269.4db1.8eca   dynamic  0         F      F    Eth1/48')

    def test_extracts_vlan(self):
        self.assertEqual(self.ios_entry.vlan, '1')
        self.assertEqual(self.nexus_entry.vlan, '2')

    def test_extracts_mac(self):
        self.assertEqual(self.ios_entry.mac_address, 'f029.be44.356f')
        self.assertEqual(self.nexus_entry.mac_address, 'c269.4db1.8eca')

    def test_extracts_type(self):
        self.assertEqual(self.ios_entry.type, 'STATIC')
        self.assertEqual(self.nexus_entry.type, 'dynamic')

    def test_extracts_interface(self):
        self.assertEqual(self.ios_entry.interface, 'Gi1/0/23')
        self.assertEqual(self.nexus_entry.interface, 'Eth1/48')

    def test_detects_nexus(self):
        self.assertEqual(self.nexus_entry.is_nexus, True)

    def test_knows_ios_not_nexus(self):
        self.assertEqual(self.ios_entry.is_nexus, False)




