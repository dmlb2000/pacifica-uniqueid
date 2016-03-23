"""
    index server unit and integration tests
"""
import unittest
from index_server_orm import UniqueIndex, BaseModel

from playhouse.test_utils import test_database
from peewee import SqliteDatabase

# pylint: disable=too-few-public-methods

TEST_DB = SqliteDatabase(':memory:')

class IndexServerUnitTests(unittest.TestCase):
    """
    index server unit and integration tests
    """
    def test_index_update(self):
        """
        test return and update of unique index
        """
        with test_database(TEST_DB, (BaseModel, UniqueIndex)):
            test_object = UniqueIndex.create(idid='file', index=892)
            self.assertEqual(test_object.idid, 'file')


if __name__ == '__main__':
    unittest.main()
