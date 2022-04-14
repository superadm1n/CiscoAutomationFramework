'''
Copyright 2021 Kyle Kowalczyk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from CiscoAutomationFramework.TransportEngines import SSHEngine
from CiscoAutomationFramework.FirmwareDetect import detect_firmware

__version__ = '0.8.19'


def connect_ssh(ip, username, password, port=22, enable_password=None, timeout=10):
    """

    Args:
        ip (str): IP address or hostname of Cisco device
        username (str): Username used to login
        password (str): Password for user
        port (int): Port to use (default 22)
        enable_password (str): Enable password to use if the user does not have privileges directly to privilege exec
        timeout (int):

    Returns: CiscoFirmware

    """

    engine = SSHEngine()
    engine.enable_password = enable_password
    engine.timeout = timeout
    engine.connect_to_server(ip, username, password, port)
    firmware = detect_firmware(engine)
    return firmware(engine)
