
from .CustomExceptions import MethodNotImplemented

class CommandMethods:

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

    def find_mac_address(self, mac_address):
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