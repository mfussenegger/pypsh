#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pypsh
from distutils.core import setup


if os.path.isfile('README.rst'):
    readme = open('README.rst').read()
else:
    readme = ''


setup(
    name="pypsh",
    version=pypsh.__version__,
    author=pypsh.__author__,
    author_email="pip@zignar.net",
    url="https://github.com/mfussenegger/pypsh",
    license=pypsh.__license__,
    description=pypsh.__doc__.strip(),
    long_description=readme,
    platforms=['any'],
    packages=['pypsh'],
    install_requires=[
        'argh',
        'paramiko',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'pypsh = pypsh.main:main',
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
