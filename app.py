from requests import post, get
from flask import Flask, request, make_response
from flask_cors import CORS
import re
import json
from config import CONFIG as config
import logging
import operation
import query
from datetime import date, datetime
from decimal import Decimal

app = Flask(__name__)
CORS(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (Decimal)):
        return float(obj)
    raise TypeError("Type %s not serializable" % type(obj))


@app.route('/transaction', methods=['POST'])
def post_transaction():
    print(f'IN: {request.get_json()}')
    app.logger.info(f'IN: {request.get_json()}')

    data = request.get_json()

    if data is None:
        raise ValueError("Transaction was not created")

    transaction, entries = operation.do(**data)

    app.logger.info(f'Transaction: {transaction}, Entries: {entries}')

    if transaction is None or transaction.get('id', '') == '':
        return make_response(json.dumps({'error': "Transaction was not created", 'details': transaction}), 400, {'Content-Type': 'application/json'})

    return make_response(json.dumps({'transaction': transaction, 'entries': entries}, default=json_serial), 200, {'Content-Type': 'application/json'})


@app.route('/transaction/<transaction_id>', methods=['DELETE'])
def undo_transaction(transaction_id):

    data = {'type': 'UndoTransaction', 'transactionId': transaction_id}

    transaction, entries = operation.do(**data)

    app.logger.info(f'Transaction: {transaction}, Entries: {entries}')

    if transaction is None or transaction.get('id', '') == '':
        return make_response(json.dumps({'error': "Transaction was not created", 'details': transaction}), 400, {'Content-Type': 'application/json'})

    return make_response(json.dumps({'transaction': transaction, 'entries': entries}, default=json_serial), 200, {'Content-Type': 'application/json'})

@app.route('/clear', methods=['POST'])
def clear_transactions():

    data = {'type': 'clearWaitingTransactions'}

    res = operation.do(**data)

    print(res)

    app.logger.info(f'Result: {res}')

    return make_response(json.dumps(res, default=json_serial), 200, {'Content-Type': 'application/json'})



@app.route('/account/<business_id>', methods=['GET'])
def balance(business_id):
    res = query.do(type='CustomerAccountBalance', business=business_id)
    try:
        return make_response(json.dumps(res, default=json_serial), 200, {'Content-Type': 'application/json'})
    except Exception as e:
        return make_response(json.dumps({'error': "{0}".format(e)}), 400, {'Content-Type': 'application/json'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
