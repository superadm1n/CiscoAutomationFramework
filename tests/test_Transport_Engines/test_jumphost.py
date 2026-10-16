from unittest import TestCase
from unittest.mock import MagicMock, patch
import socket
import paramiko
from CiscoAutomationFramework.TransportEngines import JumpHost, SSHEngine
from CiscoAutomationFramework.Exceptions import (
    AuthenticationException,
    JumpHostAuthenticationException,
    DeviceAuthenticationException,
    JumpHostConnectionException,
    JumpHostTunnelException,
)


class TestJumpHost(TestCase):

    def test_init_defaults_with_password(self):
        jh = JumpHost(ip='192.168.1.100', username='bastion', password='secretpassword')
        self.assertEqual(jh.ip, '192.168.1.100')
        self.assertEqual(jh.username, 'bastion')
        self.assertEqual(jh.password, 'secretpassword')
        self.assertEqual(jh.port, 22)
        self.assertEqual(jh.timeout, 10)
        self.assertFalse(jh.look_for_keys)
        self.assertFalse(jh.allow_agent)
        self.assertEqual(repr(jh), 'JumpHost(bastion@192.168.1.100:22)')

    def test_init_with_key_file(self):
        jh = JumpHost(ip='10.0.0.1', username='ubuntu', key_filename='/path/to/key.pem', port=2222)
        self.assertEqual(jh.ip, '10.0.0.1')
        self.assertEqual(jh.port, 2222)
        self.assertEqual(jh.key_filename, '/path/to/key.pem')
        self.assertIsNone(jh.password)
        self.assertFalse(jh.look_for_keys)
        self.assertFalse(jh.allow_agent)

    def test_init_explicit_key_flags(self):
        jh = JumpHost(ip='10.0.0.1', username='user', password='pw', look_for_keys=True, allow_agent=True)
        self.assertTrue(jh.look_for_keys)
        self.assertTrue(jh.allow_agent)

    @patch('CiscoAutomationFramework.TransportEngines.SSHClient')
    def test_connect(self, mock_ssh_client_class):
        mock_client = MagicMock()
        mock_ssh_client_class.return_value = mock_client

        jh = JumpHost(ip='192.168.1.50', username='juser', password='jpass', port=2222, timeout=15)
        result_client = jh.connect()

        self.assertEqual(result_client, mock_client)
        mock_client.set_missing_host_key_policy.assert_called_once()
        mock_client.connect.assert_called_once_with(
            hostname='192.168.1.50',
            port=2222,
            username='juser',
            password='jpass',
            key_filename=None,
            pkey=None,
            passphrase=None,
            timeout=15,
            look_for_keys=False,
            allow_agent=False
        )

    @patch('CiscoAutomationFramework.TransportEngines.SSHClient')
    def test_connect_raises_jumphost_auth_exception(self, mock_ssh_client_class):
        mock_client = MagicMock()
        mock_client.connect.side_effect = paramiko.AuthenticationException("Auth failed")
        mock_ssh_client_class.return_value = mock_client

        jh = JumpHost(ip='192.168.1.50', username='juser', password='bad')
        with self.assertRaises(JumpHostAuthenticationException) as ctx:
            jh.connect()
        self.assertIn("Authentication failed on jump host", str(ctx.exception))
        self.assertEqual(ctx.exception.jumphost, jh)

    @patch('CiscoAutomationFramework.TransportEngines.SSHClient')
    def test_connect_raises_jumphost_connection_exception(self, mock_ssh_client_class):
        mock_client = MagicMock()
        mock_client.connect.side_effect = socket.error("Connection refused")
        mock_ssh_client_class.return_value = mock_client

        jh = JumpHost(ip='192.168.1.50', username='juser')
        with self.assertRaises(JumpHostConnectionException) as ctx:
            jh.connect()
        self.assertIn("Failed to connect to jump host", str(ctx.exception))
        self.assertEqual(ctx.exception.jumphost, jh)

    def test_open_channel_success(self):
        mock_client = MagicMock()
        mock_transport = MagicMock()
        mock_channel = MagicMock()

        mock_client.get_transport.return_value = mock_transport
        mock_transport.is_active.return_value = True
        mock_transport.open_channel.return_value = mock_channel

        jh = JumpHost(ip='192.168.1.50', username='juser', timeout=12)
        channel = jh.open_channel(mock_client, '10.10.10.1', 22)

        self.assertEqual(channel, mock_channel)
        mock_transport.open_channel.assert_called_once_with(
            kind='direct-tcpip',
            dest_addr=('10.10.10.1', 22),
            src_addr=('127.0.0.1', 0),
            timeout=12
        )

    def test_open_channel_no_active_transport(self):
        mock_client = MagicMock()
        mock_client.get_transport.return_value = None

        jh = JumpHost(ip='192.168.1.50', username='juser')
        with self.assertRaises(JumpHostConnectionException):
            jh.open_channel(mock_client, '10.10.10.1', 22)

    def test_open_channel_failed_to_open(self):
        mock_client = MagicMock()
        mock_transport = MagicMock()
        mock_client.get_transport.return_value = mock_transport
        mock_transport.is_active.return_value = True
        mock_transport.open_channel.return_value = None

        jh = JumpHost(ip='192.168.1.50', username='juser')
        with self.assertRaises(JumpHostTunnelException):
            jh.open_channel(mock_client, '10.10.10.1', 22)

    def test_open_channel_ssh_exception(self):
        mock_client = MagicMock()
        mock_transport = MagicMock()
        mock_client.get_transport.return_value = mock_transport
        mock_transport.is_active.return_value = True
        mock_transport.open_channel.side_effect = paramiko.SSHException("Channel error")

        jh = JumpHost(ip='192.168.1.50', username='juser')
        with self.assertRaises(JumpHostTunnelException) as ctx:
            jh.open_channel(mock_client, '10.10.10.1', 22)
        self.assertEqual(ctx.exception.dest_ip, '10.10.10.1')
        self.assertEqual(ctx.exception.dest_port, 22)


class TestSSHEngineTunneling(TestCase):

    def setUp(self):
        self.engine = SSHEngine()

    def test_engine_defaults_disable_key_search(self):
        self.assertFalse(self.engine.look_for_keys)
        self.assertFalse(self.engine.allow_agent)

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    def test_connect_to_server_direct(self, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client

        self.engine.connect_to_server('10.1.1.1', 'admin', 'pw', port=22, jumphost=None)

        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password='pw',
            key_filename=None,
            pkey=None,
            passphrase=None,
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
            sock=None
        )
        self.assertIsNone(self.engine.jump_client)
        self.assertIsNone(self.engine.jump_channel)

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    def test_connect_to_server_with_key_filename(self, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client

        self.engine.connect_to_server(
            '10.1.1.1', 'admin',
            key_filename='/path/to/key.pem',
            passphrase='secret',
            port=22
        )

        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password=None,
            key_filename='/path/to/key.pem',
            pkey=None,
            passphrase='secret',
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
            sock=None
        )

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    def test_connect_to_server_with_pkey(self, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client
        mock_pkey = MagicMock()

        self.engine.connect_to_server('10.1.1.1', 'admin', pkey=mock_pkey, port=22)

        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password=None,
            key_filename=None,
            pkey=mock_pkey,
            passphrase=None,
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
            sock=None
        )

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    def test_connect_to_server_override_look_for_keys(self, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client

        self.engine.connect_to_server('10.1.1.1', 'admin', 'pw', look_for_keys=True, allow_agent=True)

        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password='pw',
            key_filename=None,
            pkey=None,
            passphrase=None,
            timeout=10,
            look_for_keys=True,
            allow_agent=True,
            sock=None
        )

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    def test_connect_to_server_with_jumphost_instance(self, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client

        mock_jump_client = MagicMock()
        mock_jump_channel = MagicMock()

        jh = MagicMock(spec=JumpHost)
        jh.connect.return_value = mock_jump_client
        jh.open_channel.return_value = mock_jump_channel

        self.engine.connect_to_server('10.1.1.1', 'admin', 'pw', port=22, jumphost=jh)

        jh.connect.assert_called_once()
        jh.open_channel.assert_called_once_with(mock_jump_client, '10.1.1.1', 22)
        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password='pw',
            key_filename=None,
            pkey=None,
            passphrase=None,
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
            sock=mock_jump_channel
        )
        self.assertEqual(self.engine.jump_client, mock_jump_client)
        self.assertEqual(self.engine.jump_channel, mock_jump_channel)

    @patch.object(SSHEngine, '_get_prompt_and_hostname', return_value=('router#', 'router'))
    @patch.object(JumpHost, 'connect')
    @patch.object(JumpHost, 'open_channel')
    def test_connect_to_server_with_dict(self, mock_open_channel, mock_connect, mock_prompt):
        mock_client = MagicMock()
        self.engine.client = mock_client

        mock_jump_client = MagicMock()
        mock_jump_channel = MagicMock()
        mock_connect.return_value = mock_jump_client
        mock_open_channel.return_value = mock_jump_channel

        jh_dict = {'ip': '192.168.1.50', 'username': 'jumpuser', 'password': 'jumppass'}
        self.engine.connect_to_server('10.1.1.1', 'admin', 'pw', port=22, jumphost=jh_dict)

        mock_connect.assert_called_once()
        mock_client.connect.assert_called_once_with(
            hostname='10.1.1.1',
            port=22,
            username='admin',
            password='pw',
            key_filename=None,
            pkey=None,
            passphrase=None,
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
            sock=mock_jump_channel
        )

    def test_connect_to_server_raises_device_auth_exception(self):
        mock_client = MagicMock()
        mock_client.connect.side_effect = paramiko.AuthenticationException("Bad credentials")
        self.engine.client = mock_client

        with self.assertRaises(DeviceAuthenticationException) as ctx:
            self.engine.connect_to_server('10.1.1.1', 'admin', 'badpw', port=22)
        self.assertEqual(ctx.exception.ip, '10.1.1.1')
        self.assertEqual(ctx.exception.username, 'admin')
        self.assertIn("Authentication failed on network device '10.1.1.1'", str(ctx.exception))

    def test_connect_to_server_invalid_jumphost_type(self):
        with self.assertRaises(TypeError):
            self.engine.connect_to_server('10.1.1.1', 'admin', 'pw', port=22, jumphost=12345)

    def test_close_connection_cleans_up_jumphost(self):
        mock_shell = MagicMock()
        mock_client = MagicMock()
        mock_jump_channel = MagicMock()
        mock_jump_client = MagicMock()

        self.engine.shell = mock_shell
        self.engine.client = mock_client
        self.engine.jump_channel = mock_jump_channel
        self.engine.jump_client = mock_jump_client

        self.engine.close_connection()

        mock_shell.close.assert_called_once()
        mock_client.close.assert_called_once()
        mock_jump_channel.close.assert_called_once()
        mock_jump_client.close.assert_called_once()
        self.assertIsNone(self.engine.jump_channel)
        self.assertIsNone(self.engine.jump_client)


class TestExceptionHierarchy(TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(JumpHostAuthenticationException, AuthenticationException))
        self.assertTrue(issubclass(DeviceAuthenticationException, AuthenticationException))
        self.assertTrue(issubclass(AuthenticationException, paramiko.AuthenticationException))

    def test_catch_all_authentication_exception(self):
        jump_err = JumpHostAuthenticationException("jump failed")
        device_err = DeviceAuthenticationException("device failed")

        caught_jump = False
        try:
            raise jump_err
        except AuthenticationException:
            caught_jump = True
        self.assertTrue(caught_jump)

        caught_device = False
        try:
            raise device_err
        except AuthenticationException:
            caught_device = True
        self.assertTrue(caught_device)

    def test_paramiko_compatibility(self):
        device_err = DeviceAuthenticationException("device failed")
        caught_paramiko = False
        try:
            raise device_err
        except paramiko.AuthenticationException:
            caught_paramiko = True
        self.assertTrue(caught_paramiko)
