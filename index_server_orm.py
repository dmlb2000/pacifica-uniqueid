"""
    ORM for index server
"""
import peewee
import os

# pylint: disable=too-few-public-methods
# peewee, man   ;s;s;s;


DB = peewee.MySQLDatabase(os.getenv('MYSQL_ENV_MYSQL_DATABASE'),
                          host=os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
                          port=int(os.getenv('MYSQL_PORT_3306_TCP_PORT')),
                          user=os.getenv('MYSQL_ENV_MYSQL_USER'),
                          passwd=os.getenv('MYSQL_ENV_MYSQL_PASSWORD'))

class BaseModel(peewee.Model):
    """
    auto-generated by pwiz
    """
    class Meta(object):
        """
        map to the database connected above
        """
        database = DB

class UniqueIndex(BaseModel):
    """
    auto-generated by pwiz
    maps a python record to a mysql table
    """
    idid = peewee.CharField(primary_key=True, db_column='id')
    index = peewee.BigIntegerField(db_column='index')

    class Meta(object):
        """
        map to uniqueindex table
        """
        db_table = 'uniqueindex'

def update_index(id_range, id_mode):
    """
    updates the index for a mode and returns a unique start and stop index
    """
    if id_range and id_mode and id_range > 0:
        record = UniqueIndex.get_or_create(idid=id_mode, defaults={'index':0})[0]

        index = record.index
        record.index = index + id_range
        record.save()
    else:
        index = -99
        id_range = long(1)

    return (index, id_range)

