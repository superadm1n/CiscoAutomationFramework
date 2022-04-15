from unittest import TestCase
from tests.test_Transport_Engines.Engines import IdealNoDelayGetOutput, WillTriggerTimeout
from os import listdir
from os.path import isfile, join
from pathlib import Path
from time import perf_counter
import random


class TestGettingOutput(TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.maxDiff = None

    @property
    def files(self):
        base_path = Path(__file__).parents[2]
        output_dir = join(base_path, 'output')
        return [join(output_dir, f) for f in listdir(output_dir) if isfile(join(output_dir, f))]


    def random_files(self, num=10):
        file_choices = self.files
        if num > len(file_choices):
            num = len(file_choices)
        files = []
        while len(files) < num:
            choice = random.choice(file_choices)
            if choice not in files:
                files.append(choice)

        return files

    def test_returns_all_what_was_sent_from_server(self):
        ssh = IdealNoDelayGetOutput()
        for file in self.files:
            with open(file, 'r') as f:
                canned_resp = f.read()
            # load a canned response
            ssh.load_canned_response(canned_resp)

            data = ssh.get_output()
            self.assertEqual(canned_resp.splitlines(), data)

    def test_triggers_timeout(self):
        ssh = WillTriggerTimeout()
        ssh.hostname = 'myhostname'
        start = perf_counter()
        ssh.get_output(timeout=1.2)
        elapsed = perf_counter() - start
        self.assertGreaterEqual(elapsed, 1.2)

    def test_returns_as_list(self):
        ssh = IdealNoDelayGetOutput()
        file = self.random_files(1)[0]
        with open(file, 'r') as f:
            resp = f.read()
        ssh.load_canned_response(resp)
        data = ssh.get_output()
        self.assertTrue(type(data) == list)

    def test_output_starts_with_command(self):
        ssh = IdealNoDelayGetOutput()
        file = self.random_files(1)[0]
        with open(file, 'r') as f:
            resp = f.read()
        ssh.load_canned_response(resp)
        data = ssh.get_output()
        self.assertEqual(data[0], resp.splitlines()[0])

    def test_output_ends_with_prompt(self):
        ssh = IdealNoDelayGetOutput()
        file = self.random_files(1)[0]
        with open(file, 'r') as f:
            resp = f.read()
        ssh.load_canned_response(resp)
        data = ssh.get_output()
        self.assertEqual(data[-1], resp.splitlines()[-1])

    def test_does_not_get_output_by_default_if_no_command_was_sent(self):
        ssh = IdealNoDelayGetOutput()
        # load a command so the engine will return data as long as it runs
        # I need this for proof that it does not return after we rig it
        loaded_response = 'hostname\ntext\nhostname>'
        ssh.load_canned_response(loaded_response)
        # rig engine to believe no command was sent
        ssh.commands_sent_since_last_output_get = 0
        data = ssh.get_output()
        self.assertNotEqual(loaded_response.splitlines(), data)
        self.assertEqual([], data)

    def test_able_to_get_output_if_no_command_sent_with_override(self):
        ssh = IdealNoDelayGetOutput()
        canned_response = 'hostname\ntext\nhostname>'
        ssh.canned_output = canned_response
        data = ssh.get_output(no_command_sent_previous=True)
        self.assertEqual(canned_response.splitlines(), data)


    def test_gets_prompt_when_sending_question(self):
        ssh = IdealNoDelayGetOutput()
        output_from_server = 'command ?\noutput\nhostname> this is a command of sorts '.splitlines()
        ssh._extract_prompt(output_from_server)

        self.assertEqual('hostname>', ssh.prompt)

    def test_gets_prompt_when_issuing_command(self):
        ssh = IdealNoDelayGetOutput()
        output_from_server = 'command ?\noutput\nhostname>'.splitlines()
        ssh._extract_prompt(output_from_server)

        self.assertEqual('hostname>', ssh.prompt)

    def test_gets_prompt_in_config_mode(self):
        ssh = IdealNoDelayGetOutput()
        output_from_server = 'command ?\noutput\nhostname(config)#'.splitlines()
        ssh._extract_prompt(output_from_server)

        self.assertEqual('hostname(config)#', ssh.prompt)

    def test_gets_prompt_in_priv_exec(self):
        ssh = IdealNoDelayGetOutput()
        output_from_server = 'command ?\noutput\nhostname#'.splitlines()
        ssh._extract_prompt(output_from_server)

        self.assertEqual('hostname#', ssh.prompt)

