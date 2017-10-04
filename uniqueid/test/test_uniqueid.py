#!/usr/bin/python
"""Index server unit and integration tests."""
from __future__ import print_function
import unittest
from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from uniqueid.orm import UniqueIndex, update_index


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
            self.assertEqual(index, 1)
            self.assertEqual(index_range, 10)

            index, index_range = update_index(10, 'new')
            self.assertEqual(index, 11)
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
