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
from CiscoAutomationFramework.TransportEngines import BaseEngine
from CiscoAutomationFramework.IOS import IOS
from CiscoAutomationFramework.IOSXE import IOSXE
from CiscoAutomationFramework.NXOS import NXOS
from inspect import getmodule


def detect_firmware(transport):
    if not isinstance(transport, BaseEngine):
        raise TypeError(f'transport argument MUST be an instance of {getmodule(BaseEngine).__name__}.{BaseEngine.__name__}')

    _ = transport.send_command_get_output('terminal length 0')
    show_version = transport.send_command_get_output('show version')

    results = {'IOSXE': 0, 'IOS': 0, 'NXOS': 0, 'ASA': 0}
    for line in show_version[:10]:
        if 'ios-xe' in line.lower() or 'ios xe' in line.lower():
            results['IOSXE'] += 1
        elif 'ios' in line.lower():
            results['IOS'] += 1
        elif 'nx-os' in line.lower():
            results['NXOS'] += 1
        elif 'adaptive security appliance' in line.lower():
            results['ASA'] += 1

    # stores the key with the highest value in a variable
    firmware_version = max(results, key=results.get)
    firmware_object = {'IOS': IOS, 'IOSXE': IOSXE, 'NXOS': NXOS}.get(firmware_version)

    # returns firmware object
    return firmware_object



