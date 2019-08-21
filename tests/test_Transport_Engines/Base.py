from CiscoAutomationFramework.TransportEngines import SSHEngine
import paramiko



class MyParamikoSSHClient(paramiko.SSHClient):

    def __init__(self, canned_response):
        super().__init__()
        self.canned_response = canned_response

    def invoke_shell(self, term='vt100', width=80, height=24, width_pixels=0,
                     height_pixels=0, environment=None):
        response = self.canned_response
        class Transport:
            def __init__(self):
                self.recv_response = ['{}\n'.format(x) for x in response]
                #print(self.recv_response)
                self.ready_to_recieve = True

            def recv_ready(self):
                return self.ready_to_recieve

            def send(self, command):
                if len(self.recv_response) > 0:
                    self.ready_to_recieve = True
            def recv(self, buffer_size):
                if len(self.recv_response) == 0:
                    return '#'.encode('utf-8')
                data_to_return = self.recv_response[0]
                self.recv_response.pop(0)
                #if len(self.recv_response) == 0:
                self.ready_to_recieve = False
                return data_to_return.encode('utf-8')

        cls = Transport()
        return cls

    def connect(
        self,
        hostname,
        port=20,
        username=None,
        password=None,
        pkey=None,
        key_filename=None,
        timeout=None,
        allow_agent=True,
        look_for_keys=True,
        compress=False,
        sock=None,
        gss_auth=False,
        gss_kex=False,
        gss_deleg_creds=True,
        gss_host=None,
        banner_timeout=None,
        auth_timeout=None,
        gss_trust_dns=True,
    ):
        return True


class TestableSSHEngine(SSHEngine):
    def __init__(self, canned_response):
        super().__init__()
        self.client = MyParamikoSSHClient(canned_response)
        self.all_output_recieved = []








