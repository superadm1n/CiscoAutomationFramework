from CiscoAutomationFramework.TransportEngines import BaseEngine
from CiscoAutomationFramework.FirmwareBase import CiscoFirmware

class TestableCiscoFirmware(CiscoFirmware):
    pass

class IdealNoDelayGetOutput(BaseEngine):

    def __init__(self, hostname, prompt):
        super().__init__()
        self.hostname = hostname
        self.prompt = prompt
        self.canned_output = []
        self.last_index = 0
        self._unit_test_commands_sent = []

    def connect_to_server(self, ip, username, password, port) -> bool:
        return True

    def _send_command(self, command, end) -> None:
        self._unit_test_commands_sent.append((command, end))

    def close_connection(self) -> None:
        pass

    def load_canned_response(self, response):
        self.canned_output.append(response)

    def _get_output(self, buffer_size) -> str:
        # ideal output
        new_last_index = self.last_index + buffer_size
        data = self.canned_output[0][self.last_index:new_last_index]
        self.last_index = new_last_index
        return data

    def get_output(self, buffer_size=100, timeout=1, no_command_sent_previous=False):
        data = super().get_output(buffer_size, timeout, no_command_sent_previous)
        self.last_index = 0
        self.canned_output.pop(0)
        return data