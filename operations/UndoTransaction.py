from decimal import Decimal


def do(tr, params):
    tr.data = params
    tr.data['description'] = 'Сторно транзакции'

    transactionId = params.get('transactionId')
    if transactionId is None:
        # транзакция не указана. Ошибка
        tr.cancel()
        res = {'message': 'Не указана транзакция'}
        return(res)
    else:
        # указан ID транзакции
        parentTransaction = tr.getTransaction(transactionId)
        if parentTransaction is None or parentTransaction.get('id') is None:
            tr.cancel()
            res = {'message': 'Транзакция не найдена'}
            return(res)
        else:
            tr.parent = parentTransaction.get('id')
            tr.postTransaction()
            parentTransactionEntries = tr.getTransactionEntries()

            for entry in parentTransactionEntries:
                # сторнировать
                print(entry['amount'])
                tr.postEntry(account=entry['account'],
                             amount=-entry['amount'],
                             analytics=entry['analytics'],
                             data={
                                 'description': 'Сторно', 'entry': entry['id'], 'transaction': tr.parent}
                             )

    res = tr.save()
    return(res)
