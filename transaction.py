import db
import json


class Transaction(object):

    def __init__(self):
        self.tr = db.DBTransaction()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.tr is None :
            self.tr.close()

    def transaction(self, data):
        return self.tr.get('''
insert into transaction (j)
values (%s)
returning *
''', (json.dumps(data),))

    def entry(self, transaction_id, account, amount, analytics):
        return self.tr.get('''
insert into entry (transaction, account, amount, analytics)
values (%s)
returning *
''', (transaction_id, account, amount, json.dumps(analytics),))
