from CiscoAutomationFramework.TransportEngines import SSHEngine, JumpHost
from CiscoAutomationFramework.FirmwareDetect import detect_firmware
from CiscoAutomationFramework.FirmwareBase import CiscoFirmware
from CiscoAutomationFramework.Exceptions import (
    CiscoAutomationFrameworkException,
    AuthenticationException,
    JumpHostAuthenticationException,
    DeviceAuthenticationException,
    JumpHostConnectionException,
    JumpHostTunnelException,
    EnablePasswordError,
    ForbiddenError,
    ParserError,
)

__version__ = '1.2.0'


def connect_ssh(ip, username, password, port=22, enable_password=None, timeout=10, engine=SSHEngine, jumphost=None) -> CiscoFirmware:
    """
    Connects to your cisco device, returns a firmware specific instance of CiscoFirmware object.

    :param ip: IP address or hostname of Cisco device
    :type ip: str

    :param username: Username used to login
    :type username: str

    :param password: Password for user
    :type password: str

    :param port: Port to use (default 22)
    :type port: int

    :param enable_password: Enable password to use if the user does not have privileges directly to privilege exec
    :type enable_password: str

    :param timeout: SSH timeout in seconds
    :type timeout: int

    :param engine: SSHEngine subclass to use for transport
    :type engine: type

    :param jumphost: Optional JumpHost object or dict for transparent SSH bastion tunneling
    :type jumphost: JumpHost or dict

    :return: CiscoFirmware Object
    :rtype: CiscoFirmware

    :raises CiscoAutomationFramework.Exceptions.DeviceAuthenticationException:
        When login credentials or AAA authorization fails on the target network device.
    :raises CiscoAutomationFramework.Exceptions.JumpHostAuthenticationException:
        When credentials (password or SSH key) fail on the Linux Jump Host.
    :raises CiscoAutomationFramework.Exceptions.JumpHostConnectionException:
        When establishing a connection to the Linux Jump Host fails.
    :raises CiscoAutomationFramework.Exceptions.JumpHostTunnelException:
        When opening the direct-tcpip forwarding tunnel through the Jump Host fails.
    :raises CiscoAutomationFramework.Exceptions.AuthenticationException:
        Base exception catching any authentication failure (both Jump Host and Device).

    """

    if engine:
        if not issubclass(engine, SSHEngine):
            raise TypeError('engine MUST be an SSHEngine!')


    engine = engine()
    engine.enable_password = enable_password
    engine.timeout = timeout
    try:
        engine.connect_to_server(ip, username, password, port, jumphost=jumphost)
    except TypeError:
        engine.connect_to_server(ip, username, password, port)
    firmware = detect_firmware(engine)
    return firmware(engine)
