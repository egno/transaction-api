import psycopg2
from psycopg2.extras import DictCursor
import json
from config import CONFIG as config

DB_CONFIG = config['DB']


class DBTransaction(object):

    def __init__(self):
        self.conn = None
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if not self.conn is None:
            self.conn.close()

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(host=DB_CONFIG['PGHOST'], dbname=DB_CONFIG['PGDATABASE'],
                                         user=DB_CONFIG['PGUSER'], password=DB_CONFIG['PGPASSWORD'])

    def get(self, sql, params=(None,), all=False):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql, params)
            if all:
                return cursor.fetchall()
            else:
                return cursor.fetchone()
