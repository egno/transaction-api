import db
import json
from uuid import uuid4
import psycopg2


class Transaction(db.DBTransaction):

    def __init__(self):
        super().__init__()
        self.id = uuid4()
        self.data = None
        self.entries = []

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def cancel(self):
        super().cancel()

    def save(self):
        res = []
        res.append(
            self.get('''
insert into transaction (id, j)
values (%s, %s)
returning *
''', (str(self.id), json.dumps(self.data),))
        )
        for entry in self.entries:
            res.append(
                self.get('''
insert into entry (transaction, account, amount, analytics)
values (%s, %s, %s, %s)
returning *
''', (str(self.id), entry.account, entry.amount, json.dumps(entry.analytics),))
            )
        return res[0]

    def entry(self, account, amount, analytics):
        entry = Entry(account=account, amount=amount, analytics=analytics)
        self.entries.append(entry)

    def accountBalance(self, account, conditions=[]):
        sql, values = ('''
select sum(amount) balance
from entry
where account = %s
''', (account,))
        for condition in conditions:
            sql += ' and analytics @> (%s)::jsonb '
            values = values + (json.dumps(condition),)

        return self.get(sql, values)['balance'] or 0


class Entry(object):

    def __init__(self, **params):
        self.account = params.get('account')
        self.amount = params.get('amount')
        self.analytics = params.get('analytics')
