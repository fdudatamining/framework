#!/bin/env python

import os
from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

def read(fname):
    ''' Read files in this directory '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


name = "fdudatamining"
version = "1.0"
release = "1.0.1"
setup(
    name=name,
    version=release,
    author="fdudatamining",
    author_email="ravirao@fdu.edu",
    description="A wrapper for python datamining.",
    long_description=read('README.md'),
    license="GPLv2",
    keywords="datamining",
    url="http://github.com/fdudatamining/framework",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    install_requires=[
        'geopy',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'sqlalchemy',
    ],
    dependency_links=[
        "https://github.com/matplotlib/basemap/archive/v1.1.0.zip#egg=matplotlib-1.1.0"
    ],
    setup_requires=[
        'nose',
        'coverage',
        'sphinx',
    ],
    packages=find_packages(),
    package_data={
        '': ['*.sh'],
    },
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    cmdclass=cmdclass,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc')}},
)
