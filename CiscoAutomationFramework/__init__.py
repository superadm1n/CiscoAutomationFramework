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
log_level = 60
log_to_console = True
from . import Util
from CiscoAutomationFramework.TransportEngines import SSHEngine
from CiscoAutomationFramework.IOSXE import IOSXE
from CiscoAutomationFramework.IOS import IOS
from CiscoAutomationFramework.NXOS import NXOS
from CiscoAutomationFramework import CustomExceptions
from inspect import signature
from types import FunctionType

__version__ = '0.8.8'


class ParameterError(Exception):
    pass


def _inspect_error_handler(error_handler):
    """
    Method to inspect the error handler method that is intended to be passed into connect_ssh or connect_serial
    It checks that it is a function and also checks that it accepts 1 parameter if both of those conditions
    are not met it will raise an appropriate error.
    """
    num_accepted_parameters = 2

    if type(error_handler) != FunctionType:
        raise TypeError('Data handler must be a function')
    if len(signature(error_handler).parameters) != num_accepted_parameters:
        raise ParameterError('Data Handler Must accept {} parameter'.format(num_accepted_parameters))


def connect_ssh(ip, username, password, enable_password=None, error_handler=None):
    if error_handler:
        _inspect_error_handler(error_handler)

    transport_engine = SSHEngine(error_handler=error_handler)
    transport_engine.enable_password = enable_password
    transport_engine.connect_to_server(ip, username, password)

    sh_ver_output, firmware = Util.detect_firmware(transport_engine)

    # determine parent object based on firmware
    versions = {'IOS': IOS, 'IOSXE': IOSXE, 'NXOS': NXOS}
    obj = versions.get(firmware)

    if firmware == 'ASA':
        raise CustomExceptions.OSNotSupported('Cisco ASA Operating System is not supported!')
    if not obj:
        raise CustomExceptions.OsDetectionFailure('Unable to detect OS for device')

    return obj(transport_engine)


def connect_serial(COM, username, password, enable_password=None, error_handler=None):
    if error_handler:
        _inspect_error_handler(error_handler)

    transport_engine = SerialEngine(error_handler=error_handler)
    transport_engine.enable_password = enable_password
    transport_engine.connect_to_server(COM, username, password)

    sh_ver_output, firmware = Util.detect_firmware(transport_engine)

    # determine parent object based on firmware
    versions = {'IOS': IOS, 'IOSXE': IOSXE, 'NXOS': NXOS}
    obj = versions.get(firmware)

    if firmware == 'ASA':
        raise CustomExceptions.OSNotSupported('Cisco ASA Operating System is not supported!')
    if not obj:
        raise CustomExceptions.OsDetectionFailure('Unable to detect OS for device')

    return obj(transport_engine)
