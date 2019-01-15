'''
Copyright 2018 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

===========================================================================

This Module contains the code that is specific to issuing commands to ASA's
'''

from .CustomExceptions import MethodNotImplemented

class CommandMethods:

    '''
    Generic class that all other command classes should inherit from. When a new method
    is added it should be added here first
    '''

    def get_uptime(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_run(self, timeout=15):
        raise MethodNotImplemented('This method has not been implemented!')

    def get_local_users(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def delete_local_user(self, username):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_run_interface(self, interface):
        raise MethodNotImplemented('This method has not been implemented!')

    def configure_description(self, interface, description):
        raise MethodNotImplemented('This method has not been implemented!')

    def configure_access_vlan(self, interface, vlan):
        raise MethodNotImplemented('This method has not been implemented!')

    def power_cycle_port(self, interface, delay):
        raise MethodNotImplemented('This method has not been implemented!')

    def configure_router_lan_subinterface(
            self, physical_interface, vlan_number, ip_address, subnet_mask, dhcp_servers_ip_addresses):
        raise MethodNotImplemented('This method has not been implemented!')

    def physical_port_inventory(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def physical_port_inventory_longname(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def port_status(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def power_inline(self, summary):
        raise MethodNotImplemented('This method has not been implemented!')

    def list_ospf_configuration(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def list_eigrp_configuration(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def list_down_ports(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def last_input_and_output(self, interface):
        raise MethodNotImplemented('This method has not been implemented!')

    def list_configured_vlans(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def global_last_input_and_output(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def mac_address_table(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def find_mac_address(self, mac_address, mac_table):
        raise MethodNotImplemented('This method has not been implemented!')

    def cdp_neighbor_table(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def arp_table(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_routes(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_interface_status(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_interface_description(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_configured_syslog_server(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def show_vlan(self):
        raise MethodNotImplemented('This method has not been implemented!')

    def shutdown_interface(self, interface):
        raise MethodNotImplemented('This method has not been implemented!')

    def no_shutdown_interface(self, interface):
        raise MethodNotImplemented('This method has not been implemented!')

    def set_access_vlan_on_interface(self, interface, vlan_number):
        raise MethodNotImplemented('This method has not been implemented!')
