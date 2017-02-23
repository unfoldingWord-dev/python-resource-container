from .ResourceContainer import Rc
import os
import yaml
current_version = '0.2'


def load(path, strict=True):
    rc = Rc(path)

    if strict is False:
        return rc
    else:
        if rc.manifest is None or rc.conforms_to is None:
            raise Exception('Not a resource container')

        if rc.conforms_to != current_version:
            raise Exception('Unsupported resource container version. Found ' + rc.conformsTo + ' but expected ' + current_version)

        return rc


def create(path, manifest):
    if os.path.isdir(path):
        raise Exception('Resource container already exists')

    defaults = {
        'dublin_core': {
            'type': '',
            'conformsto': 'rc' + current_version,
            'format': '',
            'identifier': '',
            'title': '',
            'subject': '',
            'description': '',
            'language': {
                'identifier': '',
                'title': '',
                'direction': ''
            },
            'source': [],
            'rights': '',
            'creator': '',
            'contributor': [],
            'relation': [],
            'publisher': '',
            'issued': '',
            'modified': '',
            'version': ''
        },
        'checking': {
            'checking_entity': [],
            'checking_level': ''
        },
        'projects': []
    }

    if 'type' not in manifest['dublin_core']:
        raise Exception('Missing required key: dublin_core.type')

    if 'format' not in manifest['dublin_core']:
        raise Exception('Missing required key: dublin_core.format')

    if 'identifier' not in manifest['dublin_core']:
        raise Exception('Missing required key: dublin_core.identifier')

    if 'language' not in manifest['dublin_core']:
        raise Exception('Missing required key: dublin_core.language')

    if 'rights' not in manifest['dublin_core']:
        raise Exception('Missing required key: dublin_core.rights')

    if 'checking' not in manifest:
        manifest['checking'] = {}

    if 'projects' not in manifest:
        manifest['projects'] = []

    opts = {
        'dublin_core': {**defaults['dublin_core'], **manifest['dublin_core']},
        'checking': {**defaults['checking'], **manifest['checking']},
        'projects': defaults['projects'] + manifest['projects']
    }

    if not os.path.isdir(path):
        os.makedirs(path)

    manifest_file = open(os.path.join(path, 'manifest.yaml'), 'w')
    manifest_file.write(yaml.dump(opts, default_flow_style=False))
    manifest_file.flush()
    os.fsync(manifest_file)

    rc = load(path)
    return rc


@property
def conforms_to():
    return current_version
