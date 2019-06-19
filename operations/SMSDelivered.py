from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Списание суммы за доставленную SMS'

    reservedId = params.get('reservedId')
    reservedAmount = 0
    if reservedId is None:
        tr.postTransaction()
    else:
        # указан ID транзакции по резервированию суммы
        parentTransaction = tr.getTransaction(reservedId)
        if parentTransaction is None or parentTransaction.get('id') is None:
            # резервирование не найдено. Ошибка
            tr.cancel()
            res = {'message': 'Не найдена транзакция по резервированию средств'}
            return(res)
        else:
            tr.parent = parentTransaction.get('id')
            reservedAmount = parentTransaction.get('j',{}).get('amount', 0)
            tr.postTransaction()
            parentTransactionEntries = tr.getTransactionEntries()

            for entry in parentTransactionEntries:
                # восстановить зарезервированную сумму
                print(entry['amount'])
                tr.postEntry(account=entry['account'],
                             amount=-entry['amount'],
                             analytics=entry['analytics'],
                             data={
                                 'description': 'Возвращена ранее зарезервированная сумма', 'entry': entry['id'], 'transaction': tr.parent}
                             )

    tr.postEntry(account='business',
                 amount=-reservedAmount,
                 analytics={'business': params['business']},
                 data={'description':'Списана сумма за отправленную SMS'})

    tr.postEntry(account='business',
                 amount=-params.get('unoCommission',0),
                 analytics={'business': params['business']},
                 data={'description': 'Списана комиссия за услуги SMS'})

    tr.postEntry(account='provider',
                 amount=-params['amount'],
                 analytics={'provider': params.get('provider')},
                 data={'description': 'Списана сумма за отправленную SMS'})

    res = tr.save()
    return(res)
