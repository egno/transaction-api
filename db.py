import psycopg2
from psycopg2.extras import RealDictCursor
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
            try:
                self.conn.commit()
                self.conn.close()
                print('save')
            except psycopg2.InterfaceError:
                pass

    def cancel(self):
        if not self.conn is None:
            try:
                self.conn.rollback()
                self.conn.close()
                print('cancel')
            except psycopg2.InterfaceError:
                pass

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(host=DB_CONFIG['PGHOST'], dbname=DB_CONFIG['PGDATABASE'],
                                         user=DB_CONFIG['PGUSER'], password=DB_CONFIG['PGPASSWORD'])
            # print('open DBTransaction')

    def get(self, sql, params=(None,), all=False):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, params)
            if all:
                return cursor.fetchall()
            else:
                return cursor.fetchone()
