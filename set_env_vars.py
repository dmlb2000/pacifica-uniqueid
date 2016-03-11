"""
Set up environment variables for test

"""

import os

os.environ['MYSQL_PORT_3306_TCP_PORT'] = '3306'

print os.getenv('MYSQL_PORT_3306_TCP_PORT')

