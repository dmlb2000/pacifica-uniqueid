#!/usr/bin/python
"""Setup and install the UniqueID service."""
from setuptools import setup

setup(name='PacificaUniqueID',
      version='1.0',
      description='Pacifica UniqueID',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['uniqueid'],
      scripts=['UniqueIDServer.py', 'DatabaseCreate.py'])
