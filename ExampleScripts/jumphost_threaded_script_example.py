"""
Example script demonstrating how to connect to Cisco devices through a Linux jump host (bastion).

Supports both:
  1. Single-threaded direct connections using connect_ssh(..., jumphost=...)
  2. Multi-threaded connections using start_threads(..., jumphost=...)
     - A single shared jump host for all threads
     - Different jump hosts per device/thread (via mapping dict or target tuples)

The tunneling is handled natively at the transport level (SSH direct-tcpip channel),
so end-to-end encryption is preserved and there is no need to interact with the
Linux bastion's shell or prompts.
"""

from getpass import getpass
from CiscoAutomationFramework import JumpHost, connect_ssh
from CiscoAutomationFramework.ThreadLib import SSH, start_threads
from CiscoAutomationFramework.util import column_print


class NetworkDevice(SSH):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_clock_time = []

    @property
    def clock_time(self):
        return ' '.join(x for x in self.raw_clock_time if x != '')

    def during_login(self, ssh):
        # Runs commands against the target Cisco device through the tunnel
        self.raw_clock_time = ssh.send_command_get_output('show clock')[1:-1]


if __name__ == '__main__':

    # =========================================================================
    # Step 1: Configure your Linux Jump Host(s)
    # =========================================================================

    # Password authentication:
    jumphost_ip = input('Enter Linux Jump Host IP: ')
    jumphost_user = input('Enter Jump Host Username: ')
    jumphost_pass = getpass(f'Enter Jump Host Password for {jumphost_user}: ')

    jump_host = JumpHost(
        ip=jumphost_ip,
        username=jumphost_user,
        password=jumphost_pass,
        port=22,
        timeout=10
    )

    # Note: SSH key authentication is also supported:
    # jump_host_key = JumpHost(
    #     ip='192.168.1.100',
    #     username='bastion_user',
    #     key_filename='/home/user/.ssh/id_rsa',  # or id_ed25519
    #     passphrase=None                         # optional key passphrase
    # )

    # =========================================================================
    # Step 2: Target Cisco device credentials
    # =========================================================================
    cisco_user = input('\nEnter Cisco Username: ')
    cisco_pass = getpass(f'Enter Cisco Password for {cisco_user}: ')
    cisco_ips = ['10.204.10.12', '10.204.10.13']

    # -------------------------------------------------------------------------
    # Example A: Single-device connection using connect_ssh
    # -------------------------------------------------------------------------
    # print('\nConnecting to a single device via JumpHost...')
    # with connect_ssh(cisco_ips[0], cisco_user, cisco_pass, jumphost=jump_host) as ssh:
    #     print(f'Connected to: {ssh.hostname}')
    #     print(f'Clock: {ssh.send_command_get_output("show clock")}')

    # -------------------------------------------------------------------------
    # Example B: Multi-threaded execution with a shared JumpHost
    # -------------------------------------------------------------------------
    print('\nReaching out to network devices through jump host...')
    threads = start_threads(
        NetworkDevice,
        cisco_ips,
        cisco_user,
        cisco_pass,
        jumphost=jump_host,
        wait_for_threads=True
    )

    # -------------------------------------------------------------------------
    # Example C: Different JumpHosts per thread/device
    # -------------------------------------------------------------------------
    # You can also pass a dict mapping device IP to specific JumpHost:
    #
    # jump_east = JumpHost('192.168.10.1', 'user', 'pass')
    # jump_west = JumpHost('192.168.20.1', 'user', 'pass')
    #
    # jumphost_mapping = {
    #     '10.204.10.12': jump_east,
    #     '10.204.10.13': jump_west,
    # }
    # threads = start_threads(NetworkDevice, cisco_ips, cisco_user, cisco_pass,
    #                         jumphost=jumphost_mapping, wait_for_threads=True)
    #
    # Or pass target tuples directly in the ips list:
    # targets = [
    #     ('10.204.10.12', jump_east),
    #     ('10.204.10.13', jump_west),
    #     ('10.204.10.14', None),  # None means direct connection without jumphost
    # ]
    # threads = start_threads(NetworkDevice, targets, cisco_user, cisco_pass, wait_for_threads=True)

    # =========================================================================
    # Step 3: Collect and display output
    # =========================================================================
    data = [['Hostname', 'IP', 'Time']]
    for thread in threads:
        data.append([thread.hostname, thread.ip, thread.clock_time])
    column_print(data, separator_char='-')
