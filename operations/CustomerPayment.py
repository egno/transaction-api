from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Пополнен баланс ЛС'
    tr.postTransaction()
    tr.postEntry(account='business', amount=params['amount'],
                 analytics={'business': params['business']},
                 data={'description': 'Пополнен баланс'})

    res = tr.save()
    return(res)
