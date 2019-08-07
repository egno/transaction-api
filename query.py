from transaction import Transaction
from decimal import Decimal

import operations.AccountOperations
import operations.CustomerAccountBalance
import operations.WaitingTransactions


operDict = {
    'AccountOperations': operations.AccountOperations,
    'CustomerAccountBalance': operations.CustomerAccountBalance,
    'WaitingTransactions': operations.WaitingTransactions
}

def do(**params):
    operationType = params['type']
    if operationType is None:
        return

    currOperation = operDict[operationType]
    if currOperation is None:
        return

    with Transaction() as tr:
        return currOperation.do(tr, params)
