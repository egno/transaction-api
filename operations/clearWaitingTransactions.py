
def do(tr, params):
    res = tr.clearWaitingTansactions()
    tr.save()
    return(res)
