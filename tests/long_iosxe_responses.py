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

show_power_inline = '''show power in

Module   Available     Used     Remaining
          (Watts)     (Watts)    (Watts)
------   ---------   --------   ---------
1          1800.0      153.6      1646.4
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi1/0/1   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/2   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/3   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/4   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/5   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/6   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/7   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/8   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/9   auto   off        0.0     n/a                 n/a   60.0
Gi1/0/10  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/11  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/12  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/13  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/14  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/15  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/16  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/17  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/18  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/19  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/20  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/21  auto   on         15.4    Ieee PD             3     60.0
Gi1/0/22  auto   on         15.4    Ieee PD             3     60.0
Gi1/0/23  auto   on         15.4    Ieee PD             3     60.0
Gi1/0/24  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/25  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/26  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/27  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/28  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/29  auto   on         15.4    Ieee PD             3     60.0
Gi1/0/30  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/31  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/32  auto   on         4.0     Ieee PD             1     60.0
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi1/0/33  auto   on         4.0     Ieee PD             1     60.0
Gi1/0/34  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/35  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/36  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/37  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/38  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/39  auto   on         30.0    AIR-AP3802I-B-K9    4     60.0
Gi1/0/40  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/41  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/42  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/43  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/44  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/45  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/46  auto   on         30.0    AIR-AP3802I-B-K9    4     60.0
Gi1/0/47  auto   off        0.0     n/a                 n/a   60.0
Gi1/0/48  auto   off        0.0     n/a                 n/a   60.0

Module   Available     Used     Remaining
          (Watts)     (Watts)    (Watts)
------   ---------   --------   ---------
2          1800.0      126.2      1673.8
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi2/0/1   auto   on         4.0     Ieee PD             1     60.0
Gi2/0/2   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/3   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/4   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/5   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/6   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/7   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/8   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/9   auto   off        0.0     n/a                 n/a   60.0
Gi2/0/10  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/11  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/12  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/13  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/14  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/15  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/16  auto   off        0.0     n/a                 n/a   60.0
Interface Admin  Oper       Power   Device              Class Max
                            (Watts)
--------- ------ ---------- ------- ------------------- ----- ----
Gi2/0/17  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/18  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/19  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/20  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/21  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/22  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/23  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/24  auto   on         4.0     Ieee PD             1     60.0
Gi2/0/25  auto   on         4.0     Ieee PD             1     60.0
Gi2/0/26  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/27  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/28  auto   on         4.0     Ieee PD             1     60.0
Gi2/0/29  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/30  auto   on         4.0     Ieee PD             1     60.0
Gi2/0/31  auto   on         15.4    Ieee PD             3     60.0
Gi2/0/32  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/33  auto   on         15.4    Ieee PD             3     60.0
Gi2/0/34  auto   on         15.4    Ieee PD             3     60.0
Gi2/0/35  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/36  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/37  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/38  auto   on         30.0    AIR-AP3802I-B-K9    4     60.0
Gi2/0/39  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/40  auto   on         30.0    AIR-AP3802I-B-K9    4     60.0
Gi2/0/41  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/42  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/43  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/44  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/45  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/46  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/47  auto   off        0.0     n/a                 n/a   60.0
Gi2/0/48  auto   off        0.0     n/a                 n/a   60.0
'''


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