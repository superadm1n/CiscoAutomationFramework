"""
Proof of concept script showing how to use the InterfaceStatusOutputParser to list interfaces that are of interest.

In this example it will show any interfaces that are in err-disable on the device it is running on
"""
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework.Parsers.InterfaceStatusParser import InterfaceStatusOutputParser

ip = 'Enter IP Address or Hostname here'
username = 'Username'
password = 'Password'

with connect_ssh(ip, username, password) as ssh:
    hostname = ssh.hostname
    output = ssh.send_command_get_output('sh int status')

parser = InterfaceStatusOutputParser(output)

print(f'Hostname: {hostname}')
for line in parser.interfaces:
    if 'err' in line.status.lower():
        print(f'Interface {line.name} is in {line.status} status!')


