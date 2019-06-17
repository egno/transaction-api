from transaction import Transaction
from decimal import Decimal

import operations.CustomerPayment
import operations.SMSReserveSum
import operations.SMSDelivered
import operations.SMSNotDelivered
import operations.UndoTransaction
import operations.clearWaitingTransactions



operDict = {
    'CustomerPayment': operations.CustomerPayment,
    'SMSReserveSum': operations.SMSReserveSum,
    'SMSDelivered': operations.SMSDelivered,
    'SMSNotDelivered': operations.SMSNotDelivered,
    'UndoTransaction': operations.UndoTransaction,
    'clearWaitingTransactions': operations.clearWaitingTransactions
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
