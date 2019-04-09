# coding=utf-8
import json
import gzip

from flask import jsonify, request

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common.workflow.node_check_message_handler import handle_node_check_message

REQUEST_POST_TIME_OUT = 20


@api_v3_app.route('/workflow/repos/<owner>/<repo>/node-check', methods=['POST'])
def receive_workflow_node_check_message(owner, repo):
    """

    :param owner:
    :param repo:
    :return:

    POST data:
    message:
    {
        'app': '...',
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
