#!/usr/bin/env python

from codecs import open
from os import path
from distutils.core import setup

from setuptools import find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Get the long description from the README file
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    REQUREMENTS = f.read().splitlines()

setup(
    name='wooper',
    version="0.4.3",
    description="FrisbyJS-inspired REST API testing helpers and steps \
for 'behave' behavior-driven development testing library",
    long_description=LONG_DESCRIPTION,
    author='Yauhen Kirylau',
    author_email='actionless.loveless@gmail.com',
    url='http://github.com/actionless/wooper',
    license=open('LICENSE').read(),
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUREMENTS,
    classifiers=[
        # @TODO: change status
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        # @TODO: add testers
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',

        # Pick your license as you wish
        'License :: OSI Approved :: GPL3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
