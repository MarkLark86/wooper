#!/usr/bin/env python

from setuptools import setup, find_packages

LONG_DESCRIPTION = open('README.md').read()

setup(
    name='wooper',
    version="0.0.1",
    description="FrisbyJS-inspired REST API testing helpers and steps \
for 'behave' behavior-driven development testing library",
    long_description=LONG_DESCRIPTION,
    author='Evžen Kiřilov',
    author_email='actionless.loveless@gmail.com',
    url='http://github.com/actionless/wooper',
    license=open('LICENSE').read(),
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.3.0',
        'behave'
    ],
    dependency_links=[
        # "git+git://github.com/actionless/behave@master#egg=behave-123",
        "git+git://github.com/actionless/behave@master#egg=behave",
    ],
    classifiers=[
        # @TODO: change status
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        # @TODO: add testers
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        # @TODO: add version
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
