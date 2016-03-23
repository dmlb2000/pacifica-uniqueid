from urlparse import parse_qs
from index_server_orm import UniqueIndex, DB
import json

def range_and_mode(environ):
    try:
        args = parse_qs(environ['QUERY_STRING'])

        if args:
            id_range = long(args.get('range', [''])[0])
            id_mode = args.get('mode', [''])[0]
            return (id_range, id_mode)

        return (None, None)

    except KeyError:
        return (None, None)

def check_for_valid_request(environ):
    # catch and handle bogus requests (ex. faveicon)
    info = environ['PATH_INFO']
    if info != '/getid':
        status = '404 NOT FOUND'

        response_body = ''

        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]

        return (status, response_headers, response_body)

    return (None, None, None)

def create_valid_return(index, range):
    id_dict = {'startIndex' : index, 'endIndex': index+range-1}
    response_body = json.dumps(id_dict)

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    return (status, response_headers, response_body)

def update_index(id_range, id_mode):

    if id_range and id_mode:
        record = UniqueIndex.get_or_create(idid=id_mode, defaults={'index':0})[0]

        index = record.index
        record.index = index + id_range
        record.save()
    else:
        index = -99
        id_range = long(1)

    return (index, id_range)
