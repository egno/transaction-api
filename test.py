from transaction import Transaction
import json

with Transaction() as tr:

    print(tr.transaction({'data': 'test'}))
