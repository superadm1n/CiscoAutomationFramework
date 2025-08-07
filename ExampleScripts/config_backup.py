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

=========================================================================

Author: Kyle Kowalczyk
Basic Backup script that will take an IP address from a user along with their credentials, login to the device,
capture the running config, and save that to a file.
'''
import datetime
from CiscoAutomationFramework import connect_ssh
from getpass import getpass

# Prints a header for the user
print('Welcome to Config_Backup.py\n')

# Gathers IP address and login info and handles checking them against the remote device to
# validate that the credentials are correct and handle them if they are not
ip = input('Enter Router/Switch IP address: ')
username = input('Enter Username: ')
password = getpass('Enter Password: ')
en_password = getpass('Enter Enable Password')

# configures todays date
date = datetime.datetime.now()
today_date = f'{date.month}-{date.day}-{date.year}'

try:
    # Logs into the device, grabs running config and the hostname
    with connect_ssh(ip, username, password, en_password) as ssh:
        hostname = ssh.hostname
        print('Successfuly Logged into {}, grabbing running config.'.format(hostname))
        running_config = ssh.running_config
except:  # TODO Improvement: - Handle Exceptions better
    print('Unable to login to device, configuration not saved!')
    exit()

# Sets up the name of the file
filename = f'{hostname}-{today_date}.txt'

# saves file
try:
    print('Saving Running config.')
    with open(filename, 'w') as file:
        file.write(running_config)
        print('Running config saved successfully in file {}!'.format(filename))
except:  # TODO Improvement: - Handle Exceptions better
    print('Running config NOT SAVED!')
    exit()


# Prints a footer and waits for the user to press enter before exiting
print('\n---End of Script---')
input('Press ENTER to exit.')
