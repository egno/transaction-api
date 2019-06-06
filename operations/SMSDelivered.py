from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Списание суммы за доставленную SMS'

    reservedId = params.get('reserveId')
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
            tr.postTransaction()
            parentTransactionEntries = tr.getTransactionEntries()

            for entry in parentTransactionEntries:
                # восстановить зарезервированную сумму
                print(entry['amount'])
                tr.postEntry(account=entry['account'],
                             amount=-entry['amount'],
                             analytics=entry['analytics'],
                             data={
                                 'description': 'Возвращена реанее зарезервированная сумма', 'entry': entry['id'], 'transaction': tr.parent}
                             )

    balance = tr.accountBalance('business', [
        {'business': params['business']}
    ])
    if balance - Decimal(params['amount']) < 0:
        tr.cancel()
        res = {'message': 'Недостаточно суммы на ЛС'}
        return(res)

    tr.postEntry(account='business',
                 amount=-params['amount'],
                 analytics={'business': params['business']},
                 data={'description':'Списана сумма за отправленную SMS'})

    res = tr.save()
    return(res)
