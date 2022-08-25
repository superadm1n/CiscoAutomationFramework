"""
Proof of concept script showing how to subclass the SSHSplitDeviceType class to run scripts against
Nexus and IOS at the same time. Shown is where the parsing of show run to extract syslog servers is different,
and while there is no secondary or post secondary action happening, it shows how you MUST define them in order
to not throw an exception.

Order of Operations of ssh object

Login
Run during_login
if secondary action is True
  run secondary_action
  run post_secondary action
"""
from CiscoAutomationFramework.ThreadLib import SSHSplitDeviceType, start_threads


class MyDevice(SSHSplitDeviceType):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.syslog_servers = []

    def ios_during_login(self, ssh):
        """Must define even if empty to properly subclass object"""
        for line in ssh.running_config:
            if line.startswith('logging host'):
                self.syslog_servers.append(line.split()[2])

    def nexus_during_login(self, ssh):
        """Must define even if empty to properly subclass object"""
        for line in ssh.running_config:
            if line.startswith('logging server'):
                self.syslog_servers.append(line.split()[2])

    def ios_secondary_action(self, ssh):
        """Must define even if empty to properly subclass object"""
        pass

    def nexus_secondary_action(self, ssh):
        """Must define even if empty to properly subclass object"""
        pass

    def ios_post_secondary_action(self, ssh):
        """Must define even if empty to properly subclass object"""
        pass

    def nexus_post_secondary_action(self, ssh):
        """Must define even if empty to properly subclass object"""
        pass


if __name__ == '__main__':

    username = 'myusername'
    password = 'mypassword'

    # replace with IP addresses of network devices on your network
    ips = ['192.168.1.1', '192.168.2.1', '192.168.3.1', '192.168.4.1', '192.168.5.1', '192.168.6.1']
    threads = start_threads(MyDevice, ips, username, password, wait_for_threads=True)
    for thread in threads:
        print(thread.hostname, len(thread.syslog_servers))
