from requests import post, get
from flask import Flask, request
from flask_cors import CORS
import re
import json
from config import CONFIG as config
import logging
import operation
import query
from datetime import date, datetime

app = Flask(__name__)
CORS(app)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@app.route('/transaction', methods=['POST'])
def post_transaction():
    print(f'IN: {request.get_json()}')
    app.logger.info(f'IN: {request.get_json()}')

    data = request.get_json()

    if data is None:
        raise ValueError("Transaction was not created")

    transaction = operation.do(**data)

    app.logger.info(f'Transaction: {transaction}')

    if transaction['id'] == None:
        raise ValueError("Transaction was not created")

    print(type(transaction))
    return json.dumps({'transaction': transaction}, default=json_serial)


@app.route('/balance/<business_id>', methods=['GET'])
def balance(business_id):
    res = query.do(type='CustomerAccountBalance', business=business_id)
    try:
        return json.dumps({'response': res}, default=json_serial)
    except Exception as e:
        return json.dumps({'error': "{0}".format(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
