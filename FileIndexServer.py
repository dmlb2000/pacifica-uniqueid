#!/usr/bin/env python
"""
UniqueID Server

The Call: curl 'http://localhost:8000/getid?range=10&mode=file'

The Response: {"endIndex": 9, "startIndex": 0}

Select a different mode to get different unique IDs.

curl 'http://localhost:8000/getid?range=10&mode=file'
curl 'http://localhost:8000/getid?range=10&mode=upload'

The Response:

{"endIndex": 9, "startIndex": 0}
{"endIndex": 9, "startIndex": 0}
"""
# disable this for classes Index and Meta (within Index)
# pylint: disable=too-few-public-methods

from wsgiref.simple_server import make_server
import json
from urlparse import parse_qs

import os
import logging
import peewee

from peewee_index import UniqueIndex

LOGGER = logging.getLogger('peewee')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler())

INDEX_LOGGER = logging.getLogger('index_server')
INDEX_LOGGER.setLevel(logging.DEBUG)
INDEX_LOGGER.addHandler(logging.StreamHandler())

INDEX_LOGGER.info("PATH = " + os.getenv('PATH') )
INDEX_LOGGER.info("DATABASE = " +  os.getenv('MYSQL_ENV_MYSQL_DATABASE'))
INDEX_LOGGER.info("PATH = " +  os.getenv('MYSQL_PORT_3306_TCP_ADDR'))
INDEX_LOGGER.info("PATH = " +  os.getenv('MYSQL_PORT_3306_TCP_PORT'))
INDEX_LOGGER.info("PATH = " +  os.getenv('MYSQL_ENV_MYSQL_USER'))
INDEX_LOGGER.info("PATH = " +  os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))


@DB.atomic()
def application(environ, start_response):
    """
    The wsgi callback
    """
    # catch and handle bogus requests (ex. faveicon)
    info = environ['PATH_INFO']
    if info != '/getid':
        status = '404 NOT FOUND'

        response_body = ''

        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response(status, response_headers)
        return [response_body]

    args = parse_qs(environ['QUERY_STRING'])
    if args:
        id_range = long(args.get('range', [''])[0])
        id_mode = args.get('mode', [''])[0]
        record = UniqueIndex.get_or_create(idid=id_mode, defaults={'index':0})[0]

        index = record.index
        record.index = index + id_range
        record.save()
    else:
        index = -99
        id_range = long(1)


    id_dict = {'startIndex' : index, 'endIndex': index+id_range-1}
    response_body = json.dumps(id_dict)

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

if not UniqueIndex.table_exists():
    UniqueIndex.create_table()

HTTPD = make_server('0.0.0.0', 8051, application)
HTTPD.serve_forever()
