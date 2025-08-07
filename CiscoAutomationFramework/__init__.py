from CiscoAutomationFramework.TransportEngines import SSHEngine
from CiscoAutomationFramework.FirmwareDetect import detect_firmware
from CiscoAutomationFramework.FirmwareBase import CiscoFirmware


def connect_ssh(ip, username, password, port=22, enable_password=None, timeout=10, engine=SSHEngine) -> CiscoFirmware:
    """
    Connects to your cisco device, returns a firmware specific instance of CiscoFirmware object.

    :param ip: IP address or hostname of Cisco device
    :type ip: str

    :param username: Username used to login
    :type username: str

    :param password: Password for user
    :type password: str

    :param port:  Port to use (default 22)
    :type port: int

    :param enable_password: Enable password to use if the user does not have privileges directly to privilege exec
    :type enable_password: str

    :param timeout: SSH timeout in seconds
    :type timeout: int

    :param

    :return: CiscoFirmware Object
    :rtype: CiscoFirmware

    """

    if engine:
        if not issubclass(engine, SSHEngine):
            raise TypeError('engine MUST be an SSHEngine!')


    engine = engine()
    engine.enable_password = enable_password
    engine.timeout = timeout
    engine.connect_to_server(ip, username, password, port)
    firmware = detect_firmware(engine)
    return firmware(engine)
