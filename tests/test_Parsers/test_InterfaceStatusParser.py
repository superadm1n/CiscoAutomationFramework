from unittest import TestCase
from CiscoAutomationFramework.Parsers.InterfaceStatusParser import InterfaceStatusOutputParser, LineParser

canned_output = """show int desc
Gi1/0/45  single_desc       connected    16         a-full a-1000 10/100/1000BaseTX
Gi1/0/46  multi description connected    trunk      a-full a-1000 10/100/1000BaseTX
Gi1/0/47  single_desc       connected    16         a-full a-1000  Not Present
Gi1/0/48  multi description connected    trunk      a-full a-1000  Not Present
devicehostname#
"""


class InterfaceStatusOutputParserTests(TestCase):

    def setUp(self) -> None:
        self.parser = InterfaceStatusOutputParser(canned_output.splitlines())

    def test_splits_a_string_by_lines(self):
        parser = InterfaceStatusOutputParser(canned_output)
        self.assertEqual(type(parser.raw_table), list)

    def test_accepts_list(self):
        self.assertEqual(type(self.parser.raw_table), list)

    def test_returns_line_parsers(self):
        all_parsers = all([isinstance(x, LineParser) for x in self.parser.interfaces])
        self.assertEqual(all_parsers, True)

    def test_returns_proper_number(self):
        num = len(self.parser.interfaces)
        self.assertEqual(num, 4)


class LineParserTests(TestCase):
    def setUp(self) -> None:
        self.single_desc_present = LineParser('Gi1/0/45  single_desc       connected    16         a-full a-1000 10/100/1000BaseTX')
        self.multi_desc_present = LineParser('Gi1/0/46  multi description connected    trunk      a-full a-1000 10/100/1000BaseTX')
        self.single_desc_no_present = LineParser('Gi1/0/47  single_desc       connected    16         a-full a-1000  Not Present')
        self.multi_desc_no_present = LineParser('Gi1/0/48  multi description connected    trunk      a-full a-1000  Not Present')

    def test_single_desc_present(self):
        self.assertEqual(self.single_desc_present.name, 'Gi1/0/45')
        self.assertEqual(self.single_desc_present.description, 'single_desc')
        self.assertEqual(self.single_desc_present.status, 'connected')
        self.assertEqual(self.single_desc_present.vlan, '16')
        self.assertEqual(self.single_desc_present.duplex, 'a-full')
        self.assertEqual(self.single_desc_present.speed, 'a-1000')
        self.assertEqual(self.single_desc_present.type, '10/100/1000BaseTX')

    def test_multi_desc_present(self):
        self.assertEqual(self.multi_desc_present.name, 'Gi1/0/46')
        self.assertEqual(self.multi_desc_present.description, 'multi description')
        self.assertEqual(self.multi_desc_present.status, 'connected')
        self.assertEqual(self.multi_desc_present.vlan, 'trunk')
        self.assertEqual(self.multi_desc_present.duplex, 'a-full')
        self.assertEqual(self.multi_desc_present.speed, 'a-1000')
        self.assertEqual(self.multi_desc_present.type, '10/100/1000BaseTX')

    def test_single_desc_no_present(self):
        self.assertEqual(self.single_desc_no_present.name, 'Gi1/0/47')
        self.assertEqual(self.single_desc_no_present.description, 'single_desc')
        self.assertEqual(self.single_desc_no_present.status, 'connected')
        self.assertEqual(self.single_desc_no_present.vlan, '16')
        self.assertEqual(self.single_desc_no_present.duplex, 'a-full')
        self.assertEqual(self.single_desc_no_present.speed, 'a-1000')
        self.assertEqual(self.single_desc_no_present.type, 'Not Present')

    def test_multi_desc_no_present(self):
        self.assertEqual(self.multi_desc_no_present.name, 'Gi1/0/48')
        self.assertEqual(self.multi_desc_no_present.description, 'multi description')
        self.assertEqual(self.multi_desc_no_present.status, 'connected')
        self.assertEqual(self.multi_desc_no_present.vlan, 'trunk')
        self.assertEqual(self.multi_desc_no_present.duplex, 'a-full')
        self.assertEqual(self.multi_desc_no_present.speed, 'a-1000')
        self.assertEqual(self.multi_desc_no_present.type, 'Not Present')

    def test_no_description_not_present(self):
        parser = LineParser('Gi1/0/48                    connected    trunk      a-full a-1000  Not Present')
        self.assertEqual(parser.name, 'Gi1/0/48')
        self.assertEqual(parser.description, '')
        self.assertEqual(parser.status, 'connected')
        self.assertEqual(parser.vlan, 'trunk')
        self.assertEqual(parser.duplex, 'a-full')
        self.assertEqual(parser.speed, 'a-1000')
        self.assertEqual(parser.type, 'Not Present')

    def test_no_description_present(self):
        parser = LineParser('Gi1/0/48                    connected    trunk      a-full a-1000 10/100/1000BaseTX')
        self.assertEqual(parser.name, 'Gi1/0/48')
        self.assertEqual(parser.description, '')
        self.assertEqual(parser.status, 'connected')
        self.assertEqual(parser.vlan, 'trunk')
        self.assertEqual(parser.duplex, 'a-full')
        self.assertEqual(parser.speed, 'a-1000')
        self.assertEqual(parser.type, '10/100/1000BaseTX')







