'''
Author: Kyle Kowalczyk
Purpose: Provide a scripting interface via SSH to Cisco IOS, IOSXE, and NXOS devices for scripting administration and change tasks
Version: v0.58
Notes:
'''

from . import Util
from .TransportEngines import SSHEngine, SerialEngine
from .CiscoIOSXE import IOSXE
from .CiscoIOS import IOS
from .CiscoNXOS import NXOS
from .CiscoASA import ASA
from . import CustomExceptions

def factory(transport_engine):

    # detect the firmware
    firmware = Util.detect_firmware(transport_engine)

    # determine parent object based on firmware
    if firmware == 'IOS':
        obj = IOS
    elif firmware == 'IOSXE':
        obj = IOSXE
    elif firmware == 'NXOS':
        obj = NXOS
    elif firmware == 'ASA':
        obj = ASA
    else:
        raise CustomExceptions.OsDetectionFailure('Unable to detect OS for device')

    # Build Interface Class
    class CAF(obj):
        def __init__(self, transport):
            self.transport = transport
            super().__init__(transport)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.transport.close_connection()

    return CAF(transport_engine)


def connect_ssh(ip, username, password, enable_password=None):
    ssh = SSHEngine()
    ssh.enable_password = enable_password
    ssh.connect_to_server(ip, username, password)
    return factory(ssh)


def connect_serial(COM, username, password, enable_password=None):
    ser = SerialEngine()
    ser.enable_password = enable_password
    ser.connect_to_server(COM, username, password)
    return factory(ser)