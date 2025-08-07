import datetime
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework.TransportEngines import ReadOnlySSHEngine
from getpass import getpass


# Gathers IP address and login info and handles checking them against the remote device to
# validate that the credentials are correct and handle them if they are not
ip = input('Enter Router/Switch IP address: ')
username = input('Enter Username: ')
password = getpass('Enter Password: ')
en_password = getpass('Enter Enable Password')


with connect_ssh(ip, username, password, enable_password=en_password, engine=ReadOnlySSHEngine) as ssh:
    print(ssh.hostname)
    ssh.cli_to_config_mode()