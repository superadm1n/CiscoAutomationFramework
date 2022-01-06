from CiscoAutomationFramework.TransportEngines import SSHEngine
from CiscoAutomationFramework.FirmwareDetect import detect_firmware

__version__ = '0.8.11'

def connect_ssh(ip, username, password, port=22, enable_password=None):
    engine = SSHEngine()
    engine.connect_to_server(ip, username, password, port)
    firmware = detect_firmware(engine)
    return firmware(engine)
