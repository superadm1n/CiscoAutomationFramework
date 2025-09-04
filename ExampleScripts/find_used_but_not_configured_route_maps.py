'''
This is an example script that will check your BGP config, get all of the referenced route maps, then check
if there is a route map with that name configured on the device.

This script is intended to show the power of the ConfigParser and the level of insights you can gain
through integrated search utilities.
'''
from CiscoAutomationFramework.Parsers.ConfigParser import ConfigParser
from CiscoAutomationFramework.util import extract_line_from_tree

# Update path to the path of your config file
config_file_path = '/path/to/config_file.txt'

# read in config file
with open(config_file_path, 'r') as f:
    conf = f.read()


def extract_route_map_names(rm_definition_lines):
    """Helper function to extract the route map name from the route map definition
    ex. neighbor 192.168.10.5 route-map TEST in || will extract "TEST"
    """
    map_names = []
    for map_statement in rm_definition_lines:
        for idx, word in enumerate(map_statement.split()):
            if word == 'route-map':
                map_names.append(map_statement.split()[idx + 1])
    return map_names


parser = ConfigParser(conf)
# extract only BGP config
bgp_config = parser.search_config_tree('router bgp')
# From BGP config extract all lines that contain the text "route-map"
maps = extract_line_from_tree(bgp_config.config_tree, 'route-map', find_all=True)
# use helper function to extract the name of the route map from all references
configured_route_maps = extract_route_map_names(maps)

# Iterate over each route map name, try and get the route map definition from the config, printing out the name
# if not found
for route_map in configured_route_maps:
    if not parser.get_route_map(route_map):
        print(f'Route map {route_map} is referenced but not configured!')
