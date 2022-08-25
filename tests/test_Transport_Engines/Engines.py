from CiscoAutomationFramework.TransportEngines import BaseEngine


class BaseTestableGetOutput(BaseEngine):
    def __init__(self):
        super().__init__()
        self.canned_output = ''
        self.last_index = 0

    def connect_to_server(self, ip, username, password, port) -> bool:
        return True

    def _send_command(self, command, end) -> None:
        pass

    def close_connection(self) -> None:
        pass


class TestableSendCommand(BaseEngine):
    def __init__(self):
        super().__init__()
        self.unit_test_tracker_commands_sent = []

    def connect_to_server(self, ip, username, password, port) -> bool:
        return True

    def _send_command(self, command, end) -> None:
        self.unit_test_tracker_commands_sent.append((command, end))

    def close_connection(self) -> None:
        pass

    def _get_output(self, buffer_size) -> str:
        pass


class IdealNoDelayGetOutput(BaseTestableGetOutput):

    def load_canned_response(self, response):
        self.canned_output = response
        self.hostname = response.splitlines()[-1].rstrip('#').rstrip('>')

        # prep engine
        self.last_index = 0
        self.commands_sent_since_last_output_get += 1


    def _get_output(self, buffer_size) -> str:
        # ideal output
        new_last_index = self.last_index + buffer_size
        data = self.canned_output[self.last_index:new_last_index]
        self.last_index = new_last_index
        return data

    def get_output(self, buffer_size=100, timeout=1, no_command_sent_previous=False):
        data = super().get_output(buffer_size, timeout, no_command_sent_previous)
        self.last_index = 0
        return data



class WillTriggerTimeout(BaseTestableGetOutput):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.commands_sent_since_last_output_get = 1

    def _get_output(self, buffer_size) -> str:
        if self.flag is True:
            return ''
        else:
            self.flag = True
            return 'garbage'



