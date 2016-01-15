#!/usr/bin/env python

from wsgiref.simple_server import make_server
import json
from cgi import parse_qs, escape
import MySQLdb

import os
import peewee

db = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE'), 
			host=os.getenv('MYSQL_PORT_3306_TCP_ADDR'), 
			port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT')), 
			user=os.getenv('MYSQL_ENV_MYSQL_USER'), 
			passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

class Index(peewee.Model):
    """
    ORM model of the Artist table
    """
    index = peewee.IntegerField()
 
    class Meta:
        db = db

def application(environ, start_response):

#"""
    print "ping"

    o = parse_qs(environ['QUERY_STRING'])
    if (o):
        try:
            range = long(o.get('range', [''])[0])
            print "range"
            print range
	    
	    print "connecting"
	    db.connect()

	    print "connected"

            record = Index.select().get()
	    print "record"
	    print record

	    index = record.index
	    print "index"
	    print index

        except Exception, e:
	    print "error on transaction"
            print e.message
            db.close()
            return
        finally:
            db.close()
    else:
        
        index = -99
        range = 1


    dict = {'startIndex' : index,'endIndex' : index+range-1}
    response_body = json.dumps(dict)

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
    print os.getenv('MYSQL_ENV_MYSQL_USER'), 
    print os.getenv('MYSQL_ENV_MYSQL_PASSWORD')

    Index.create_table()

    # insert initial index
    initial_record = Index.create(index=9)
    initial_record.save()
    

except peewee.OperationalError:
    print "Error creating Index table"

httpd = make_server('0.0.0.0', 8051, application)
httpd.serve_forever()
