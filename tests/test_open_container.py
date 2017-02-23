from door43rc import Rc
from unittest import TestCase

rc = Rc.load('/Users/jeremymlane/Development/NeutrinoGraphics/projects/en-obs')

class TestResourceContainer(TestCase):

    def test_open_resource_container(self):
        """
        This tests opening a resource container
        """
        #testing = rc.Rc()
        #assert testing == '123'

    def test_open_project(self):
        project = rc.project()
        assert project['identifier'] == 'obs'

    def test_conforms_to(self):
        assert rc.conforms_to == '0.2'

    def test_getting_chapters(self):
        assert type(rc.chapters()) == list

    def test_getting_language(self):
        assert rc.language['identifier'] == 'en'

    def test_getting_chunks(self):
        assert rc.chunks('01') == ['01.md']

    def test_read_chunk(self):
        assert rc.read_chunk('01', '01').split('\n', 1)[0] == '# 1. The Creation'

    def test_get_type(self):
        assert rc.type == 'book'

    def test_access_config(self):
        assert rc.config['content']['10']['10']['dict'][0] == '/en/tw/bible/god'

    def test_access_toc(self):
        assert rc.toc is None

    def test_write_and_remove_chunk(self):
        my_chunk = 'this is a test'
        rc.write_chunk('test', 'test', my_chunk)
        assert rc.read_chunk('test', 'test') == my_chunk
        rc.delete_chunk('test', 'test')
        assert rc.read_chunk('test', 'test') is None

    def test_create_resource_container(self):
        Rc.create('/Users/jeremymlane/Development/NeutrinoGraphics/projects/en-obs-test', {
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
