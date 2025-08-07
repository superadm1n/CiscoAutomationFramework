"""
This script is a proof of concept sub classing of the SSH object to make a threaded program. Note in secondary_action
and post_secondary_action you DO NOT need to redefine those methods in order to make the program run.


Order of Operations of ssh object

Login
Run during_login
if secondary action is True
  run secondary_action
  run post_secondary action

"""
from CiscoAutomationFramework.ThreadLib import SSH, start_threads


class MyDevice(SSH):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interfaces_connected = []

    def during_login(self, ssh):
        for line in ssh.send_command_get_output('show interface status'):
            if 'connected' in line and not 'notconn' in line:
                self.interfaces_connected.append(line.split()[0])

    def secondary_action(self, ssh):
        """If there is some secondary action needed to be performed, code it here
        If there is nothing you need to do you DO NOT need to define this method"""
        pass

    def post_secondary_action(self, ssh):
        """If you need to something post the secondary action taking place, code it here.
        an example would be re gathering data or saving config

        If there is nothing you need to do you DO NOT need to define this method"""
        pass


if __name__ == '__main__':

    username = 'myusername'
    password = 'mypassword'

    # replace with IP addresses of network devices on your network
    ips = ['192.168.1.1', '192.168.2.1', '192.168.3.1', '192.168.4.1', '192.168.5.1', '192.168.6.1']
    threads = start_threads(MyDevice, ips, username, password, wait_for_threads=True)
    for thread in threads:
        print(thread.hostname, len(thread.interfaces_connected))
