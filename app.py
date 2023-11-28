"""
    Overriding Default SQL Lite Setup for Chroma.
"""

__import__('pysqlite3')
import os, sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

### SET ROOT ENV VARIABLE
os.environ['env_name'] = 'dev'
#########################
from api import api as application


if __name__ == '__main__':
    application.run(host="0.0.0.0",port=3000)