from threading import Thread
from CiscoAutomationFramework import connect_ssh
from abc import ABC, abstractmethod


class SSH(Thread, ABC):

    """
    Base SSH object that you can inhert from when building a threaded script that will run across the network.
    Unless you build the logic yourself all functions during_login, secondary_action, and post_secondary_action
    will be run against each device. I find alot of the time this is sufficient.
    """

    def __init__(self, ip, username, password, enable_password=None, perform_secondary_action=False):
        super().__init__()
        self.ip = ip
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.perform_secondary_action = perform_secondary_action
        self.hostname = ''
        self.is_nexus = False

    def during_login(self, ssh):
        pass

    def secondary_action(self, ssh):
        pass

    def post_secondary_action(self, ssh):
        pass

    def run(self) -> None:

        with connect_ssh(self.ip, self.username, self.password) as ssh:
            self.is_nexus = ssh.is_nexus
            self.hostname = ssh.hostname
            self.during_login(ssh)
            if self.perform_secondary_action:
                self.secondary_action(ssh)
                self.post_secondary_action(ssh)


class SSHSplitDeviceType(SSH):

    """
    Create a script by inheriting from this object if you are running the same script against both
    Nexus and IOS devices but the command are different on each platform or the sequence is different.
    Out of the box it will run the functions prepended with ios on ios and iosxe devices and functions
    prepended with nexus on nxos devices. Because it is implied that this script will be run against a mix
    of nexus and ios you must define the functions regardless if they will be used or not
    """

    @abstractmethod
    def ios_during_login(self, ssh):
        pass

    @abstractmethod
    def nexus_during_login(self, ssh):
        pass

    @abstractmethod
    def ios_secondary_action(self, ssh):
        pass

    @abstractmethod
    def nexus_secondary_action(self, ssh):
        pass

    @abstractmethod
    def ios_post_secondary_action(self, ssh):
        pass

    @abstractmethod
    def nexus_post_secondary_action(self, ssh):
        pass

    def during_login(self, ssh):
        if self.is_nexus:
            self.nexus_during_login(ssh)
        else:
            self.ios_during_login(ssh)

    def secondary_action(self, ssh):
        if self.is_nexus:
            self.secondary_action(ssh)
        else:
            self.secondary_action(ssh)
            pass

    def post_secondary_action(self, ssh):
        if self.is_nexus:
            self.nexus_post_secondary_action(ssh)
        else:
            self.ios_post_secondary_action(ssh)


def start_threads(object, ips, username, password, enable_password=None,
                  perform_secondary_action=False, wait_for_threads=False):

    """
    This helper function is a quick and easy way to start your threads. Gives you an option for waiting for threads
    to complete also.
    It will return the thread objects from the function for further processing by the main thread.
    """

    if not issubclass(object, SSH):
        raise TypeError('object MUST be a subclass of ThreadedSSH!')

    # Instantiate thread objects and start them
    threads = [object(ip=ip, username=username, password=password, enable_password=enable_password,
                      perform_secondary_action=perform_secondary_action) for ip in ips]
    for thread in threads:
        thread.start()

    # if user wants to wait for them, wait for threads to finish
    if wait_for_threads:
        for thread in threads:
            thread.join()

    return threads
