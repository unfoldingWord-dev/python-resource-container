import os
import yaml


class Rc:
    def __init__(self, directory):
        """
        :param string directory:
        """
        self.dir = directory
        self.manifest = yaml.load(open(os.path.join(directory, 'manifest.yaml')))

        dublin_core = self.manifest['dublin_core']

        self.language = dublin_core['language']
        self.resource = dublin_core
        self.conformsTo = dublin_core['conformsto'].replace('rc', '') if type(dublin_core['conformsto']) is str else None

        if type(self.dir) is not str:
            raise Exception('Missing string parameter: dir')

    def project(self, identifier=None):
        """
        Retrieves a project from the RC.

        You can exclude the parameter if the RC only has one project.

        :param identifier:
        :return:
        """
        if identifier:
            for p in self.manifest['projects']:
                if p['identifier'] == identifier:
                    return p
        else:
            if len(self.manifest['projects']) == 1:
                return self.manifest['projects'][0]
            elif len(self.manifest['projects']) > 1:
                raise Exception('Multiple projects found. Specify the project identifier.')

    def project_count(self):
        return len(self.manifest['projects'])

    def chapters(self, identifier=None):
        """
        Returns an array of chapters in this resource container.

        You can exclude the parameter if this RC only has one project.

        :param identifier: The project identifier
        :return array:
        """
        p = self.project(identifier)
        if p is None:
            return []
        else:
            directory = os.path.join(self.dir, p['path'])
            for root, dirs, files in os.walk(directory):
                return dirs
