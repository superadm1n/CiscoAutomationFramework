Usage Examples
==============

Below are some example scripts showing how to use the framework to interact with remote devices

Display running config using SSH
--------------------------------

.. code-block:: python

    from CiscoAutomationFramework import connect_ssh

    # credentials for remote device
    ip = '192.168.1.1'
    username = 'user4'
    password = 'password1'
    enable_password = 'myenablePassword1'

    # log into device and capture the running config
    with connect_ssh(ip, username, password, enable_password) as ssh:
        running_config = ssh.show_run()

    # print running config
    print(running_config)

List the number of ports on a device using SSH
----------------------------------------------

.. code-block:: python

    from CiscoAutomationFramework import connect_ssh

    # credentials for remote device
    ip = '192.168.1.1'
    username = 'user4'
    password = 'password1'
    enable_password = 'myenablePassword1'

    # log into device and capture the running config
    with connect_ssh(ip, username, password, enable_password) as ssh:
        hostname = ssh.hostname
        port_inv = ssh.physical_port_inventory_longname()

    # print running config
    print('Device {} has a total of {} ports'.format(hostname, len(port_inv)))

List running config of a device using serial interface
------------------------------------------------------

.. code-block:: python

    from CiscoAutomationFramework import connect_serial

    # credentials for remote device
    interface = 'COM4'
    username = 'user4'
    password = 'password1'
    enable_password = 'myenablePassword1'

    # log into device and capture the running config
    with connect_serial(interface, username, password, enable_password) as serial:
        running_config = serial.show_run()

    # print running config
    print(running_config)

