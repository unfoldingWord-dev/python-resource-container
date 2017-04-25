from setuptools import setup

setup(name='resource_container',
      version='0.1',
      description='A utility for managing Door43 Resource Containers',
      url='https://github.com/unfoldingWord-dev/python-resource-container',
      author='Door43',
      author_email='joel@neutrinographics.com',
      license='MIT',
      packages=['resource_container'],
      install_requires=[
            'yaml',
            'uw_tools'
      ],
      zip_safe=False)
