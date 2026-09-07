import json
from pathlib import Path
import tempfile
import unittest

from resolve_config import resolve


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def read(self, **kwargs):
        return resolve(self.root, 'example/service', home=self.home, **kwargs)

    def config(self, organization='Test Team'):
        return {'version': 1, 'context': {'organization': organization,
                'repositories': ['example/service']}}

    def test_no_config_is_generic(self):
        self.assertEqual('generic', self.read(environ={})['mode'])

    def test_precedence_selects_one_file(self):
        self.write('home/.config/engineering-flow/config.json', self.config('User'))
        self.assertEqual('User', self.read(environ={})['config']['context']['organization'])
        self.write('engineering-flow.local.json', self.config('Project'))
        self.assertEqual('Project', self.read(environ={})['config']['context']['organization'])
        self.write('env.json', self.config('Env'))
        self.write('chosen.json', self.config('Chosen'))
        env = {'ENGINEERING_FLOW_CONFIG': 'env.json'}
        self.assertEqual('Env', self.read(environ=env)['config']['context']['organization'])
        self.assertEqual('Chosen', self.read(explicit='chosen.json', environ=env)['config']['context']['organization'])

    def test_wrong_repo_does_not_expose_context(self):
        self.write('engineering-flow.local.json', self.config())
        result = resolve(self.root, 'example/other', environ={}, home=self.home)
        self.assertEqual('generic', result['mode'])
        self.assertEqual('', result['config']['context']['organization'])

    def test_explicit_missing_does_not_fallback(self):
        self.write('engineering-flow.local.json', self.config())
        with self.assertRaises(ValueError):
            self.read(explicit='missing.json', environ={})

    def test_invalid_config_fails_closed(self):
        cases = [[], {'version': True}, {'version': 2}, {'version': 1, 'auto_push': True},
                 {'version': 1, 'tools': {'logs': False}},
                 {'version': 1, 'context': {'repositories': '*'}},
                 {'version': 1, 'logs': {'environments': {'qa': {'index': 'x'}}}},
                 {'version': 1, 'verification': [{'patterns': ['*'], 'command': []}]}]
        for data in cases:
            with self.subTest(data=data):
                self.write('bad.json', data)
                with self.assertRaises(ValueError):
                    self.read(explicit='bad.json', environ={})

    def test_malformed_and_duplicate_json(self):
        for content in ('{', '{"version":1,"version":1}'):
            self.root.joinpath('bad.json').write_text(content, encoding='utf-8')
            with self.assertRaises(ValueError):
                self.read(explicit='bad.json', environ={})

    def test_rules_path_defaults_and_command_are_data(self):
        data = self.config()
        data['context']['rules_file'] = 'team.local.md'
        data['tools'] = {'logs': 'example-log-skill'}
        data['verification'] = [{'patterns': ['*.py'], 'command': ['no-such-command', '--check']}]
        self.write('private/config.json', data)
        result = self.read(explicit='private/config.json', environ={})['config']
        self.assertEqual(str(self.root / 'private/team.local.md'), result['context']['rules_file'])
        self.assertEqual('', result['tools']['ci'])
        self.assertEqual('no-such-command', result['verification'][0]['command'][0])

    def test_example_is_valid_and_scoped(self):
        example = Path(__file__).with_name('engineering-flow.example.json')
        self.assertEqual('configured', self.read(explicit=example, environ={})['mode'])


if __name__ == '__main__':
    unittest.main()
