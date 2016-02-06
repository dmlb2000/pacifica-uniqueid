#!/usr/bin/env python
"""
UniqueID Server

"""
# disable this for classes Index and Meta (within Index)
# pylint: disable=too-few-public-methods
# pylint: disable=broad-except
from wsgiref.simple_server import make_server
import json
from urlparse import parse_qs

import os
import peewee

DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT')),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

class UniqueIndex(peewee.Model):
    """
    ORM model of the index table
    """
    unique_index = peewee.IntegerField(default=-1)

    class Meta(object):
        """
        Internal meta class for the model
        """
        database = DB

@DB.atomic()
def application(environ, start_response):
    """
    The main application
    """
    args = parse_qs(environ['QUERY_STRING'])
    if args:
        id_range = long(args.get('range', [''])[0])
        id_space = long(args.get('id', [''])[0])
        record = UniqueIndex.get_or_create(id=id_space,
                                           defaults={'unique_index':0})[0]
        index = record.unique_index
        record.unique_index = index + id_range
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
