'''

Copyright 2025 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

=========================================================================

Author: Kyle Kowalczyk

This is an example script for how you can use the ConfigParser class to
search for and dynamically generate the configuration needed to remove multiple BGP neighbors.

My hope is that this script gives you inspiration to other uses for dynamic configuration generation
weather that be for removal, modification, etc.

The output of this script will be:

router bgp 65100
 address-family ipv4 vrf CustA
  no neighbor 10.88.52.13 peer-group MyPeers
  no neighbor 10.88.52.13 activate
 address-family ipv4 vrf CustB
  no neighbor 10.88.55.25 remote-as 65102
  no neighbor 10.88.55.25 description To Router 1
  no neighbor 10.88.55.25 timers 20 60
  no neighbor 10.88.55.25 fall-over bfd
  no neighbor 10.88.55.25 activate
  no neighbor 10.88.55.25 send-community
  no neighbor 10.88.55.25 next-hop-self
  no neighbor 10.88.55.25 soft-reconfiguration inbound

=======================================================

This is meant to demonstrate how easy it is to read in the config, modify a portion of it, and getting
usable configuration right out of the box that you can either manually or via a larger script automatically apply.

Notice how there is not duplicated configuration such as multiple router bgp lines or address-family lines.
Also because we performed the search and modify function, only the configuration paths that were matched in our
search are shown, it omitted all other parts of our config.

Keep in mind the more generic the search like for an IP address like I did here could yield incorrect results if
there is a description somewhere with that IP so keep things as specific as possible when you can.
'''
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser

# example running configuration
example_config = '''interface GigabitEthernet1/0/1
 description InterfaceDescription
 mtu 1500
!
router bgp 65100
 address-family ipv4
  network 10.5.5.1 mask 255.255.255.255
  neighbor 10.88.51.13 activate
  neighbor 10.88.51.17 activate
  neighbor 10.88.51.25 activate
  maximum-paths 2
 exit-address-family
 !
 address-family ipv4 vrf CustA
  bgp router-id 172.20.61.205
  network 10.88.52.190 mask 255.255.255.255
  neighbor 10.88.52.13 peer-group MyPeers
  neighbor 10.88.52.13 activate
  neighbor 10.88.52.17 peer-group MyPeers
  neighbor 10.88.52.17 activate
  neighbor 10.88.52.25 remote-as 65102
  neighbor 10.88.52.25 description asdf
  neighbor 10.88.52.25 timers 20 60
  neighbor 10.88.52.25 fall-over bfd
  neighbor 10.88.52.25 activate
  neighbor 10.88.52.25 send-community
  neighbor 10.88.52.25 next-hop-self
  neighbor 10.88.52.25 soft-reconfiguration inbound
  maximum-paths 2
 exit-address-family
 !
 address-family ipv4 vrf CustB
  bgp router-id 172.20.93.205
  neighbor 10.88.55.13 peer-group MyPeers
  neighbor 10.88.55.13 activate
  neighbor 10.88.55.17 peer-group MyPeers
  neighbor 10.88.55.17 activate
  neighbor 10.88.55.25 remote-as 65102
  neighbor 10.88.55.25 description To Router 1
  neighbor 10.88.55.25 timers 20 60
  neighbor 10.88.55.25 fall-over bfd
  neighbor 10.88.55.25 activate
  neighbor 10.88.55.25 send-community
  neighbor 10.88.55.25 next-hop-self
  neighbor 10.88.55.25 soft-reconfiguration inbound
  maximum-paths 2
 exit-address-family
!
line console 0
 logging synchronous
'''

neighbors_to_remove = ['10.88.52.13', '10.88.55.25']

parser = ConfigParser(example_config)
modified_config_tree = parser.search_and_modify_config_tree(search_terms=neighbors_to_remove, full_match=False, prepend_text='no ')
formatted_config = parser.config_tree_to_list(modified_config_tree, indent_step=1)

for line in formatted_config:
    print(line)
