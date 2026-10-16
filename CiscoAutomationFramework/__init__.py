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
import inspect

__version__ = '1.3.0'


def connect_ssh(ip, username, password=None, port=22, enable_password=None, timeout=10,
                engine=SSHEngine, jumphost=None,
                key_filename=None, pkey=None, passphrase=None,
                look_for_keys=False, allow_agent=False, **kwargs) -> CiscoFirmware:
    """
    Connects to your cisco device, returns a firmware specific instance of CiscoFirmware object.

    :param ip: IP address or hostname of Cisco device
    :type ip: str

    :param username: Username used to login
    :type username: str

    :param password: Password for user (optional if key_filename or pkey is provided)
    :type password: str or None

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

    :param key_filename: Path to private key file for SSH key authentication
    :type key_filename: str or None

    :param pkey: Paramiko PKey object for SSH key authentication
    :type pkey: paramiko.PKey or None

    :param passphrase: Password/passphrase for decrypting the private key
    :type passphrase: str or None

    :param look_for_keys: Search ~/.ssh/ for discoverable keys (default False)
    :type look_for_keys: bool

    :param allow_agent: Query SSH agent for keys (default False)
    :type allow_agent: bool

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

    connect_kwargs = {
        'port': port,
        'jumphost': jumphost,
        'key_filename': key_filename,
        'pkey': pkey,
        'passphrase': passphrase,
        'look_for_keys': look_for_keys,
        'allow_agent': allow_agent,
    }
    connect_kwargs.update(kwargs)

    sig = inspect.signature(engine.connect_to_server)
    params = sig.parameters
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())

    if has_var_keyword:
        engine.connect_to_server(ip, username, password=password, **connect_kwargs)
    else:
        filtered_kwargs = {k: v for k, v in connect_kwargs.items() if k in params}
        engine.connect_to_server(ip, username, password=password, **filtered_kwargs)

    firmware = detect_firmware(engine)
    return firmware(engine)
