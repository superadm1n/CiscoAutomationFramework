from CiscoAutomationFramework.TransportEngines import SSHEngine, SerialEngine
from CiscoAutomationFramework import IOS, IOSXE, NXOS, ASA



def factory(transport_engine, firmware_command_class):



    # Build Interface Class
    class CAF(firmware_command_class):
        def __init__(self, transport):
            self.transport = transport
            self.firmware = 'firmware'
            self.hostname = 'test_sw'
            super().__init__(transport)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.transport.close_connection()

    return CAF(transport_engine)


class TestingSSHEngine(SSHEngine):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.commands_ran = []

        self.response_zero = ''
        self.response_one = ''
        self.response_two = ''
        self.response_three = ''
        self.response_four = ''
        self.response_five = ''
        self.response_six = ''
        self.response_seven = ''
        self.response_eight = ''
        self.response_nine = ''

    def connect_to_server(self, ip, username, password):
        return None

    def send_command(self, command):
        self.commands_ran.append(command)

    def get_output(self, wait_time=.2, detecting_firmware=False, return_as_list=False, buffer_size=1, timeout=10):
        response = None

        if self.counter == 0:
            response = self.response_zero
        elif self.counter == 1:
            response = self.response_one
        elif self.counter == 2:
            response = self.response_two
        elif self.counter == 3:
            response = self.response_three
        elif self.counter == 4:
            response = self.response_four
        elif self.counter == 5:
            response = self.response_five
        elif self.counter == 6:
            response = self.response_six
        elif self.counter == 7:
            response = self.response_seven
        elif self.counter == 8:
            response = self.response_eight
        elif self.counter == 9:
            response = self.response_nine

        self.counter += 1

        return response



