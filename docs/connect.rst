
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


SSH Key Authentication
======================

By default, CiscoAutomationFramework disables automatic SSH key discovery (``look_for_keys=False`` and ``allow_agent=False``). This ensures Paramiko will never automatically probe discoverable keys in your user's ``~/.ssh/`` directory or query a running SSH agent, avoiding unexpected authentication rejects on network devices.

To authenticate using an SSH private key, specify the key file explicitly via ``key_filename`` (and optional ``passphrase``)::

    from CiscoAutomationFramework import connect_ssh

    with connect_ssh('10.1.1.1', 'admin', key_filename='/path/to/private_key.pem') as ssh:
        print(ssh.hostname)

If your private key requires a passphrase::

    with connect_ssh('10.1.1.1', 'admin', key_filename='/path/to/private_key.pem', passphrase='secret') as ssh:
        print(ssh.hostname)


Connecting Through a Linux Jump Host (Bastion)
==============================================

To connect to devices isolated behind an SSH jump host (bastion server), instantiate a :class:`~CiscoAutomationFramework.TransportEngines.JumpHost` object and pass it to :func:`~CiscoAutomationFramework.connect_ssh`::

    from CiscoAutomationFramework import connect_ssh, JumpHost

    jump = JumpHost(
        ip='192.168.1.50',
        username='bastion_user',
        password='bastion_password',
        port=22
    )

    with connect_ssh('10.1.1.1', 'cisco_user', 'cisco_password', jumphost=jump) as ssh:
        print(ssh.hostname)

Key-based authentication on the jump host is also supported by specifying ``key_filename`` (and optional ``passphrase``)::

    jump = JumpHost(
        ip='192.168.1.50',
        username='bastion_user',
        key_filename='/home/user/.ssh/id_rsa'
    )


Handling Connection and Authentication Exceptions
=================================================

The framework provides specific exception types to distinguish between jump host failures and target device failures.

Catching Specific Failures
--------------------------

To handle bastion and device errors independently::

    from CiscoAutomationFramework import connect_ssh, JumpHost
    from CiscoAutomationFramework.Exceptions import (
        DeviceAuthenticationException,
        JumpHostAuthenticationException,
        JumpHostConnectionException,
        JumpHostTunnelException,
    )

    jump = JumpHost(ip='192.168.1.50', username='jumpuser', password='jumppassword')

    try:
        with connect_ssh('10.1.1.1', 'cisco_admin', 'cisco_pass', jumphost=jump) as ssh:
            print(f'Connected to: {ssh.hostname}')

    except JumpHostAuthenticationException as exc:
        # Fired when jump host credentials (password or SSH key) are rejected
        print(f"Jump host rejected credentials: {exc}")

    except JumpHostConnectionException as exc:
        # Fired when the jump host is unreachable (timeout, connection refused)
        print(f"Unable to reach jump host: {exc}")

    except JumpHostTunnelException as exc:
        # Fired when the direct-tcpip channel to the target device fails
        print(f"Tunnel through jump host failed: {exc}")

    except DeviceAuthenticationException as exc:
        # Fired when login or AAA authorization fails on the Cisco device
        print(f"Cisco device rejected credentials on {exc.ip}: {exc}")


Catching Any Authentication Failure
-----------------------------------

Both :exc:`~CiscoAutomationFramework.Exceptions.JumpHostAuthenticationException` and
:exc:`~CiscoAutomationFramework.Exceptions.DeviceAuthenticationException` inherit from
:exc:`~CiscoAutomationFramework.Exceptions.AuthenticationException` (which also inherits from
``paramiko.AuthenticationException`` for backwards compatibility). You can catch all authentication
failures with a single block::

    from CiscoAutomationFramework import connect_ssh
    from CiscoAutomationFramework.Exceptions import AuthenticationException

    try:
        with connect_ssh('10.1.1.1', 'cisco_admin', 'bad_pass') as ssh:
            print(ssh.hostname)
    except AuthenticationException as exc:
        print(f"Authentication failed: {exc}")


.. automodule:: CiscoAutomationFramework
   :members: connect_ssh

.. autoclass:: CiscoAutomationFramework.TransportEngines.JumpHost
   :members:

.. automodule:: CiscoAutomationFramework.Exceptions
   :members: