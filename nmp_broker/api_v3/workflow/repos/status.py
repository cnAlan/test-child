# coding=utf-8
import datetime
import gzip

from flask import request, jsonify, json, current_app

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common.workflow.status_message_handler import handle_status_message


@api_v3_app.route('/workflow/repos/<owner>/<repo>/status', methods=['POST'])
def receive_workflow_status_message(owner, repo):
    """
    receive status of workflow server, and send to status message handler.
    store into local cache and then post it to remote web server.

    POST data

    message: a JSON string. Schema:
    {
        'app': 'sms_status_collector' or 'ecflow_status_collector',
        'timestamp': current_time,
        'data': {
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
            'status': 'error',
            'message': message['error']
        }
        return jsonify(result)

    message_app = message['app']
    if message_app == 'sms_status_collector' or message_app == 'ecflow_status_collector':
        message_data = message['data']
        handle_status_message(owner, repo, message_data, message_app)
    else:
        current_app.logger.error("message app is unknown", message_app)
        result = {
            'status': 'error',
            'message': 'message app is unknown ' + message_app
        }
        return jsonify(result)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    current_app.logger.info("{owner}/{repo}/status used {time_cost}".format(
        owner=owner, repo=repo,
        time_cost=end_time - start_time))

    return jsonify(result)
