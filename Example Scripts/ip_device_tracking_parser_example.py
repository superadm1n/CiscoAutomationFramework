"""
Proof of concept script showing how to use the DeviceTrackingOutputParser to list interfaces that have an APIPA address
detected on it.
"""
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework.Parsers import DeviceTrackingOutputParser
from CiscoAutomationFramework.util import column_print

ip = 'Enter IP Address or Hostname here'
username = 'Username'
password = 'Password'

with connect_ssh(ip, username, password) as ssh:
    hostname = ssh.hostname
    output = ssh.send_command_get_output('show ip device tracking all')

parser = DeviceTrackingOutputParser(output)

print_data = [['Switch', 'Interface', 'Configured Vlan', 'APIPA Address']]
for entry in parser.entries:
    if entry.is_apipa:
        print_data.append([hostname, entry.interface, entry.vlan, entry.ip_address])
column_print(print_data)
