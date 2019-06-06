from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Пополнен баланс ЛС'
    tr.postTransaction()

    tr.postEntry(account='paymentSystemDebt',
                 amount=params['amount'],
                 analytics={'provider': params.get('provider')},
                 data={'description': 'Сформирована задолженность ПС'})

    tr.postEntry(account='paymentSystemComission',
                 amount=params['payCommission'],
                 analytics={'provider': params.get('provider')},
                 data={'description': 'Учтена комиссия платежной системы'})

    tr.postEntry(account='income',
                 amount=params.get('unoCommission'),
                 analytics={
                     'business': params['business'], 'provider': params.get('provider')},
                 data={'description': 'Получена выручка от предоставления возможности онлайн платежей'})

    tr.postEntry(account='business', amount=params['amount'],
                 analytics={'business': params['business']},
                 data={'description': 'Пополнен баланс'})

    tr.postEntry(account='business',
                 amount=-params.get('unoCommission'),
                 analytics={'business': params['business']},
                 data={'description': 'Списана комиссия за предоставление возможности онлайн платежей'})

    res = tr.save()
    return(res)
