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

from index_server_orm import UniqueIndex, DB
from index_server_utils import range_and_mode, check_for_valid_request, create_valid_return, update_index


@DB.atomic()
def application(environ, start_response):
    """
    The wsgi callback
    """
    # catch and handle bogus requests (ex. faveicon)
    status, response_headers, response_body = check_for_valid_request(environ)
    if (status):
        start_response(status, response_headers)
        return [response_body]

    # get the index range and index mode from the query string
    id_range, id_mode = range_and_mode(environ)

    # get the new unique end index
    index, id_range = update_index(id_range, id_mode)

    # create the response with start and end indices
    status, response_headers, response_body = create_valid_return(index, id_range)

    # send it back to the requestor
    start_response(status, response_headers)
    return [response_body]

def main():

    LOGGER = logging.getLogger('peewee')
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())

    INDEX_LOGGER = logging.getLogger('index_server')
    INDEX_LOGGER.setLevel(logging.DEBUG)
    INDEX_LOGGER.addHandler(logging.StreamHandler())

    INDEX_LOGGER.info("MYSQL_ENV_MYSQL_DATABASE = " +  os.getenv('MYSQL_ENV_MYSQL_DATABASE'))
    INDEX_LOGGER.info("MYSQL_PORT_3306_TCP_ADDR = " +  os.getenv('MYSQL_PORT_3306_TCP_ADDR'))
    INDEX_LOGGER.info("MYSQL_PORT_3306_TCP_PORT = " +  os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    INDEX_LOGGER.info("MYSQL_ENV_MYSQL_USER = " +  os.getenv('MYSQL_ENV_MYSQL_USER'))
    INDEX_LOGGER.info("MYSQL_ENV_MYSQL_PASSWORD = " +  os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

    if not UniqueIndex.table_exists():
        UniqueIndex.create_table()

    HTTPD = make_server('0.0.0.0', 8051, application)
    HTTPD.serve_forever()


if __name__ == '__main__':
    main()
