from transaction import Transaction
from decimal import Decimal

import operations.SMSReserveSum
import operations.CustomerPayment
import operations.CustomerAccountBalance


operDict = {
    'SMSReserveSum': operations.SMSReserveSum,
    'CustomerPayment': operations.CustomerPayment,
    'CustomerAccountBalance': operations.CustomerAccountBalance
}

def do(name, **params):
    currOperation = operDict[name]
    if currOperation is None:
        return

    params['type'] = name

    with Transaction() as tr:
        return currOperation.do(tr, params)
