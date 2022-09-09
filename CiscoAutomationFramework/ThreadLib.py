from threading import Thread
from CiscoAutomationFramework import connect_ssh
from CiscoAutomationFramework.FirmwareBase import CiscoFirmware
from abc import ABC, abstractmethod


class SSH(Thread, ABC):

    """
    Base SSH object that you can inherit from when building a threaded script that will run across the network.

    To build a script you must subclass this object and override the methods that are documented.

    Method Execution Order
    The object logs into the device
    during_login is executed
    if perform_secondary_action is set to True secondary_action is executed and then post_secondary_action


    """

    def __init__(self, ip, username, password, enable_password=None, perform_secondary_action=False):
        """

        :param ip: IP address of device
        :type ip: str
        :param username: Username to login with
        :type username: str
        :param password: Password for user
        :type password: str
        :param enable_password: Enable password if login user does not have direct access to privilege exec mode
        :type enable_password: str
        :param perform_secondary_action: True/False to execute secondary_action method when logged in
        :type perform_secondary_action: bool
        """
        super().__init__()
        self.ip = ip
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.perform_secondary_action = perform_secondary_action
        self.hostname = ''
        self.commands_sent = []
        self.is_nexus = False

    def during_login(self, ssh):
        """
        Every time this object runs against a device this method will be run. Override this method and add logic
        that needs to be run every time your object runs against a device.

        I find I often add logic here that gathers data and does not modify configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    def secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True.

        I often find this is useful for containing logic that modifies configuration that only needs to be run if a
        certain condition is met.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    def post_secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True and AFTER secondary_action has completed.

        I often find this is useful for containing logic that re gathers data or saves configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    def run(self) -> None:

        with connect_ssh(self.ip, self.username, self.password) as ssh:
            self.is_nexus = ssh.is_nexus
            self.hostname = ssh.hostname
            self.during_login(ssh)
            if self.perform_secondary_action:
                self.secondary_action(ssh)
                self.post_secondary_action(ssh)
            self.commands_sent = ssh.commands_sent


class SSHSplitDeviceType(SSH):

    """
    Create a script by inheriting from this object if you are running the same script against both
    Nexus and IOS devices but the command are different on each platform or the sequence is different.
    Out of the box it will run the functions prepended with ios on ios and iosxe devices and functions
    prepended with nexus on nxos devices. Because it is implied that this script will be run against a mix
    of nexus and ios you must define the functions regardless if they will be used or not when inheriting from
    this object
    """

    @abstractmethod
    def ios_during_login(self, ssh):
        """
        Every time this object runs against a device that is detected to be NOT Nexus this method
        will be run. Override this method and add logic that needs to be run every time your object runs against a
        device.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type

        I find I often add logic here that gathers data and does not modify configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    @abstractmethod
    def nexus_during_login(self, ssh):
        """
        Every time this object runs against a device that is detected to be running Nexus this method
        will be run. Override this method and add logic that needs to be run every time your object runs against a
        device.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type

        I find I often add logic here that gathers data and does not modify configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    @abstractmethod
    def ios_secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True and the device is detected as not Nexus.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type

        I often find this is useful for containing logic that modifies configuration that only needs to be run if a
        certain condition is met.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    @abstractmethod
    def nexus_secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True and the device is detected Nexus.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type.

        I often find this is useful for containing logic that modifies configuration that only needs to be run if a
        certain condition is met.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    @abstractmethod
    def ios_post_secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True and AFTER secondary_action has completed
        and the device is detected to be NOT Nexus.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type.

        I often find this is useful for containing logic that re gathers data or saves configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
        pass

    @abstractmethod
    def nexus_post_secondary_action(self, ssh):
        """
        This method will run only if perform_secondary_action is set to True and AFTER secondary_action has completed
        and the device is detected to be Nexus.

        Must be overridden when inheriting from this object regardless if your script will run against this device
        type.

        I often find this is useful for containing logic that re gathers data or saves configuration.

        :param ssh: SSH object is provided to this method for interacting with the end device
        :type ssh: CiscoFirmware
        :return: Nothing
        """
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

    :param object: Object you have written to perform your task. Must be inherted from SSH or SSHSplitDeviceType
    :type object: [SSH, SSHSplitDeviceType]
    :param ips: List of IP addresses or hostnames to run your worker object against
    :type ips: list[str]
    :param username: Username to login with
    :type username: str
    :param password: Password for user
    :type password: str
    :param enable_password: Enable password if user does not have rights to privilege exec mode without enable password
    :type enable_password: str
    :param perform_secondary_action: True if you want to run the secondary_action method against device
    :type perform_secondary_action: bool
    :param wait_for_threads: Wait for all threads to complete before returning
    :type wait_for_threads: bool
    :return: List of threads either running or completed depending on if wait_for_threads is True/False
    :rtype: list[SSH, SSHSplitDeviceType, type(object)]
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
