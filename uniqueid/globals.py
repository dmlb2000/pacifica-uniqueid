#!/usr/bin/python
"""Global module for static variables."""
from os import getenv


CHERRYPY_CONFIG = getenv('CHERRYPY_CONFIG', 'server.conf')
