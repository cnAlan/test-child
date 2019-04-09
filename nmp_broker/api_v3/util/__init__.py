# coding=utf-8
from flask import jsonify

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import data_store


@api_v3_app.route('/util/ticket/new')
def get_tickets():
    ticket = data_store.get_new_64bit_ticket()
    if ticket is None:
        result = {
            'error': 'error',
            'message': "can't get a new 64bit ticket"
        }
    else:
        result ={
            'ticket': ticket
        }
    return jsonify(result)
