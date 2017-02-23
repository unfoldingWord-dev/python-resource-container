import os
import yaml

class Rc:
    def __init__(self, directory):
        """
        :param string directory:
        """
        self.dir = directory

        manifest_dir = os.path.join(directory, 'manifest.yaml')
        if os.access(manifest_dir, os.R_OK):
            self.manifest = yaml.load(open(manifest_dir))
        else:
            self.manifest = None

        config_path = os.path.join(directory, 'content', 'config.yaml')
        if os.access(config_path, os.R_OK):
            self.config = yaml.load(open(config_path))
        else:
            self.config = None

        toc_path = os.path.join(directory, 'content', 'toc.yaml')
        if os.access(toc_path, os.R_OK):
            self.toc = yaml.load(open(toc_path))
        else:
            self.toc = None

        if type(self.dir) is not str:
            raise Exception('Missing string parameter: dir')

    @property
    def path(self):
        return self.dir

    @property
    def type(self):
        return self.manifest['dublin_core']['type']

    @property
    def language(self):
        return self.manifest['dublin_core']['language']

    @property
    def resource(self):
        return self.manifest['dublin_core']

    @property
    def conforms_to(self):
        return self.manifest['dublin_core']['conformsto'].replace('rc', '') if type(self.manifest['dublin_core']['conformsto']) is str else None

    @property
    def chunk_ext(self):
        return {
            'text/usx': 'usx',
            'text/usfm': 'usfm',
            'text/markdown': 'md'
        }.get(self.manifest['dublin_core']['format'], 'txt')

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

    def chunks(self, project_identifier, chapter_identifier=None):
        if chapter_identifier is None:
            chapter_identifier = project_identifier
            project_identifier = 0

        p = self.project(project_identifier)
        if p is None:
            return []

        directory = os.path.join(self.dir, p['path'], chapter_identifier)
        for root, dirs, files in os.walk(directory):
            return files

    def read_chunk(self, project_identifier, chapter_identifier, chunk_identifier=None):
        if chunk_identifier is None:
            chunk_identifier = chapter_identifier
            chapter_identifier = project_identifier
            project_identifier = None

        p = self.project(project_identifier)
        if p is None:
            return []

        file_path = os.path.join(self.dir, p['path'], chapter_identifier, chunk_identifier + '.' + self.chunk_ext)

        if os.access(file_path, os.R_OK):
            contents = open(file_path).read()
        else:
            contents = None
        return contents

    def write_chunk(self, project_identifier, chapter_identifier, chunk_identifier, content=None):
        if content is None:
            content = chunk_identifier
            chunk_identifier = chapter_identifier
            chapter_identifier = project_identifier
            project_identifier = None

        p = self.project(project_identifier)
        if p is None:
            return

        directory_path = os.path.join(self.dir, p['path'], chapter_identifier)
        file_path = os.path.join(directory_path, chunk_identifier + '.' + self.chunk_ext)

        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        file = open(file_path, 'w')
        file.write(content)

    def delete_chunk(self, project_identifier, chapter_identifier, chunk_identifier=None):
        if chunk_identifier is None:
            chunk_identifier = chapter_identifier
            chapter_identifier = project_identifier
            project_identifier = None

        p = self.project(project_identifier)
        if p is None:
            return

        file_path = os.path.join(self.dir, p['path'], chapter_identifier, chunk_identifier + '.' + self.chunk_ext)
        if os.access(file_path, os.R_OK):
            os.remove(file_path)
