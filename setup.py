#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pypsh
from setuptools import setup


with open('README.rst', 'r') as f:
    readme = f.read()


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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Networking',
    ],
)
