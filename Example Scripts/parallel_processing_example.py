'''
Example script to use parallel processing to run a script against multiple
network devices at the same time.
'''
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework import MPLib


def data_handler(data):
    '''This function will run every time one of the processes return
    data from a network device. This will just print the data

    :param data: Data captured from network device via one of the processes
    '''
    print(data)


def worker_process(ip, username, password, enable_password):
    '''
    This is the function that will be run against each of the network devices
    '''
    with connect_ssh(ip, username, password, enable_password) as ssh:
        hostname = ssh.hostname
        uptime = ssh.get_uptime()
    return '{}, {}'.format(hostname, uptime)


if __name__ == '__main__':
    from datetime import datetime
    from getpass import getpass

    # List of IP's to run against
    ips = ['10.104.200.1', '10.104.200.15', '10.104.200.16']

    # Get user info
    username = input('Enter username: ')
    password = getpass('Enter Password for {}: '.format(username))
    enable_password = getpass('Enter Enable Password: ')

    # Construct list of jobs
    joblist = [MPLib.Job(worker_process, x, username, password, enable_password) for x in ips]

    start_time = datetime.now()  # start a timer

    # start the processes and return data, also passing in the data_handler function
    # to print out the data in real time
    all_returned_data = MPLib.parallel_process(joblist, data_handler=data_handler)

    # get the time all of the processes took and print that to the user
    time_elapsed = datetime.now() - start_time
    print('All of the data from every process was returned in {}'.format(time_elapsed))

