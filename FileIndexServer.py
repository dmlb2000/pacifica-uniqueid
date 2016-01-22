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

class Index(peewee.Model):
    """
    ORM model of the index table
    """
    index = peewee.IntegerField()

    class Meta(object):
        """
        Internal meta class for the model
        """
        database = DB

def application(environ, start_response):
    """
    The main application
    """
    print "ping"
    args = parse_qs(environ['QUERY_STRING'])
    if args:
        try:
            id_range = long(args.get('range', [''])[0])
            print "range"
            print id_range
            print "connecting"
            DB.connect()

            print "connected"

            record = Index.select().get()
            print "record"
            print record

            index = record.index
            print "index"
            print index

        except Exception, ex:
            print "error on transaction"
            print ex.message
            DB.close()
            return
        finally:
            DB.close()
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
    print "success"
    print response_body
    return [response_body]

try:

    print os.getenv('MYSQL_ENV_MYSQL_DATABASE')
    print os.getenv('MYSQL_PORT_3306_TCP_ADDR')
    print os.getenv('MYSQL_PORT_3306_TCP_PORT')
    print os.getenv('MYSQL_ENV_MYSQL_USER')
    print os.getenv('MYSQL_ENV_MYSQL_PASSWORD')

    Index.create_table()

    # insert initial index
    INITIAL_RECORD = Index.create(index=9)
    INITIAL_RECORD.save()

except peewee.OperationalError:
    print "Error creating Index table"

HTTPD = make_server('0.0.0.0', 8051, application)
HTTPD.serve_forever()
