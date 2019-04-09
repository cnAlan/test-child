# coding: utf-8
import datetime
import gzip

from flask import request, json, jsonify, current_app

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common.workload.jobs_message_handler import handle_jobs_message


REQUEST_POST_TIME_OUT = 20


@api_v3_app.route('/workload/repos/<owner>/<repo>/jobs', methods=['POST'])
def receive_workload_jobs(owner, repo):
    """

    :param owner:
    :param repo:
    :return:

    POST
        message: json string of loadleveler collection result
            {
                app: nwpc_hpc_collector.loadleveler_status,
                type: 'command',
                time: "%Y-%m-%d %H:%M:%S",
                data: {
                    workload_system: loadleveler,
                    user_name: user name,
                    collected_time: "%Y-%m-%d %H:%M:%S",
                    type: 'JobListContent',
                    request: {
                        command: 'loadleveler_status',
                        sub_command: 'collect',
                        arguments: []
                    },
                    response: model_dict
                        {
                            items: array
                            [
                                {
                                    props: array
                                }
                            ]
                        }
                }
            }
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
    handle_jobs_message(owner, repo, message)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    current_app.logger.info("{owner}/{repo}/jobs used {time_cost}".format(
        owner=owner, repo=repo, time_cost=end_time - start_time))

    return jsonify(result)
