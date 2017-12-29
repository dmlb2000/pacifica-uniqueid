#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UniqueID Server.

The Call: curl 'http://localhost:8000/getid?range=10&mode=file'

The Response: {"endIndex": 9, "startIndex": 0}

Select a different mode to get different unique IDs.

curl 'http://localhost:8000/getid?range=10&mode=file'
curl 'http://localhost:8000/getid?range=10&mode=upload'

The Response:

{"endIndex": 9, "startIndex": 0}
{"endIndex": 9, "startIndex": 0}
"""
import cherrypy
from uniqueid.__main__ import main, error_page_default
from uniqueid.rest import Root
from uniqueid.globals import CHERRYPY_CONFIG


cherrypy.config.update({'error_page.default': error_page_default})
# pylint doesn't realize that application is actually a callable
# pylint: disable=invalid-name
application = cherrypy.Application(Root(), '/', CHERRYPY_CONFIG)
# pylint: enable=invalid-name
if __name__ == '__main__':  # pragma no branch
    main()
