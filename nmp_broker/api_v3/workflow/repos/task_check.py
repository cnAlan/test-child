# coding=utf-8
import datetime
import json
import gzip

from flask import jsonify, request, current_app
import requests

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import weixin, data_store

REQUEST_POST_TIME_OUT = 20


@api_v3_app.route('/workflow/repos/<owner>/<repo>/task-check', methods=['POST'])
def receive_sms_node_task_message(owner, repo):
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
    task_name = message_data['request']['task']['name']

    unfit_node_list = []

    node_result = message_data['response']['nodes']
    for a_node_record in node_result:
        node_path = a_node_record['node_path']
        unfit_check_list = []

        for a_check_result in a_node_record['check_list_result']:
            is_condition_fit = a_check_result['is_condition_fit']
            if is_condition_fit is None:
                pass
            elif is_condition_fit:
                pass
            elif not is_condition_fit:
                unfit_check_list.append(a_check_result)

        if len(unfit_check_list):
            unfit_node_list.append({
                'node_path': node_path,
                'unfit_check_list': unfit_check_list
            })

    print(unfit_node_list)
    if len(unfit_node_list) > 0:
        weixin_message = {
            'app': 'nmp_broker',
            'type': 'sms_node_task',
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'data': {
                'owner': owner,
                'repo': repo,
                'task_name': task_name,
                'unfit_nodes': unfit_node_list
            }
        }

        takler_object_system_dict = data_store.save_sms_task_check_to_nwpc_takler_object_system(
            owner, repo,
            message_data, unfit_node_list
        )

        unfit_nodes_blob_id = None
        for a_blob in takler_object_system_dict['blobs']:
            if a_blob['data']['type'] == 'unfit_nodes':
                unfit_nodes_blob_id = a_blob['id']
                weixin_message['data']['unfit_nodes_blob_id'] = unfit_nodes_blob_id
        print(unfit_nodes_blob_id)

        post_message = {
            'app': 'nmp_broker',
            'event': 'post_sms_task_check',
            'timestamp': datetime.datetime.utcnow(),
            'data': {
                'type': 'takler_object',
                'blobs': takler_object_system_dict['blobs'],
                'trees': takler_object_system_dict['trees'],
                'commits': takler_object_system_dict['commits']
            }
        }

        website_post_data = {
            'message': json.dumps(post_message)
        }

        print('gzip the data...')
        gzipped_post_data = gzip.compress(bytes(json.dumps(website_post_data), 'utf-8'))
        print('gzip the data...done')

        website_url = current_app.config['BROKER_CONFIG']['sms']['task_check']['cloud']['put']['url'].format(
            owner=owner,
            repo=repo
        )
        response = requests.post(
            website_url,
            data=gzipped_post_data,
            headers={
                'content-encoding': 'gzip'
            },
            timeout=REQUEST_POST_TIME_OUT
        )
        print(response)

        weixin_app = weixin.WeixinApp(
            weixin_config=current_app.config['BROKER_CONFIG']['weixin_app'],
            cloud_config=current_app.config['BROKER_CONFIG']['cloud']
        )
        weixin_app.send_sms_node_task_warn(weixin_message)
    # else:
    #     # debug message.
    #     weixin_message = {
    #         'app': 'nmp_broker',
    #         'type': 'sms_node_task',
    #         'timestamp': datetime.datetime.utcnow().isoformat(),
    #         'data': {
    #             'owner': owner,
    #             'repo': repo,
    #             'task_name': task_name,
    #         }
    #     }
    #
    #     weixin_app = weixin.WeixinApp(
    #         weixin_config=app.config['BROKER_CONFIG']['weixin_app'],
    #         cloud_config=app.config['BROKER_CONFIG']['cloud']
    #     )
    #     weixin_app.send_sms_node_task_message(weixin_message)

    response_result = {
        'status': 'ok'
    }
    return jsonify(response_result)
