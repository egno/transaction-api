from requests import post, get
from flask import Flask, request
from flask_cors import CORS
import re
import json
import db
from config import CONFIG as config
import logging
import operation
import query

app = Flask(__name__)
CORS(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

@app.route('/transaction', methods=['POST'])
def post_transaction():
    print(f'IN: {request.get_json()}')
    app.logger.info(f'IN: {request.get_json()}')

    data = request.get_json()

    if data is None:
        raise ValueError("Transaction was not created")

    transaction_id = operation.do(**data)['id']


    app.logger.info(f'Transaction: {transaction_id}')

    if transaction_id == None:
        raise ValueError("Transaction was not created")

    return json.dumps({'transaction': transaction_id})


@app.route('/balance/<business_id>', methods=['GET'])
def balance(business_id):
    res = query.do(type='CustomerAccountBalance', business=business_id)
    try:
        return json.dumps({'response': res})
    except Exception as e:
        return json.dumps({'error': "{0}".format(e)})


if __name__ == "__main__":

    app.run(host='0.0.0.0')
