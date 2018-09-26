# coding=utf-8

import datetime
import gzip

from flask import request, jsonify, json, current_app

from nmp_broker.api_v2 import api_v2_app

from nmp_broker.common.workflow.status_message_handler import handle_status_message
from nmp_broker.common.workflow.node_check_message_handler import handle_node_check_message

REQUEST_POST_TIME_OUT = 20


@api_v2_app.route('/hpc/workflow/status', methods=['POST'])
def receive_workflow_status_message():
    """
    received workflow status message, using status message handler which saves
    message to local cache and send message to remote server.

    POST data: May be gzipped (according to content-encoding). Contents:
        message (string): JSON string.
            structure:
                {
                    data: status collector's data
                    [error]: exists when there is an error
                }
    :return: jsonify result
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

    message_data = message['data']
    handle_status_message(message_data)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)


@api_v2_app.route('/hpc/workflow/<owner>/<repo>/node-check', methods=['POST'])
def receive_workflow_node_check_message(owner, repo):
    """

    :param owner:
    :param repo:
    :return:

    post data:
    message:
    {
        'app': 'nwpc_monitor_task_scheduler',
        'type': 'sms_node_task',
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'data': {
            'owner': args['owner'],
            'repo': args['repo'],
            'request': {
                'task': args['task'],
            },
            'response': {
                'nodes': [
                    {
                        'node_path': node path,
                        'check_list_result': [
                            {
                                "is_condition_fit": false,
                                "type": "variable",
                                "name": "SMSDATE",
                                "value": {
                                    "expected_value": "20170522",
                                    "value": "20170401"
                                }
                            }

                        ]
                    },
                    ...
                ]
            }
        }
    }
    """
    content_encoding = request.headers.get('content-encoding', '').lower()
    if content_encoding == 'gzip':
        gzipped_data = request.data
        data_string = gzip.decompress(gzipped_data)
        body = json.loads(data_string.decode('utf-8'))
    else:
        body = request.form

    message = json.loads(body['message'])
    message_data = message['data']
    handle_node_check_message(owner, repo, message_data)

    response_result = {
        'status': 'ok'
    }
    return jsonify(response_result)
