from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Пополнен баланс ЛС'
    tr.entry('business', params['amount'], {
        'business': params['business']})

    res = tr.save()
    return(res)
