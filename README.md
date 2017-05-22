Master: [![Build Status](https://travis-ci.org/unfoldingWord-dev/python-resource-container.svg?branch=master)](https://travis-ci.org/unfoldingWord-dev/python-resource-container)

# python-resource-container
A utility for managing Door43 Resource Containers. This follows the specification at http://resource-container.readthedocs.io/en/v0.2/.

## What is an RC?
A Resource Container (RC) is a modular/portable package of translation data.

## Installation
```
pip install resource_container
```

## Requirements

python 2.7+

## Usage
To get started you must first load an RC. Then you can read/write as needed.

```python
from resource_container import factory


rc = factory.load('/path/to/resource/container/dir')

# some attributes have dedicated properties
print(rc.type)

# other attributes are accessible from the manifest
print(rc.manifest['dublin_core']['rights'])

# read
chapter = rc.read_chunk('01', 'title')

# write
rc.write_chunk('front', 'title', 'Some book title')
```

### Multiple Projects
It is possible for an RC to contain multiple projects.
In such cases methods like writing and reading chunks will
throw an error telling you to specify the project.

```python
# assume rc contains the projects: gen, exo.

# this throws an error
rc.read_chunk('01', 'title')

# you can check how many projects are in an rc
rc.project_count

# this works as expected
chapter01title = rc.read_chunk('gen', '01', 'title')
```

### Strict Mode

By default the tool will operate in strict mode when loading an RC. 
This will perform some checks to ensure the RC is valid.
If you need to look at an RC regardless of it's validity
you can disable strict mode by passing in `False`.

```python
rc = factory.load('/invalid/rc/dir', False)
# do stuff with the invalid rc
```


### Creating an RC

This tool also allows you to create a brand new RC.

> NOTE: currently you must specify the complete manifest manually.
> This might change a little in the future.

```python
manifest = {
    ...
}

rc = factory.create('/my/rc/dir/', manifest)
# do stuff with your new rc
```
