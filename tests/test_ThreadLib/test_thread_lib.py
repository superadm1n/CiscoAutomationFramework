from unittest import TestCase
from unittest.mock import MagicMock, patch
from CiscoAutomationFramework.ThreadLib import (
    SSH, ReadOnlySSH, SSHSplitDeviceType, start_threads,
    _is_jumphost_config_dict, _resolve_jumphost
)
from CiscoAutomationFramework.TransportEngines import JumpHost, SSHEngine
from CiscoAutomationFramework import connect_ssh


class DummySSH(SSH):
    def during_login(self, ssh):
        pass


class DummySplitSSH(SSHSplitDeviceType):
    def ios_during_login(self, ssh):
        pass

    def nexus_during_login(self, ssh):
        pass

    def ios_secondary_action(self, ssh):
        pass

    def nexus_secondary_action(self, ssh):
        pass

    def ios_post_secondary_action(self, ssh):
        pass

    def nexus_post_secondary_action(self, ssh):
        pass


class TestJumphostResolvers(TestCase):

    def test_is_jumphost_config_dict(self):
        self.assertTrue(_is_jumphost_config_dict({'ip': '1.1.1.1', 'username': 'user'}))
        self.assertTrue(_is_jumphost_config_dict({'hostname': 'jump.local', 'username': 'user'}))
        self.assertFalse(_is_jumphost_config_dict({'10.1.1.1': JumpHost('1.1.1.1', 'user')}))
        self.assertFalse(_is_jumphost_config_dict('not a dict'))
        self.assertFalse(_is_jumphost_config_dict({'ip': '1.1.1.1'}))  # missing username

    def test_resolve_jumphost_none(self):
        self.assertIsNone(_resolve_jumphost(None, '10.1.1.1', 0))

    def test_resolve_jumphost_object(self):
        jh = JumpHost('1.1.1.1', 'user')
        self.assertEqual(_resolve_jumphost(jh, '10.1.1.1', 0), jh)
        self.assertEqual(_resolve_jumphost(jh, '10.2.2.2', 1), jh)

    def test_resolve_jumphost_config_dict(self):
        cfg = {'ip': '1.1.1.1', 'username': 'user'}
        self.assertEqual(_resolve_jumphost(cfg, '10.1.1.1', 0), cfg)

    def test_resolve_jumphost_mapping_dict(self):
        jh1 = JumpHost('1.1.1.1', 'user')
        jh2 = JumpHost('2.2.2.2', 'user')
        mapping = {'10.1.1.1': jh1, '10.2.2.2': jh2}
        self.assertEqual(_resolve_jumphost(mapping, '10.1.1.1', 0), jh1)
        self.assertEqual(_resolve_jumphost(mapping, '10.2.2.2', 1), jh2)
        self.assertIsNone(_resolve_jumphost(mapping, '10.3.3.3', 2))

    def test_resolve_jumphost_list(self):
        jh1 = JumpHost('1.1.1.1', 'user')
        jh2 = JumpHost('2.2.2.2', 'user')
        jh_list = [jh1, jh2]
        self.assertEqual(_resolve_jumphost(jh_list, '10.1.1.1', 0), jh1)
        self.assertEqual(_resolve_jumphost(jh_list, '10.2.2.2', 1), jh2)
        self.assertIsNone(_resolve_jumphost(jh_list, '10.3.3.3', 2))

    def test_resolve_jumphost_callable(self):
        jh_east = JumpHost('1.1.1.1', 'user')
        jh_west = JumpHost('2.2.2.2', 'user')
        router = lambda ip: jh_east if ip.startswith('10.1') else jh_west
        self.assertEqual(_resolve_jumphost(router, '10.1.5.1', 0), jh_east)
        self.assertEqual(_resolve_jumphost(router, '10.2.5.1', 1), jh_west)


class TestSSHClass(TestCase):

    def test_ssh_init_defaults(self):
        worker = DummySSH('10.1.1.1', 'admin', 'pass')
        self.assertEqual(worker.ip, '10.1.1.1')
        self.assertEqual(worker.username, 'admin')
        self.assertEqual(worker.password, 'pass')
        self.assertIsNone(worker.enable_password)
        self.assertFalse(worker.perform_secondary_action)
        self.assertIsNone(worker.jumphost)

    def test_ssh_init_with_jumphost(self):
        jh = JumpHost('1.1.1.1', 'jumpuser')
        worker = DummySSH('10.1.1.1', 'admin', 'pass', jumphost=jh)
        self.assertEqual(worker.jumphost, jh)

    @patch('CiscoAutomationFramework.ThreadLib.connect_ssh')
    def test_ssh_run_passes_jumphost(self, mock_connect_ssh):
        mock_ctx = MagicMock()
        mock_device = MagicMock()
        mock_device.is_nexus = False
        mock_device.hostname = 'switch1'
        mock_device.commands_sent = []
        mock_ctx.__enter__.return_value = mock_device
        mock_connect_ssh.return_value = mock_ctx

        jh = JumpHost('1.1.1.1', 'jumpuser')
        worker = DummySSH('10.1.1.1', 'admin', 'pass', jumphost=jh)
        worker.run()

        mock_connect_ssh.assert_called_once_with(
            '10.1.1.1', 'admin', 'pass',
            enable_password=None,
            engine=SSHEngine,
            jumphost=jh
        )

    @patch('CiscoAutomationFramework.ThreadLib.connect_ssh')
    def test_ssh_run_passes_key_auth(self, mock_connect_ssh):
        mock_ctx = MagicMock()
        mock_device = MagicMock()
        mock_device.is_nexus = False
        mock_device.hostname = 'switch1'
        mock_device.commands_sent = []
        mock_ctx.__enter__.return_value = mock_device
        mock_connect_ssh.return_value = mock_ctx

        worker = DummySSH('10.1.1.1', 'admin', key_filename='/path/to/key.pem', passphrase='secret')
        worker.run()

        mock_connect_ssh.assert_called_once_with(
            '10.1.1.1', 'admin', None,
            enable_password=None,
            engine=SSHEngine,
            jumphost=None,
            key_filename='/path/to/key.pem',
            passphrase='secret'
        )

    @patch('CiscoAutomationFramework.ThreadLib.connect_ssh')
    def test_ssh_run_captures_error(self, mock_connect_ssh):
        from CiscoAutomationFramework.Exceptions import DeviceAuthenticationException
        auth_err = DeviceAuthenticationException("Login failed", ip='10.1.1.1', username='admin')
        mock_connect_ssh.side_effect = auth_err

        worker = DummySSH('10.1.1.1', 'admin', 'badpass')
        with self.assertRaises(DeviceAuthenticationException):
            worker.run()

        self.assertEqual(worker.error, auth_err)


class TestStartThreads(TestCase):

    @patch.object(DummySSH, 'start')
    def test_start_threads_with_key_filename(self, mock_start):
        threads = start_threads(
            DummySSH, ['10.1.1.1'], 'admin',
            key_filename='/path/to/key.pem', passphrase='pass'
        )
        self.assertEqual(len(threads), 1)
        self.assertIsNone(threads[0].password)
        self.assertEqual(threads[0].key_filename, '/path/to/key.pem')
        self.assertEqual(threads[0].passphrase, 'pass')
        self.assertFalse(threads[0].look_for_keys)
        self.assertFalse(threads[0].allow_agent)

    @patch.object(DummySSH, 'start')
    def test_start_threads_no_jumphost(self, mock_start):
        threads = start_threads(DummySSH, ['10.1.1.1', '10.1.1.2'], 'admin', 'pass')
        self.assertEqual(len(threads), 2)
        self.assertIsNone(threads[0].jumphost)
        self.assertIsNone(threads[1].jumphost)
        self.assertEqual(mock_start.call_count, 2)

    @patch.object(DummySSH, 'start')
    def test_start_threads_single_jumphost(self, mock_start):
        jh = JumpHost('192.168.1.100', 'jumpuser')
        threads = start_threads(DummySSH, ['10.1.1.1', '10.1.1.2'], 'admin', 'pass', jumphost=jh)
        self.assertEqual(threads[0].jumphost, jh)
        self.assertEqual(threads[1].jumphost, jh)

    @patch.object(DummySSH, 'start')
    def test_start_threads_jumphost_mapping(self, mock_start):
        jh1 = JumpHost('192.168.1.101', 'jump1')
        jh2 = JumpHost('192.168.1.102', 'jump2')
        mapping = {'10.1.1.1': jh1, '10.1.1.2': jh2}
        threads = start_threads(DummySSH, ['10.1.1.1', '10.1.1.2', '10.1.1.3'], 'admin', 'pass', jumphost=mapping)
        self.assertEqual(threads[0].jumphost, jh1)
        self.assertEqual(threads[1].jumphost, jh2)
        self.assertIsNone(threads[2].jumphost)

    @patch.object(DummySSH, 'start')
    def test_start_threads_with_tuples(self, mock_start):
        jh1 = JumpHost('192.168.1.101', 'jump1')
        targets = [('10.1.1.1', jh1), ('10.1.1.2', None)]
        threads = start_threads(DummySSH, targets, 'admin', 'pass')
        self.assertEqual(threads[0].ip, '10.1.1.1')
        self.assertEqual(threads[0].jumphost, jh1)
        self.assertEqual(threads[1].ip, '10.1.1.2')
        self.assertIsNone(threads[1].jumphost)

    @patch.object(DummySSH, 'start')
    def test_start_threads_with_callable(self, mock_start):
        jh_east = JumpHost('1.1.1.1', 'east')
        jh_west = JumpHost('2.2.2.2', 'west')
        threads = start_threads(
            DummySSH, ['10.1.0.1', '10.2.0.1'], 'admin', 'pass',
            jumphost=lambda ip: jh_east if '10.1' in ip else jh_west
        )
        self.assertEqual(threads[0].jumphost, jh_east)
        self.assertEqual(threads[1].jumphost, jh_west)


class TestConnectSSH(TestCase):

    @patch('CiscoAutomationFramework.detect_firmware')
    def test_connect_ssh_passes_jumphost(self, mock_detect_firmware):
        mock_firmware_class = MagicMock()
        mock_detect_firmware.return_value = mock_firmware_class

        class RecordingEngine(SSHEngine):
            def __init__(self):
                self.enable_password = None
                self.timeout = 10
                self.recorded_call = None

            def connect_to_server(self, ip, username, password, port=22, jumphost=None):
                self.recorded_call = (ip, username, password, port, jumphost)

        jh = JumpHost('192.168.1.1', 'jumpuser')
        # We patch RecordingEngine instantiation or inspect instance
        created_instances = []
        original_init = RecordingEngine.__init__

        def tracked_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            created_instances.append(self)

        RecordingEngine.__init__ = tracked_init

        connect_ssh('10.1.1.1', 'admin', 'pass', engine=RecordingEngine, jumphost=jh)

        self.assertEqual(len(created_instances), 1)
        self.assertEqual(
            created_instances[0].recorded_call,
            ('10.1.1.1', 'admin', 'pass', 22, jh)
        )

    @patch('CiscoAutomationFramework.detect_firmware')
    def test_connect_ssh_passes_key_auth_params(self, mock_detect_firmware):
        mock_firmware_class = MagicMock()
        mock_detect_firmware.return_value = mock_firmware_class

        class KeyRecordingEngine(SSHEngine):
            def __init__(self):
                self.enable_password = None
                self.timeout = 10
                self.recorded_kwargs = None

            def connect_to_server(self, ip, username, password=None, **kwargs):
                self.recorded_kwargs = (ip, username, password, kwargs)

        created_instances = []
        original_init = KeyRecordingEngine.__init__

        def tracked_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            created_instances.append(self)

        KeyRecordingEngine.__init__ = tracked_init

        connect_ssh(
            '10.1.1.1', 'admin',
            key_filename='/path/to/key.pem',
            passphrase='secret',
            engine=KeyRecordingEngine
        )

        self.assertEqual(len(created_instances), 1)
        ip, user, pw, kwargs = created_instances[0].recorded_kwargs
        self.assertEqual(ip, '10.1.1.1')
        self.assertEqual(user, 'admin')
        self.assertIsNone(pw)
        self.assertEqual(kwargs['key_filename'], '/path/to/key.pem')
        self.assertEqual(kwargs['passphrase'], 'secret')
        self.assertFalse(kwargs['look_for_keys'])
        self.assertFalse(kwargs['allow_agent'])

    @patch('CiscoAutomationFramework.detect_firmware')
    def test_connect_ssh_passes_explicit_look_for_keys(self, mock_detect_firmware):
        mock_firmware_class = MagicMock()
        mock_detect_firmware.return_value = mock_firmware_class

        class FlagRecordingEngine(SSHEngine):
            def __init__(self):
                self.enable_password = None
                self.timeout = 10
                self.recorded_kwargs = None

            def connect_to_server(self, ip, username, password=None, **kwargs):
                self.recorded_kwargs = kwargs

        created_instances = []
        original_init = FlagRecordingEngine.__init__

        def tracked_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            created_instances.append(self)

        FlagRecordingEngine.__init__ = tracked_init

        connect_ssh(
            '10.1.1.1', 'admin', 'pw',
            look_for_keys=True,
            allow_agent=True,
            engine=FlagRecordingEngine
        )

        self.assertEqual(len(created_instances), 1)
        kwargs = created_instances[0].recorded_kwargs
        self.assertTrue(kwargs['look_for_keys'])
        self.assertTrue(kwargs['allow_agent'])
