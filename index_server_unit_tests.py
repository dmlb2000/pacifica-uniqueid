import unittest
import os
from index_server_orm import UniqueIndex, BaseModel

from playhouse.test_utils import test_database
from peewee import SqliteDatabase

TEST_DB = SqliteDatabase(':memory:')

class Test_index_server_unit_tests(unittest.TestCase):

    def test_index_update(self):
        """test things"""
        with test_database(TEST_DB, (BaseModel, UniqueIndex)):
            test_object = UniqueIndex.create(idid= 'file', index=892)
            self.assertEqual(test_object.idid, 'file')


if __name__ == '__main__':
    unittest.main()
