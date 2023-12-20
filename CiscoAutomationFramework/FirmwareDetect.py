from CiscoAutomationFramework.TransportEngines import BaseEngine
from CiscoAutomationFramework.IOS import IOS
from CiscoAutomationFramework.IOSXE import IOSXE
from CiscoAutomationFramework.NXOS import NXOS
from inspect import getmodule
from time import sleep


def detect_firmware(transport):
    if not isinstance(transport, BaseEngine):
        raise TypeError(f'transport argument MUST be an instance of {getmodule(BaseEngine).__name__}.{BaseEngine.__name__}')

    show_version = transport.send_command_get_truncated_output('show version')

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



