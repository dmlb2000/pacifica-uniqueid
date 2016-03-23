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

import os
import logging

from index_server_orm import UniqueIndex, DB
from index_server_utils import range_and_mode, valid_request, \
                               create_valid_return, create_invalid_return


@DB.atomic()
def application(environ, start_response):
    """
    The wsgi callback
    """
    # catch and handle bogus requests (ex. faveicon)
    valid = valid_request(environ)
    if not valid:
        status, response_headers, response_body = create_invalid_return()
        start_response(status, response_headers)
        return [response_body]

    # get the index range and index mode from the query string
    id_range, id_mode = range_and_mode(environ)

    # get the new unique end index
    obj = UniqueIndex()
    index, id_range = obj.update_index(id_range, id_mode)

    # create the response with start and end indices
    status, response_headers, response_body = create_valid_return(index, id_range)

    # send it back to the requestor
    start_response(status, response_headers)
    return [response_body]

def main():
    """
        entry point for main index server
    """
    peewee_logger = logging.getLogger('peewee')
    peewee_logger.setLevel(logging.DEBUG)
    peewee_logger.addHandler(logging.StreamHandler())

    main_logger = logging.getLogger('index_server')
    main_logger.setLevel(logging.DEBUG)
    main_logger.addHandler(logging.StreamHandler())

    main_logger.info("MYSQL_ENV_MYSQL_DATABASE = " +  os.getenv('MYSQL_ENV_MYSQL_DATABASE'))
    main_logger.info("MYSQL_PORT_3306_TCP_ADDR = " +  os.getenv('MYSQL_PORT_3306_TCP_ADDR'))
    main_logger.info("MYSQL_PORT_3306_TCP_PORT = " +  os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    main_logger.info("MYSQL_ENV_MYSQL_USER = " +  os.getenv('MYSQL_ENV_MYSQL_USER'))
    main_logger.info("MYSQL_ENV_MYSQL_PASSWORD = " +  os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

    if not UniqueIndex.table_exists():
        UniqueIndex.create_table()

    httpd = make_server('0.0.0.0', 8051, application)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
