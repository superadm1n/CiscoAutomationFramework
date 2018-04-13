Project Goals
===============

Create a framework that is able to issue commands to a Cisco device regardless of device type
or firmware level (IOS, NXOS, IOSXE, ASA) and return the data in a format that a script writer would
find the most useful. In addition to that these commands should be able to be issued via any transport medium
and return the same results in the same format weather is SSH, serial, or telnet.

For example:
when getting the MAC address table it is best to return a list of lists with the appropriate columns in each list
so then the script creator can iterate over the mac address table and pluck out each column they need to use vs
haveing to find a way to parse that data theirselves