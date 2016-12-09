#!/usr/bin/python
"""Index server unit and integration tests."""
from __future__ import print_function
import unittest
from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from uniqueid.orm import UniqueIndex, update_index
from uniqueid.utils import range_and_mode, create_invalid_return,\
                               create_valid_return, valid_request


class IndexServerUnitTests(unittest.TestCase):
    """Index server unit and integration tests."""

    def test_index_update(self):
        """Test return and update of unique index."""
        with test_database(SqliteDatabase(':memory:'), [UniqueIndex]):
            test_object = UniqueIndex.create(idid='file', index=892)
            self.assertEqual(test_object.idid, 'file')

            index, index_range = update_index(10, 'file')
            self.assertEqual(index, 892)
            self.assertEqual(index_range, 10)

            index, index_range = update_index(10, 'file')
            self.assertEqual(index, 902)
            self.assertEqual(index_range, 10)

            index, index_range = update_index(10, 'new')
            self.assertEqual(index, 0)
            self.assertEqual(index_range, 10)

            index, index_range = update_index(10, 'new')
            self.assertEqual(index, 10)
            self.assertEqual(index_range, 10)

            index, index_range = update_index(None, 'new')
            self.assertEqual(index, -1)
            self.assertEqual(index_range, -1)

            index, index_range = update_index(2, None)
            self.assertEqual(index, -1)
            self.assertEqual(index_range, -1)

            index, index_range = update_index(-5, 'new')
            self.assertEqual(index, -1)
            self.assertEqual(index_range, -1)

    def test_range_and_mode(self):
        """Test parsing of environ dictionary."""
        environ = {}
        environ['QUERY_STRING'] = 'range=10&mode=file'
        id_range, id_mode = range_and_mode(environ)
        self.assertEqual(id_range, 10)
        self.assertEqual(id_mode, 'file')

        environ['QUERY_STRING'] = 'rage=10&mode=file'
        id_range, id_mode = range_and_mode(environ)
        self.assertEqual(id_range, None)
        self.assertEqual(id_mode, None)

        environ['BEERY_STRING'] = 'range=10&mode=file'
        id_range, id_mode = range_and_mode(environ)
        self.assertEqual(id_range, None)
        self.assertEqual(id_mode, None)

    def test_valid_request(self):
        """Catch and handle bogus requests (ex. faveicon)."""
        environ = {}
        environ['PATH_INFO'] = '/getid'
        val = valid_request(environ)
        self.assertEqual(val, True)

        environ['PATH_INFO'] = '/favicon'
        val = valid_request(environ)
        self.assertEqual(val, False)

    def test_create_invalid_return(self):
        """Catch and handle bogus requests (ex. faveicon)."""
        status, response_headers, response_body = create_invalid_return()

        self.assertEqual(status, '404 NOT FOUND')
        self.assertEqual(response_body, '')

        self.assertEqual(response_headers[0][0], 'Content-Type')
        self.assertEqual(response_headers[0][1], 'application/json')
        self.assertEqual(response_headers[1][0], 'Content-Length')
        self.assertEqual(response_headers[1][1], '0')

    def test_create_valid_return(self):
        """Catch and handle bogus requests (ex. faveicon)."""
        status, response_headers, response_body = create_valid_return(333, 10)

        self.assertEqual(status, '200 OK')
        self.assertEqual(response_body, '{"endIndex": 342, "startIndex": 333}')

        self.assertEqual(response_headers[0][0], 'Content-Type')
        self.assertEqual(response_headers[0][1], 'application/json')
        self.assertEqual(response_headers[1][0], 'Content-Length')
        self.assertEqual(response_headers[1][1], '36')


if __name__ == '__main__':
    unittest.main()
    print('test complete')
