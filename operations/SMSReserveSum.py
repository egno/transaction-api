from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Резервирование суммы на отправку SMS'
    tr.status='waiting'
    balance = tr.accountBalance('business', [
        {'business': params['business']}])
    if not params.get('business') is None and balance - Decimal(params['amount']) < 0:
        tr.cancel()
        res = {'message': 'Недостаточно суммы на ЛС'}
        return(res)
    tr.postTransaction()
    tr.postEntry(account='business', amount=-params['amount'],
                 analytics={'business': params['business']},
                 data={'description': 'Зарезервирована сумма на отправку SMS'}
                 )

    res = tr.save()
    return(res)
