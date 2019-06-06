from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Возврат суммы за недоставленную SMS'

    reservedId = params.get('reserveId')
    if reservedId is None:
        # резервирование не указано. Ошибка
        tr.cancel()
        res = {'message': 'Не указана транзакция по резервированию средств'}
        return(res)
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
                                 'description': 'Возвращена ранее зарезервированная сумма', 'entry': entry['id'], 'transaction': tr.parent}
                             )

    res = tr.save()
    return(res)
