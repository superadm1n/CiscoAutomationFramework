"""
Proof of concept script showing how to use the route map parsing and prefix list parsing in the ConfigParser

This script will log into a cisco device, iterate through every configured route map displaying the route map
name and iterate through each rule showing the sequence number, action, match condition, and set conditions.

It will also detect if a prefix list was referenced in the match condition and if one was it will display
each prefix and match condition configured for all of the prefix lists configured in the route map rule.

This script is useful for seeing all relevant information in a route map in a single concise output without
needing to enter multiple commands and scroll up and down in configuration.

"""
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser

ip = 'Enter IP Address or Hostname here'
username = 'Username'
password = 'Password'

with connect_ssh(ip, username, password) as ssh:
    hostname = ssh.hostname
    running_configuration = ssh.running_config

searched_config = 'nested config here'
parser = ConfigParser(running_configuration)
referenced_sections = parser.sections_config_referenced_in(searched_config)
for section in referenced_sections:
    print(section)
print(f'\nConfig "{searched_config}" has been found in a total of {len(referenced_sections)} sections!')
