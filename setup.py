#!/usr/bin/env python

import os

from distutils.core import setup
from komapy.version import get_version


def read(filename):
    """Read file contents."""
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='komapy',
    version=get_version(),
    description='Python library for creating customizable BPPTKG Monitoring API chart',
    long_description=read('README.md'),
    license='MIT',
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='https://gitlab.com/bpptkg/komapy',
    zip_safe=True,
    packages=['komapy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
