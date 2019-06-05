from transaction import Transaction
from decimal import Decimal

import operations.SMSReserveSum
import operations.CustomerPayment


operDict = {
    'SMSReserveSum': operations.SMSReserveSum,
    'CustomerPayment': operations.CustomerPayment
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