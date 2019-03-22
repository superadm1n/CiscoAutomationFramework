show_interfaces = '''




Ethernet1/48 is up
 Dedicated Interface
  Belongs to Po11
  Hardware: 1000/10000 Ethernet, address: 002a.6a11.3e37 (bia 002a.6a11.3e37)
  Description: N7K CORE VDC
  MTU 1500 bytes, BW 10000000 Kbit, DLY 10 usec
  reliability 255/255, txload 4/255, rxload 5/255
  Encapsulation ARPA
  Port mode is trunk
  full-duplex, 10 Gb/s, media type is 10G
  Beacon is turned off
  Input flow-control is off, output flow-control is off
  Rate mode is dedicated
  Switchport monitor is off
  EtherType is 0x8100
  Last link flapped 140week(s) 6day(s)
  Last clearing of "show interface" counters never
  30 seconds input rate 209999056 bits/sec, 29837 packets/sec
  30 seconds output rate 220888328 bits/sec, 28520 packets/sec
  Load-Interval #2: 5 minute (300 seconds)
    input rate 213.14 Mbps, 30.22 Kpps; output rate 178.03 Mbps, 24.88 Kpps
  RX
    2171821437684 unicast packets  3142458920 multicast packets  2272793974 broadcast packets
    2177236690578 input packets  2290016237078656 bytes
    1207094382851 jumbo packets  0 storm suppression bytes
    0 runts  0 giants  0 CRC  0 no buffer
    0 input error  0 short frame  0 overrun   0 underrun  0 ignored
    0 watchdog  0 bad etype drop  0 bad proto drop  0 if down drop
    0 input with dribble  0 input discard
    0 Rx pause
  TX
    1342374869096 unicast packets  189117058 multicast packets  135067697 broadcast packets
    1342699053851 output packets  928809313843609 bytes
    464310745672 jumbo packets
    1509 output errors  0 collision  0 deferred  0 late collision
    0 lost carrier  0 no carrier  0 babble 0 output discard
    0 Tx pause
  3 interface resets

port-channel10 is up
  Hardware: Port-Channel, address: 002a.6a11.3e32 (bia 002a.6a11.3e32)
  Description: vpc peer link
  MTU 1500 bytes, BW 40000000 Kbit, DLY 10 usec
  reliability 255/255, txload 2/255, rxload 1/255
  Encapsulation ARPA
  Port mode is trunk
  full-duplex, 10 Gb/s
  Input flow-control is off, output flow-control is off
  Switchport monitor is off
  EtherType is 0x8100
  Members in this channel: Eth1/43, Eth1/44, Eth1/45, Eth1/46
  Last clearing of "show interface" counters never
  30 seconds input rate 66952328 bits/sec, 7076 packets/sec
  30 seconds output rate 382912448 bits/sec, 40636 packets/sec
  Load-Interval #2: 5 minute (300 seconds)
    input rate 88.61 Mbps, 8.73 Kpps; output rate 324.78 Mbps, 36.45 Kpps
  RX
    1019634056191 unicast packets  15511825251 multicast packets  4536491671 broadcast packets
    1039682373113 input packets  1224508417847936 bytes
    716014379301 jumbo packets  0 storm suppression bytes
    0 runts  0 giants  1181 CRC  0 no buffer
    1181 input error  0 short frame  0 overrun   0 underrun  0 ignored
    0 watchdog  0 bad etype drop  0 bad proto drop  0 if down drop
    0 input with dribble  0 input discard
    0 Rx pause
  TX
    2572409427316 unicast packets  10977160560 multicast packets  4695688113 broadcast packets
    2588082275989 output packets  2773709844268093 bytes
    1426948144398 jumbo packets
    51686 output errors  0 collision  0 deferred  0 late collision
    0 lost carrier  0 no carrier  0 babble 0 output discard
    0 Tx pause
  3 interface resets
 '''

ospf_running_config = '''





interface Ethernet2/3
  description mydesc
  switchport mode trunk
  switchport trunk native vlan 1000
  mtu 9216
  channel-group 11 mode active
  no shutdown
router ospf 1
  router-id 10.255.242.4
  network 10.1.0.0/23 area 0.0.0.0
  network 10.1.10.0/23 area 0.0.0.0
router eigrp 100
  distance 100 100




'''



show_interface_status = '''sh int status

--------------------------------------------------------------------------------
Port          Name               Status    Vlan      Duplex  Speed   Type
--------------------------------------------------------------------------------
mgmt0         --                 connected routed    full    1000    --
Eth1/1        vpc peer link      connected trunk     full    10G     SFP-H10GB-A
Eth1/2        a descrip          connected routed    full    10G     10Gbase-SR
Eth1/3        a descrip          connected trunk     full    10G     SFP-H10GB-C
Eth1/4        --                 sfpAbsent 1         auto    auto    --
Eth1/5        vpc peer link      connected trunk     full    10G     SFP-H10GB-A
Eth1/6        --                 sfpAbsent 1         auto    auto    --
Eth1/7        --                 sfpAbsent 1         auto    auto    --
Eth1/8        --                 sfpAbsent 1         auto    auto    --
Eth1/9        a descrip          connected routed    full    10G     10Gbase-LR
Eth1/10       a descrip          connected trunk     full    10G     SFP-H10GB-C
Eth1/11       adescrip           connected routed    full    10G     SFP-H10GB-C
Vlan1         --                 connected routed    auto    auto    --
Po10          vpc peer link      connected trunk     full    10G     --
Eth2/17       --                 disabled  1         auto    auto    1000base-T
switch#
'''