.. CiscoAutomationFramework documentation master file, created by
   sphinx-quickstart on Fri Apr  1 11:39:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CiscoAutomationFramework's documentation!
====================================================

The CiscoAutomation Framework is designed to be a library in Python that abstracts away
CLI navigation and scraping so a network administrator can interact with a Cisco device
and they need to worry much less about parsing output or navigating to the correct
CLI section when issuing commands.

Example Usage
========

Basic connection to a device::

   from CiscoAutomationFramework import connect_ssh
   ssh = connect_ssh('ipaddress', 'username', 'password')
   print(ssh.running_config)
   print(ssh.startup_config)
   print(ssh.arp_table)
   print(ssh.mac_address_table)
   ssh.close_connection

You can also use a context manager (recommended) so you dont have to worry about closing the connection::

   from CiscoAutomationFramework import connect_ssh

   with connect_ssh('ip', 'username', 'password') as ssh:
      mac_table = ssh.mac_address_table

   print(mac_table)


There are integrated output parsers so you can have an easy way of interacting tables that are complex to parse::

   from CiscoAutomationFramework import connect_ssh
   from CiscoAutomationFramework.Parsers.InterfaceStatusParser import InterfaceStatusOutputParser

   with connect_ssh('ip', 'username', 'password') as ssh:
      output = ssh.send_command_get_output('sh int status')

   parser = InterfaceStatusOutputParser(output)
   for entry in parser.interfaces:
      print(f'{entry.name} - {entry.vlan} - {entry.status} - {entry.description}')


Connect SSH Documentation
=======
This function is what you call when connecting to a device, it sets up the connection and all of the
low level library and hands you an instantiated child of the CiscoFirmware object specific to the device
type you are connected to.

.. automodule:: CiscoAutomationFramework
   :members: connect_ssh

CiscoFirmware Object
=====
After connecting to a device you recieve a child of this class that is specific to IOS/Nexus based
on what is detected you are connected to. You will have all of the attributes documented here
to interact with your Cisco device.

.. autoclass:: CiscoAutomationFramework.FirmwareBase.CiscoFirmware
   :members:

Concurrency When Interacting with multiple devices
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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
