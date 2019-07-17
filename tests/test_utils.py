from unittest import TestCase
from CiscoAutomationFramework.Util import extract_version_number_iosxe, extract_version_number_ios, extract_version_number_nxos

class TestIOSVersionNumberDetection(TestCase):

    def setUp(self) -> None:
        self.expected_sh_ver_data = '''sh ver
Cisco IOS Software, C3750E Software (C3750E-IPBASEK9-M), Version 15.0(2)SE9, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2015 by Cisco Systems, Inc.
Compiled Tue 01-Dec-15 06:27 by prod_rel_team

ROM: Bootstrap program is C3750E boot loader
BOOTLDR: C3750E Boot Loader (C3750X-HBOOT-M) Version 12.2(53r)SE1, RELEASE SOFTWARE (fc1)

LIBL-1C-SW uptime is 3 years, 17 weeks, 6 days, 17 hours, 55 minutes
System returned to ROM by power-on
System restarted at 14:22:19 cst Tue Mar 8 2016
System image file is "flash:/c3750e-ipbasek9-mz.150-2.SE9/c3750e-ipbasek9-mz.150-2.SE9.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

License Level: lanbase
License Type: Permanent
Next reload license Level: lanbase

cisco WS-C3750X-48P (PowerPC405) processor (revision A0) with 262144K bytes of memory.
Processor board ID FDO1441Z0PX
Last reset from power-on
2 Virtual Ethernet interfaces
1 FastEthernet interface
208 Gigabit Ethernet interfaces
8 Ten Gigabit Ethernet interfaces
The password-recovery mechanism is enabled.
'''

    def test_detects_version_number_properly(self):
        detected_version = extract_version_number_ios(self.expected_sh_ver_data.splitlines())
        self.assertEqual('15.0(2)SE9', detected_version)

class TestIOSXEVersionNumberDetection(TestCase):

    def setUp(self) -> None:
        self.expected_sh_ver_data = '''sh ver
        Cisco IOS XE Software, Version 16.06.05
        Cisco IOS Software [Everest], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.6.5, RELEASE SOFTWARE (fc3)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2018 by Cisco Systems, Inc.
        Compiled Mon 10-Dec-18 12:52 by mcpre


        Cisco IOS-XE software, Copyright (c) 2005-2018 by cisco Systems, Inc.
        All rights reserved.  Certain components of Cisco IOS-XE software are
        licensed under the GNU General Public License ("GPL") Version 2.0.  The
        software code licensed under GPL Version 2.0 is free software that comes
        with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
        GPL code under the terms of GPL Version 2.0.  For more details, see the
        documentation or "License Notice" file accompanying the IOS-XE software,
        or the applicable URL provided on the flyer accompanying the IOS-XE
        software.


        ROM: IOS-XE ROMMON
        BOOTLDR: System Bootstrap, Version 16.8.1r [FC4], RELEASE SOFTWARE (P)

        DEVICE uptime is 13 weeks, 1 day, 10 hours, 54 minutes
        Uptime for this control processor is 13 weeks, 1 day, 10 hours, 55 minutes
        System returned to ROM by Reload Command
        System image file is "flash:packages.conf"
        Last reload reason: Reload Command



        This product contains cryptographic features and is subject to United
        States and local country laws governing import, export, transfer and
        use. Delivery of Cisco cryptographic products does not imply
        third-party authority to import, export, distribute or use encryption.
        Importers, exporters, distributors and users are responsible for
        compliance with U.S. and local country laws. By using this product you
        agree to comply with applicable laws and regulations. If you are unable
        to comply with U.S. and local laws, return this product immediately.

        A summary of U.S. laws governing Cisco cryptographic products may be found at:
        http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

        If you require further assistance please contact us by sending email to
        export@cisco.com.


        Technology Package License Information:

        -----------------------------------------------------------------
        Technology-package                   Technology-package
        Current             Type             Next reboot
        ------------------------------------------------------------------
        network-advantage   Permanent        network-advantage
        dna-advantage       Subscription     dna-advantage

        cisco C9300-48U (X86) processor with 1392780K/6147K bytes of memory.
        Processor board ID FOC2243X0C7
        3 Virtual Ethernet interfaces
        260 Gigabit Ethernet interfaces
        40 Ten Gigabit Ethernet interfaces
        10 Forty Gigabit Ethernet interfaces
        2048K bytes of non-volatile configuration memory.
        8388608K bytes of physical memory.
        1638400K bytes of Crash Files at crashinfo:.
        1638400K bytes of Crash Files at crashinfo-2:.
        11264000K bytes of Flash at flash:.
        11264000K bytes of Flash at flash-2:.
        0K bytes of WebUI ODM Files at webui:.
        1638400K bytes of Crash Files at crashinfo-3:.
        11264000K bytes of Flash at flash-3:.
        1638400K bytes of Crash Files at crashinfo-4:.
        11264000K bytes of Flash at flash-4:.

        '''

    def test_detects_version_number_properly(self):
        detected_version = extract_version_number_iosxe(self.expected_sh_ver_data.splitlines())
        self.assertEqual('16.06.05', detected_version)


class TestNXOSVersionNumberDetection(TestCase):

    def setUp(self) -> None:
        self.expected_sh_ver_data = '''sh ver
Cisco Nexus Operating System (NX-OS) Software
TAC support: http://www.cisco.com/tac
Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
Copyright (c) 2002-2013, Cisco Systems, Inc. All rights reserved.
The copyrights to certain works contained herein are owned by
other third parties and are used and distributed under license.
Some parts of this software are covered under the GNU Public
License. A copy of the license is available at
http://www.gnu.org/licenses/gpl.html.

Software
  BIOS:      version 3.6.0
  loader:    version N/A
  kickstart: version 5.2(1)N1(4)
  system:    version 5.2(1)N1(4)
  power-seq: Module 1: version v5.0
  uC:        version v1.0.0.2
  SFP uC:    Module 1: v1.0.0.0
  BIOS compile time:       05/09/2012
  kickstart image file is: bootflash:///n5000-uk9-kickstart.5.2.1.N1.4.bin
  kickstart compile time:  3/19/2013 3:00:00 [03/19/2013 05:12:59]
  system image file is:    bootflash:///n5000-uk9.5.2.1.N1.4.bin
  system compile time:     3/19/2013 3:00:00 [03/19/2013 07:10:47]


Hardware
  cisco Nexus5596 Chassis ("O2 48X10GE/Modular Supervisor")
  Intel(R) Xeon(R) CPU         with 8263848 kB of memory.
  Processor Board ID FOC17040FQJ

  Device name: DEVICE
  bootflash:    2007040 kB

Kernel uptime is 1110 day(s), 10 hour(s), 18 minute(s), 2 second(s)

Last reset
  Reason: Unknown
  System version: 5.2(1)N1(4)
  Service:
'''

    def test_detects_version_number_properly(self):
        detected_version = extract_version_number_nxos(self.expected_sh_ver_data.splitlines())
        self.assertEqual('5.2(1)N1(4)', detected_version)