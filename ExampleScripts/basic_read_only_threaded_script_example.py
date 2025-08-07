from CiscoAutomationFramework.ThreadLib import ReadOnlySSH, start_threads
from CiscoAutomationFramework.util import column_print


class NetworkDevice(ReadOnlySSH):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raw_clock_time = []

    @property
    def clock_time(self):
        return ' '.join(x for x in self.raw_clock_time if x != '')

    def during_login(self, ssh):
        self.raw_clock_time = ssh.send_command_get_output('show clock')[1:-1]
        ssh.cli_to_config_mode()



if __name__ == '__main__':
    from getpass import getpass

    username = input('Enter Username: ')
    password = getpass(f'Enter Password for {username}: ')
    ips = ['10.204.10.12', '10.204.10.13']  # replace with your IP addresses or get them programmatically

    print('Reaching out to network devices!')
    threads = start_threads(NetworkDevice, ips, username, password)

    print('Waiting for threads to complete.')
    for t in threads:
        t.join()

    data = [['Hostname', 'IP', 'Time']]
    for thread in threads:
        data.append([thread.hostname, thread.ip, thread.clock_time])
    column_print(data, separator_char='-')
