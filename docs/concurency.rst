Interacting with Multiple Network Devices at the same time
======
CiscoAutomationFramework provides a way of running the same code on multiple devices
concurrently. It takes into account situations where you will have a mix of IOS and Nexus and
when you dont care, providing object to inherit from and override in both circumstances.



.. autoclass:: CiscoAutomationFramework.ThreadLib.SSH
   :members:

.. autoclass:: CiscoAutomationFramework.ThreadLib.SSHSplitDeviceType
   :members:

.. automodule:: CiscoAutomationFramework.ThreadLib
   :members: start_threads


Example Scripts
-----
Below is an example script that will run concurrently across multiple network devices::

    from CiscoAutomationFramework.ThreadLib import SSH, start_threads


    class MyDevice(SSH):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.interfaces_connected = []

        def during_login(self, ssh):
            # Code here will run every time no matter what
            for line in ssh.send_command_get_output('show interface status'):
                if 'connected' in line and not 'notconn' in line:
                    self.interfaces_connected.append(line.split()[0])

        def secondary_action(self, ssh):
            """
            If there is some secondary action needed to be performed, code it here
            If there is nothing you need to do you DO NOT need to define this method

            To execute this, when starting threads via the start_threads method set
            perform_secondary_action=True
            """
            pass

        def post_secondary_action(self, ssh):
            """
            If you need to something post the secondary action taking place, code it here.
            an example would be re gathering data or saving config

            If there is nothing you need to do you DO NOT need to define this method

            To execute this, when starting threads via the start_threads method set
            perform_secondary_action=True
            """
            pass


    if __name__ == '__main__':

        username = 'myusername'
        password = 'mypassword'

        # replace with IP addresses of network devices on your network
        ips = ['192.168.1.1', '192.168.2.1', '192.168.3.1', '192.168.4.1', '192.168.5.1', '192.168.6.1']
        threads = start_threads(MyDevice, ips, username, password, wait_for_threads=True)
        for thread in threads:
            print(thread.hostname, len(thread.interfaces_connected))


