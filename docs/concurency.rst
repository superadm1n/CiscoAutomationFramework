Interacting with Multiple Network Devices at the same time
======
CiscoAutomationFramework provides a way of running the same code on multiple devices
concurrently. It takes into account situations where you will have a mix of IOS and Nexus and
when you dont care, providing object to inherit from and override in both circumstances.



.. autoclass:: CiscoAutomationFramework.ThreadLib.SSH
   :members:

.. autoclass:: CiscoAutomationFramework.ThreadLib.SSHSplitDeviceType
   :members:

.. autoclass:: CiscoAutomationFramework.ThreadLib.ReadOnlySSH
   :members:

.. automodule:: CiscoAutomationFramework.ThreadLib
   :members: start_threads


Example Scripts
-----
.. literalinclude:: ExampleScripts/basic_threaded_script_example.py
   :language: python
   :linenos:
   :caption: An example script that will run concurrently across multiple network devices
