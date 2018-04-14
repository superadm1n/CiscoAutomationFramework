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
from CiscoAutomationFramework import CAF
from getpass import getpass

# Prints a header for the user
print('Welcome to Config_Backup.py\n')

# Gathers IP address and login info
ip = input('Enter Router/Switch IP address: ')
username = input('Enter Username: ')
password = getpass('Enter Password: ')
en_password = getpass('Enter Enable Password: ')

# configures todays date
date = datetime.datetime.now()
today_date = '{}-{}-{}'.format(date.month, date.day, date.year)

try:
    # Logs into the device, grabs running config and the hostname
    with CAF('ssh') as ssh:
        ssh.connect(ip, username, password, en_password)
        hostname = ssh.hostname
        print('Successfuly Logged into {}, grabbing running config.'.format(hostname))
        running_config = ssh.show_run()

    # Sets up the name of the file
    filename = '{}-{}.txt'.format(hostname, today_date)
    # saves file
    with open(filename, 'w') as file:
        print('Saving Running config.')
        try:
            file.write(running_config)
            print('Running config saved successfully in file {}!'.format(filename))
        except:  # TODO Improvement: - Handle Exceptions better
            print('Running config NOT SAVED!')

except:  # TODO Improvement: - Handle Exceptions better
    print('Unable to login to device, configuration not saved!')

# Prints a footer and waits for the user to press enter before exiting
print('\n---End of Script---')
input('Press ENTER to exit.')
