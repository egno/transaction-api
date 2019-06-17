import db
import json
from uuid import uuid4
import psycopg2


class Entry(object):

    def __init__(self, **params):
        self.account = params.get('account')
        self.amount = params.get('amount')
        self.analytics = params.get('analytics')
        self.data = params.get('data')

    def post(self, tr):
        print(tr.id)
        return tr.get('''
insert into entry (transaction, account, amount, analytics, j)
values (%s, %s, %s, %s, %s)
returning *
''', (str(tr.id), self.account, self.amount, json.dumps(self.analytics), json.dumps(self.data)))


class Transaction(db.DBTransaction):

    def __init__(self, **params):
        super().__init__()
        self.id = uuid4()
        self.data = params.get('data')
        self.parent = params.get('parent')
        self.status = params.get('status')
        self.entries = []
        self.transaction = None

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)

    def cancel(self):
        super().close()

    def save(self):
        super().save()
        return {'transaction': self.transaction, 'entries': self.entries}

    def postTransaction(self):
        parent = None
        if not self.parent is None:
            parent = str(self.parent)
        self.transaction = self.get('''
insert into transaction (id, j, parent, status)
values (%s, %s, %s, %s)
returning *
''', (str(self.id), json.dumps(self.data), parent, self.status))

        if not self.transaction is None and not self.transaction['id'] is None:
            self.id = self.transaction['id']
        return self.transaction

    def postEntry(self, account, amount, analytics=None, data=None):
        if amount is None or amount == 0:
            return
        entry = Entry(account=account, amount=amount,
                      analytics=analytics, data=data)
        res = entry.post(self)
        self.entries.append(res)
        return res

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

    def getTransaction(self, id):
        res = self.get('''
select t.* 
from transaction t
left join transaction p on p.parent = t.id
where t.id = %s
and p.id is null
''', (str(id),))
        return res

    def getTransactionEntries(self):
        if self.parent is None:
            return []
        res = self.get('''
select * 
from entry 
where transaction = %s
''', (str(self.parent),), all=True)
        return res

    def clearWaitingTansactions(self, hours = 48):
        sql, values = ('''
SELECT * from public.clear_waiting_transactions(%s);
''', (hours,))
        res = self.get(sql, values, all=True)
        print(res)
        return res

    def getWaitingTansactions(self):
        sql, values = ('''
SELECT * from public.waiting_transactions;
''', (0,))
        res = self.get(sql, values, all=True)
        print(res)
        return res