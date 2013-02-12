#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pypsh import __version__
from distutils.core import setup


if os.path.isfile('README.md'):
    readme = open('README.md').read()
else:
    readme = ''


setup(
    name="pypsh",
    version=__version__,
    author="Mathias Fußenegger",
    author_email="pip@zignar.net",
    url="https://github.com/mfussenegger/pypsh",
    license="MIT",
    description="remotely execute commands in parallel with ssh on\
    hostnames that match a regex.",
    long_description=readme,
    platforms=['any'],
    packages=['pypsh'],
    install_requires=[
        'argh',
        'paramiko',
    ],
    entry_points={
        'console_scripts': [
            'pypsh = pypsh:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Networking',
    ],
)
