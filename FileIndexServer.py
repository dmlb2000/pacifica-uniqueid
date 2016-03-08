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
import logging

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print os.getenv('PATH')
print os.getenv('MYSQL_ENV_MYSQL_DATABASE')
print os.getenv('MYSQL_PORT_3306_TCP_ADDR')
print os.getenv('MYSQL_PORT_3306_TCP_PORT')
print os.getenv('MYSQL_ENV_MYSQL_USER')
print os.getenv('MYSQL_ENV_MYSQL_PASSWORD')


DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT')),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

class BaseModel(peewee.Model):
    class Meta:
        database = DB

class UniqueIndex(BaseModel):
    filemode = peewee.BigIntegerField(db_column='fileMode')
    uploadmode = peewee.BigIntegerField(db_column='uploadMode')

    class Meta:
        db_table = 'uniqueindex'

@DB.atomic()
def application(environ, start_response):
    """
    The main application
    """
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
        #record = UniqueIndex.get_or_create(id == 0, defaults={'filemode':0, 'uploadmode':0})

        record = UniqueIndex.get(UniqueIndex.id == 0)

        if id_mode.lower() == 'filemode':
            index = record.filemode
            record.filemode = index + id_range
        if id_mode.lower() == 'uploadmode':
            index = record.uploadmode
            record.uploadmode = index + id_range

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
