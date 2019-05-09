show_interfaces = '''show interfaces
Vlan2100 is up, line protocol is up
  Hardware is EtherSVI, address is 5057.a834.7fc1 (bia 5057.a834.7fc1)
  Internet address is 10.210.0.16/23
  MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not supported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 6000 bits/sec, 8 packets/sec
  5 minute output rate 1000 bits/sec, 1 packets/sec
     938760915 packets input, 90404749479 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     405103488 packets output, 96533474773 bytes, 0 underruns
     0 output errors, 2 interface resets
     0 output buffer failures, 0 output buffers swapped out
FastEthernet0 is administratively down, line protocol is down
  Hardware is PowerPC405 FastEthernet, address is 5057.a834.7fb7 (bia 5057.a834.7fb7)
  MTU 1500 bytes, BW 100000 Kbit, DLY 100 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive not set
  Unknown duplex, Unknown Speed, MII
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/0 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     0 packets input, 0 bytes
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog
     0 input packets with dribble condition detected
     0 packets output, 0 bytes, 0 underruns
     0 output errors, 0 collisions, 0 interface resets
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier
     0 output buffer failures, 0 output buffers swapped out
GigabitEthernet1/0/1 is up, line protocol is up (connected)
  Hardware is Gigabit Ethernet, address is 5057.a834.7f81 (bia 5057.a834.7f81)
  Description: MetaSys HVAC Control PC
  MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
  input flow-control is off, output flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:09:20, output 00:00:01, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 10000 bits/sec, 4 packets/sec
  5 minute output rate 10000 bits/sec, 11 packets/sec
     583826046 packets input, 146863078876 bytes, 0 no buffer
     Received 7933555 broadcasts (3952189 multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 3952189 multicast, 0 pause input
     0 input packets with dribble condition detected
     1670868480 packets output, 1174286312168 bytes, 0 underruns
     0 output errors, 0 collisions, 5 interface resets
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 PAUSE output
     0 output buffer failures, 0 output buffers swapped out
switch#
'''


show_interface_status = '''sh int status

Port      Name               Status       Vlan       Duplex  Speed Type
Gi1/0/1                      connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/2   exampledescrip     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/3                      connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/4                      notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/5                      notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/6                      notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/7                      connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/8                      notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/9                      connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/10                     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/11                     connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/12                     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/13                     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/14                     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/15                     connected    400        a-full  a-100 10/100/1000BaseTX
Gi1/0/16                     notconnect   400          auto   auto 10/100/1000BaseTX
Gi1/0/17                     connected    400        a-full a-1000 10/100/1000BaseTX
Gi1/0/18  To switch          connected    trunk      a-full  a-100 10/100/1000BaseTX
switch#
'''

show_power_inline = '''sh power in

Module   Available     Used     Remaining
          (Watts)     (Watts)    (Watts)
------   ---------   --------   ---------
1          1170.0      240.4       929.6
2          1170.0      113.0      1057.0
3          1170.0       34.4      1135.6
4          1170.0       60.0      1110.0
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi1/0/1   auto   on         4.0     Ieee PD             1     30.0
Gi1/0/41  auto   on         4.0     Ieee PD             1     30.0
Gi1/0/42  auto   off        0.0     n/a                 n/a   30.0
Gi1/0/43  auto   on         30.0    AIR-AP3802I-B-K9    4     30.0
Gi1/0/44  auto   on         30.0    AIR-AP3802I-B-K9    4     30.0
Gi1/0/45  auto   on         30.0    AIR-AP3802I-B-K9    4     30.0
Gi1/0/46  auto   on         30.0    AIR-AP3802I-B-K9    4     30.0
Gi1/0/47  auto   on         15.4    AIR-CAP2602I-A-K9   3     30.0
Gi2/0/48  auto   on         4.0     Ieee PD             1     30.0

Switch#'''


ospf_runing_config = '''interface Vlan1234
 description should not show up
 ip address 10.10.10.10 255.255.255.255
 ip directed-broadcast
!
!
router eigrp 1
 network 9.9.9.9 0.0.0.0
 eigrp stub connected summary
!
router ospf 1
 router-id 1.1.1.1
 log-adjacency-changes
 network 2.2.2.2 0.0.0.0 area 25
 network 3.3.3.3 0.0.0.0 area 25
 network 4.4.4.4 0.0.0.0 area 25
 network 5.5.5.5 0.0.0.0 area 25
 network 6.6.6.6 0.0.0.0 area 25
 default-information originate metric 2000
 distance 109
!
router ospf 2
 log-adjacency-changes
 network 7.7.7.7 0.0.0.0 area 25
 default-information originate metric 2000
!
ip classless
no ip http server
ip http secure-server
'''

show_interface_description = '''sh int desc
Interface                      Status         Protocol Description
Vl1                            admin down     down
Vl400                          up             up
Fa0                            admin down     down
Gi1/0/1                        up             up
Gi1/0/2                        down           down
Gi1/0/3                        up             up
Gi1/0/4                        down           down
Gi1/0/5                        down           down
Gi1/0/6                        down           down
Gi1/0/7                        up             up
Gi1/0/8                        down           down
Gi1/0/9                        up             up
Gi1/0/10                       down           down
Gi1/0/11                       up             up
Gi1/0/12                       down           down
Gi1/0/13                       down           down
Gi1/0/14                       down           down     exampledescrip
Gi1/0/15                       up             up
Gi1/0/16                       down           down
Gi1/0/17                       up             up
Gi1/0/18                       up             up       To LIBL-PCT-SW-002
switch#
'''


show_interface_1 = '''sh int gi1/0/1
GigabitEthernet1/0/1 is up, line protocol is up (connected)
  Hardware is Gigabit Ethernet, address is c471.fe17.1581 (bia c471.fe17.1581)
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
  input flow-control is off, output flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:17, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 1000 bits/sec, 2 packets/sec
  5 minute output rate 29000 bits/sec, 15 packets/sec
     258142894 packets input, 68640893535 bytes, 0 no buffer
     Received 4032578 broadcasts (3676864 multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 3676864 multicast, 0 pause input
     0 input packets with dribble condition detected
     1939339422 packets output, 677867998121 bytes, 0 underruns
     0 output errors, 0 collisions, 1 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out
'''

show_vlan_brief = '''sh vl br

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/10
400  vlan400descrip                   active
410  vlandescrip                      active
600  VLAN0600                         active
601  first_network                    active    Gi0/1, Gi0/2, Gi0/3, Gi0/4, Gi0/5, Gi0/6, Gi0/7, Gi0/8
912  anothernetwork                   active
950  Isolated VLAN                    active
1002 fddi-default                     act/unsup
1003 token-ring-default               act/unsup
1004 fddinet-default                  act/unsup
1005 trnet-default                    act/unsup
switch#
'''

mac_address_table = '''sh mac add
          Mac Address Table

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
 All    aaaa.aaaa.aaaa    STATIC      CPU
 All    bbbb.bbbb.bbbb    STATIC      CPU
 All    cccc.cccc.cccc    STATIC      CPU
 All    dddd.dddd.dddd    STATIC      CPU
 All    eeee.eeee.eeee    STATIC      CPU
 All    ffff.ffff.ffff    STATIC      CPU
   1    gggg.gggg.gggg    DYNAMIC     Gi1/0/18
   1    hhhh.hhhh.hhhh    DYNAMIC     Gi2/0/19
   1    iiii.iiii.iiii    DYNAMIC     Po1
Total Mac Addresses for this criterion: 000
switch#
'''

cdp_neighbor_detail = '''sh cdp nei detail
-------------------------
Device ID: dev1
Entry address(es):
  IP address: 1.1.1.1
Platform: cisco WS-C3750X-48P,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/1/1,  Port ID (outgoing port): GigabitEthernet1/1/4
Holdtime : 126 sec

Version :
Cisco IOS Software, C3750E Software (C3750E-UNIVERSALK9-M), Version 12.2(58)SE2, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Thu 21-Jul-11 01:23 by prod_rel_team

advertisement version: 2
Protocol Hello:  OUI=0x00000C, Protocol ID=0x0112; payload len=27, value=00000000FFFFFFFF010225050000000000006400F1560580FF0000
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
Power Available TLV:

    Power request id: 0, Power management id: 1, Power available: 0, Power management level: -1
Management address(es):
  IP address: 1.1.1.1

-------------------------
Device ID: dev2
Entry address(es):
  IP address: 2.2.2.2
Platform: cisco AIR-AP3802I-B-K9,  Capabilities: Router Trans-Bridge
Interface: GigabitEthernet1/0/44,  Port ID (outgoing port): GigabitEthernet0
Holdtime : 151 sec

Version :
Cisco AP Software, ap3g3-k9w8 Version: 8.3.143.10
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 2014-2015 by Cisco Systems, Inc.

advertisement version: 2
Duplex: full
Power drawn: 30.000 Watts
Power request id: 26928, Power management id: 15
Power request levels are:30000 15400 0 0 0
Power Available TLV:

    Power request id: 0, Power management id: 0, Power available: 0, Power management level: 0
Management address(es):
  IP address: 2.2.2.2


switch#
'''

show_ip_arp = '''sh ip arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  1.1.1.1                0   Incomplete      ARPA
Internet  2.2.2.2                99   aaaa.aaaa.aaaa  ARPA   Vlan1
Internet  3.3.3.3                43   bbbb.bbbb.bbbb  ARPA   Vlan1
Internet  4.4.4.4                 0   cccc.cccc.cccc  ARPA   Vlan1
Internet  5.5.5.5                 9   dddd.dddd.dddd  ARPA   Vlan1
Internet  6.6.6.6               174   eeee.eeee.eeee  ARPA   Vlan1
Internet  7.7.7.7                 0   ffff.ffff.ffff  ARPA   Vlan1
switch#
'''