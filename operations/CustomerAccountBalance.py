from decimal import Decimal


def do(tr, params):
    balance = tr.accountBalance('business', [
        {'business': params['business']}])
    tr.cancel()
    params['balance'] = float(balance)
    return(params)
