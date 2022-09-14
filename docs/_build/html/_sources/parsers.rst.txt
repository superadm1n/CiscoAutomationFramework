Command Output Parsers
======
CiscoAutomationFramework provides integrated parsers for various command outputs. These parsers allow
you to pass in the output from the network device and be able to iterate over output and/or extract
data from the output in a programatic way versus needing to build your own parsers

Show Interface Status Parser
-----
Pass in the raw output from "show interface status" command to this parser and you will be
able to iterate over the table and interact with the entries individually

.. autoclass:: CiscoAutomationFramework.Parsers.InterfaceStatusParser.InterfaceStatusOutputParser
   :members:

.. autoclass:: CiscoAutomationFramework.Parsers.InterfaceStatusParser.LineParser
   :members:


IP Device Tracking Parser
------
Pass in the raw output from "show ip device tracking all" and this parser allows you to iterate
over the contents of the table one at a time.

.. autoclass:: CiscoAutomationFramework.Parsers.IpDeviceTrackingParser.DeviceTrackingOutputParser
   :members:

.. autoclass:: CiscoAutomationFramework.Parsers.IpDeviceTrackingParser.EntryParser
   :members:

MAC Address Table Parser
------
Pass in the raw output from "show mac address-table" and this parser allows you to iterate
over the contents of the table one at a time and also analyze the table in other ways.::

   from CiscoAutomationFramework import connect_ssh
   from CiscoAutomationFramework.Parsers.MacAddressTableParser import MacAddressTableParser

   with connect_ssh('ip', 'username', 'password') as ssh:
      mac_table = MacAddressTableParser(ssh.mac_address_table)

   for entry in mac_table:
      print(f'{entry.interface} - {entry.vlan} - {entry.mac_address}')


.. autoclass:: CiscoAutomationFramework.Parsers.MacAddressTableParser.MacAddressTableParser
   :members:

.. autoclass:: CiscoAutomationFramework.Parsers.MacAddressTableParser.MacEntryParser
   :members:


Power Inline Parser
------
Pass the raw output from 'show power inline' to this parser and you will
be able to iterate over the entries in the power inline table::

    from CiscoAutomationFramework import connect_ssh
    from CiscoAutomationFramework.Parsers.PowerInlineParser import PowerInlineParser

    with connect_ssh('ip', 'username', 'password') as ssh:
        parser = PowerInlineParser(ssh.send_command_get_output('show power inline'))

    for entry in parser:
        print(f'{entry.name} - {entry.watts} - {entry.detected_device}')


.. autoclass:: CiscoAutomationFramework.Parsers.PowerInlineParser.PowerInlineParser
   :members:

.. autoclass:: CiscoAutomationFramework.Parsers.PowerInlineParser.PowerInlineInterface
   :members: