
How To Connect to A Network Device
======
Calling the CiscoAutomationFramework.connect_ssh function is how you connect to a device.
it sets up the connection and all of the
low level library and hands you an instantiated child of the CiscoFirmware object specific to the device
type you are connected to.

You can connect by assigning the output directly to a variable::

    from CiscoAutomationFramework import connect_ssh
    ssh = connect_ssh('ip', 'username', 'password')
    #other code here
    ssh.close_connection()

However It is recommended to use a context manager so you dont have to remember to close the connection
or if an exception if hit in your code it closes for you::

    from CiscoAutomationFramework import connect_ssh
    with connect_ssh('ip', 'username', 'password') as ssh:
        # Code here while logged into the device
    # Code here while logged out of the device




.. automodule:: CiscoAutomationFramework
   :members: connect_ssh