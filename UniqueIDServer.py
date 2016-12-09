#!/usr/bin/env python
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
from wsgiref.simple_server import make_server

import os
import logging
from time import sleep
import peewee
from uniqueid.orm import UniqueIndex, update_index
from uniqueid.utils import range_and_mode, valid_request, \
                               create_valid_return, create_invalid_return

DATABASE_CONNECT_ATTEMPTS = 15
DATABASE_WAIT = 3


def application(environ, start_response):
    """The wsgi callback."""
    try:
        # catch and handle bogus requests (ex. faveicon)
        valid = valid_request(environ)
        if not valid:
            status, response_headers, response_body = create_invalid_return()
            start_response(status, response_headers)
            return [response_body]

        # get the index range and index mode from the query string
        id_range, id_mode = range_and_mode(environ)

        # get the new unique end index
        if id_range and id_mode:
            UniqueIndex.database_connect()
            index, id_range = update_index(id_range, id_mode)
            UniqueIndex.database_close()
            if index >= 0 and id_range:
                # create the response with start and end indices
                status, response_headers, response_body = create_valid_return(index, id_range)

                # send it back to the requestor
                start_response(status, response_headers)
                return [response_body]

        # something bad
        status, response_headers, response_body = create_invalid_return()
        start_response(status, response_headers)
        return [response_body]
    except peewee.OperationalError as ex:
        peewee_logger = logging.getLogger('peewee')
        peewee_logger.setLevel(logging.DEBUG)
        peewee_logger.addHandler(logging.StreamHandler())
        peewee_logger.warn('OperationalError(%s)', str(ex))


def main():
    """Entry point for main index server."""
    peewee_logger = logging.getLogger('peewee')
    peewee_logger.setLevel(logging.DEBUG)
    peewee_logger.addHandler(logging.StreamHandler())

    main_logger = logging.getLogger('index_server')
    main_logger.setLevel(logging.DEBUG)
    main_logger.addHandler(logging.StreamHandler())

    main_logger.info('MYSQL_ENV_MYSQL_DATABASE = %s', os.getenv('MYSQL_ENV_MYSQL_DATABASE', 'pacifica_uniqueid'))
    main_logger.info('MYSQL_PORT_3306_TCP_ADDR = %s', os.getenv('MYSQL_PORT_3306_TCP_ADDR', '127.0.0.1'))
    main_logger.info('MYSQL_PORT_3306_TCP_PORT = %s', os.getenv('MYSQL_PORT_3306_TCP_PORT', 3306))
    main_logger.info('MYSQL_ENV_MYSQL_USER = %s', os.getenv('MYSQL_ENV_MYSQL_USER', 'uniqueid'))
    main_logger.info('MYSQL_ENV_MYSQL_PASSWORD = %s', os.getenv('MYSQL_ENV_MYSQL_PASSWORD', 'uniqueid'))

    def try_db_connect(attempts=0):
        """Try connecting to the db."""
        try:
            UniqueIndex.database_connect()
        except peewee.OperationalError as ex:
            if attempts < DATABASE_CONNECT_ATTEMPTS:
                sleep(DATABASE_WAIT)
                attempts += 1
                try_db_connect(attempts)
            else:
                raise ex

    try_db_connect()
    if not UniqueIndex.table_exists():
        UniqueIndex.create_table()

    UniqueIndex.database_close()

    httpd = make_server('0.0.0.0', 8051, application)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
