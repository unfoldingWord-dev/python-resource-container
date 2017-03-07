import factory
from unittest import TestCase
import os
import shutil

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

class TestResourceContainer(TestCase):

    def setUpClass(cls=None):
        directory = os.path.join(DATA_DIR, 'new-rc')
        if os.path.exists(directory):
            shutil.rmtree(directory)

    def test_open_project(self):
        dir = os.path.join(DATA_DIR, 'existing-rc', 'en-obs')
        rc = factory.load(dir)
        project = rc.project()
        assert project['identifier'] == 'obs'
        assert rc.conforms_to == '0.2'
        assert type(rc.chapters()) == list
        assert rc.language['identifier'] == 'en'
        assert rc.chunks('01') == ['01.md']
        assert rc.read_chunk('01', '01').split('\n', 1)[0] == '# 1. The Creation'
        assert rc.type == 'book'
        assert rc.config['content']['10']['10']['dict'][0] == '/en/tw/bible/god'
        assert rc.toc is None

    def test_write_and_remove_chunk(self):
        dir = os.path.join(DATA_DIR, 'existing-rc', 'en-obs')
        rc = factory.load(dir)
        my_chunk = 'this is a test'
        rc.write_chunk('test', 'test', my_chunk)
        assert rc.read_chunk('test', 'test') == my_chunk
        rc.delete_chunk('test', 'test')
        assert rc.read_chunk('test', 'test') is None

    def test_create_resource_container(self):
        dir = os.path.join(DATA_DIR, 'new-rc', 'en-obs')
        container = factory.create(dir, {
            'dublin_core': {
                'type': 'book',
                'format': 'text/markdown',
                'identifier': 'obs',
                'language': {
                    'direction': 'ltr',
                    'identifier': 'en',
                    'title': 'English'
                },
                'rights': 'CC BY-SA 4.0'
            }
        })
        assert container.conforms_to == '0.2'
