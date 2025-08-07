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


parser = ConfigParser(running_configuration)

for route_map in parser.route_maps:
    print(f'Route map {route_map.name}, {route_map.num_rules} configured rules')
    print(f'Sequence numbers used: {", ".join(route_map.configured_sequence_numbers)}')
    for route_map_rule in route_map.rules:
        print(f'  Rule seq: {route_map_rule.sequence_number}')
        print(f'  Action: {route_map_rule.action}')
        print(f'  Match: {route_map_rule.match_clause}')

        if 'prefix-list' in route_map_rule.match_clause:
            # Display the prefix lists with the route map info for easy viewing
            for prefix_list_name in route_map_rule.match_clause.split()[4:]:
                print(f'    Prefix List {prefix_list_name}')
                prefix_list = parser.get_prefix_list(prefix_list_name)
                for pl_rule in prefix_list.rules:
                    print(f'      {pl_rule.action} {pl_rule.entire_prefix}')

        print(f'  Set: {", ".join(route_map_rule.set_clause)}')
        print('--------')

    print('\n\n======================')
