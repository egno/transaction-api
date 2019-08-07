
def do(tr, params):
    res = tr.accountOperations(account=params.get('account'), date = params.get('date'))
    return(res)
