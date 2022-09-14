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
