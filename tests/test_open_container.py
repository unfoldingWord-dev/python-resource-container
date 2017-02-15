from door43rc import Rc
from unittest import TestCase

rc = Rc.Rc('/Users/jeremymlane/Development/NeutrinoGraphics/projects/en-obs')

class TestResourceContainer(TestCase):

    def test_open_resource_container(self):
        """
        This tests opening a resource container
        """
        #testing = Rc.Rc()
        #assert testing == '123'

    def test_open_project(self):
        project = rc.project()
        print(project)

    def test_conforms_to(self):
        assert rc.conformsTo == '0.2'

    def test_getting_chapters(self):
        assert type(rc.chapters()) == list
