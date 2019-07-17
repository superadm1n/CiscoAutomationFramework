'''
Copyright 2018 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

===========================================================================


'''
log_level = 10
log_to_console = True
from . import Util
from .TransportEngines import SSHEngine, SerialEngine
from .CiscoIOSXE import IOSXE
from .CiscoIOS import IOS
from .CiscoNXOS import NXOS
from .CiscoASA import ASA
from . import CustomExceptions

def factory(transport_engine):

    # detect the firmware
    sh_ver_output, firmware = Util.detect_firmware(transport_engine)
    detected_firmware_version_number = None

    # determine parent object based on firmware
    obj = None
    versions = {'IOS': IOS, 'IOSXE': IOSXE, 'NXOS': NXOS, 'ASA': ASA}
    if firmware == 'IOS':
        obj = IOS
        detected_firmware_version_number = Util.extract_version_number_ios(sh_ver_output)
    elif firmware == 'IOSXE':
        obj = IOSXE
        detected_firmware_version_number = Util.extract_version_number_iosxe(sh_ver_output)
    elif firmware == 'NXOS':
        obj = NXOS
        detected_firmware_version_number = Util.extract_version_number_nxos(sh_ver_output)
    elif firmware == 'ASA':
        raise CustomExceptions.OSNotSupported('Cisco ASA Operating System is not supported!')
    else:
        raise CustomExceptions.OsDetectionFailure('Unable to detect OS for device')

    # Build Interface Class
    class CAF(obj):
        def __init__(self, transport):
            self.transport = transport
            self.firmware = firmware
            self.hostname = transport.hostname
            self.detected_firmware_version = detected_firmware_version_number
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
