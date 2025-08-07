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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   connect
   interact
   concurency
   parsers
   utilities

Example Usage
========

Basic connection to a device::

   from CiscoAutomationFramework import connect_ssh
   ssh = connect_ssh('ipaddress', 'username', 'password')
   print(ssh.running_config)
   print(ssh.startup_config)
   print(ssh.arp_table)
   print(ssh.mac_address_table)
   ssh.close_connection()

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


Indices and tables
==================


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
