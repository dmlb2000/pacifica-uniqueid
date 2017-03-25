#!/usr/bin/python
"""Create the unique index database schema."""
from uniqueid.orm import UniqueIndex, try_db_connect


def create_tables():
    """Create the UniqueIndex database table."""
    try_db_connect()
    if not UniqueIndex.table_exists():
        UniqueIndex.create_table()
    UniqueIndex.database_close()


if __name__ == '__main__':
    create_tables()
