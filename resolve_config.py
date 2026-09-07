"""Read local engineering context without executing commands or contacting services."""

import argparse
import copy
import json
import os
from pathlib import Path
import sys

WORKFLOWS = (
    'diagnosing-bugs', 'codebase-design', 'research', 'tdd', 'code-review',
    'resolving-merge-conflicts', 'domain-modeling', 'prototype', 'grilling',
    'writing-for-agents',
)
DEFAULTS = {
    'version': 1,
    'context': {'organization': '', 'repositories': [], 'frameworks': [],
                'services': [], 'rules_file': ''},
    'tools': {'tracker': '', 'logs': '', 'ci': '', 'issue_conventions': ''},
    'logs': {'environments': {}},
    'workflows': {key: 'mattpocock-skills:' + key for key in WORKFLOWS},
    'verification': [],
}


def string_list(value, label, nonempty=False):
    if (type(value) is not list or any(type(x) is not str or not x.strip() for x in value)
            or (nonempty and not value)):
        raise ValueError(label + ' must be a list of nonempty strings')


def merge_checked(base, override, label='config'):
    if type(override) is not dict:
        raise ValueError(label + ' must be an object')
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key not in base:
            raise ValueError(label + ' contains an unknown key')
        current = label + '.' + key
        if type(base[key]) is dict:
            if current == 'config.logs.environments':
                if type(value) is not dict:
                    raise ValueError(current + ' must be an object')
                envs = {}
                for name, profile in value.items():
                    if not name.strip() or type(profile) is not dict or set(profile) != {'profile', 'index', 'trace_field'}:
                        raise ValueError(current + ' requires named profile/index/trace_field objects')
                    if any(type(x) is not str or not x.strip() for x in profile.values()):
                        raise ValueError(current + ' fields must be nonempty strings')
                    envs[name] = profile.copy()
                result[key] = envs
            else:
                result[key] = merge_checked(base[key], value, current)
        elif type(base[key]) is list:
            if key == 'verification':
                if type(value) is not list:
                    raise ValueError(current + ' must be a list')
                for rule in value:
                    if type(rule) is not dict or set(rule) != {'patterns', 'command'}:
                        raise ValueError(current + ' rules require patterns and command')
                    string_list(rule['patterns'], current + '.patterns', True)
                    string_list(rule['command'], current + '.command', True)
            else:
                string_list(value, current)
            result[key] = copy.deepcopy(value)
        elif type(value) is not type(base[key]):
            raise ValueError(current + ' has the wrong type')
        else:
            result[key] = value
    return result


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate configuration key')
        result[key] = value
    return result


def resolve(root, repository='', explicit=None, environ=None, home=None):
    environ = os.environ if environ is None else environ
    root = Path(root).resolve()
    home = Path.home() if home is None else Path(home)
    chosen = explicit if explicit is not None else environ.get('ENGINEERING_FLOW_CONFIG')
    if chosen is not None:
        if not str(chosen).strip():
            raise ValueError('explicit configuration path is empty')
        path = Path(chosen).expanduser()
        path = path if path.is_absolute() else root / path
    else:
        path = next((p for p in (root / 'engineering-flow.local.json',
                                home / '.config/engineering-flow/config.json') if p.exists()), None)
    if path is None:
        return {'mode': 'generic', 'config': copy.deepcopy(DEFAULTS)}
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError('configuration cannot be read as UTF-8 JSON') from error
    if type(data) is not dict or type(data.get('version')) is not int or data['version'] != 1:
        raise ValueError('configuration version must be integer 1')
    config = merge_checked(DEFAULTS, data)
    if not repository or repository not in config['context']['repositories']:
        return {'mode': 'generic', 'reason': 'repository-not-in-scope', 'config': copy.deepcopy(DEFAULTS)}
    rules = config['context']['rules_file']
    if rules:
        rules_path = Path(rules).expanduser()
        config['context']['rules_file'] = str((path.parent / rules_path).resolve())
    return {'mode': 'configured', 'config': config}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, help='target repository root')
    parser.add_argument('--repository', default='', help='verified owner/repository; exact match')
    parser.add_argument('--config', help='explicit local JSON file; no implicit fallback on error')
    args = parser.parse_args()
    try:
        result = resolve(args.root, args.repository, args.config)
    except ValueError as error:
        print('Configuration error: ' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
