"""
    testable utilities for index server
"""

from urlparse import parse_qs
import json

# pylint: disable=bare-except

def range_and_mode(environ):
    """
    parse the parameters for a request from the environ dictionary
    """
    try:
        args = parse_qs(environ['QUERY_STRING'])

        if args:
            id_range = long(args.get('range', [''])[0])
            id_mode = args.get('mode', [''])[0]
            return (id_range, id_mode)
        return (None, None)

    except:
        return (None, None)

def valid_request(environ):
    """
    catch and handle bogus requests (ex. faveicon)
    """
    info = environ['PATH_INFO']
    return info == '/getid'

def create_invalid_return():
    """
    create an error message
    """
    status = '404 NOT FOUND'

    response_body = ''

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    return (status, response_headers, response_body)

def create_valid_return(index, id_range):
    """
    creates the dictionary containing the start and stop index
    packs the message components
    """
    id_dict = {'startIndex' : index, 'endIndex': index+id_range-1}
    response_body = json.dumps(id_dict)

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    return (status, response_headers, response_body)


