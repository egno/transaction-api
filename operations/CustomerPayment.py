from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Пополнен баланс ЛС'
    tr.postTransaction()

    amount = float(params['amount'])
    payCommission = float(params.get('payCommission', 0))
    unoCommission = float(params.get('unoCommission', 0))

    tr.postEntry(account='paymentSystemDebt',
                 amount=amount,
                 analytics={'provider': params.get('provider')},
                 data={'description': 'Сформирована задолженность ПС'})

    tr.postEntry(account='paymentSystemComission',
                 amount=payCommission,
                 analytics={'provider': params.get('provider')},
                 data={'description': 'Учтена комиссия платежной системы'})

    tr.postEntry(account='income',
                 amount=unoCommission,
                 analytics={
                     'business': params['business'], 'provider': params.get('provider')},
                 data={'description': 'Получена выручка от предоставления возможности онлайн платежей'})

    tr.postEntry(account='business',
                 amount=amount,
                 analytics={'business': params['business']},
                 data={'description': 'Пополнен баланс'})

    tr.postEntry(account='business',
                 amount=-unoCommission,
                 analytics={'business': params['business']},
                 data={'description': 'Списана комиссия за предоставление возможности онлайн платежей'})

    res = tr.save()
    return(res)
