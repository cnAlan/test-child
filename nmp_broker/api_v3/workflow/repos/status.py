# coding=utf-8
import datetime
import gzip

from flask import request, jsonify, json

from nmp_broker.api_v3 import api_v3_app

from nmp_broker.common.workflow.sms import sms_status_message_handler
from nmp_broker.common.workflow.ecflow import ecflow_status_message_handler


@api_v3_app.route('/workflow/repos/<owner>/<repo>/status', methods=['POST'])
def receive_workflow_status_message(owner, repo):
    """
    receive status of workflow server, store into local cache and then post it to remote web server.

    POST data

    message: a JSON string. There are some different types of message:
    sms
    {
        'app': 'sms_status_collector',
        'type': 'sms_status',
        'timestamp': current_time,
        'data': {
            'owner': owner,
            'repo': repo,
            'sms_name': sms_name,
            'sms_user': sms_user,
            'time': current_time,
            'status': bunch_dict
        }
    }

    ecflow
    {
        'app': 'ecflow_status_collector',
        'type': 'ecflow_status',
        'timestamp': current_time,
        'data': {
            'owner': owner,
            'repo': repo,
            'server_name': server_name  # should removed
            'time': current_time,
            'status': bunch_dict
        }
    }


    :return:
    """
    start_time = datetime.datetime.utcnow()

    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])

    if 'error' in message:
        result = {
            'status': 'ok'
        }
        return jsonify(result)

    message_app = message['app']
    message_type = message['type']
    if message_app == 'sms_status_collector':
        message_data = message['data']
        sms_status_message_handler(message_data)
    elif message_app == 'ecflow_status_collector':
        message_data = message['data']
        ecflow_status_message_handler(message_data)
    else:
        print("message app is unknown", message_app)
        result = {
            'status': 'error',
            'message': 'message app is unknown ' + message_app
        }
        return jsonify(result)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)
