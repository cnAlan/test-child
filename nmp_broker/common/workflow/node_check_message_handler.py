# coding: utf-8
import datetime
import gzip

import requests
from flask import current_app, json

from nmp_broker.common import weixin, data_store

from nmp_model.mongodb.blobs.unfit_nodes import UnfitNodesBlob


REQUEST_POST_TIME_OUT = 20


def handle_node_check_message(owner, repo, message_data: dict) -> None:
    """

    :param owner: owner name
    :param repo: repo name
    :param message_data: a dict of message data.
    {
        'owner': owner,
        'repo': repo,
        'request': {
            'task': {
                'name': 'grapes_meso_post',
                'type': 'sms-node',
                'trigger': [
                    {
                        'type': 'time',
                        'time': '11:35:00'
                    }
                ],
                "nodes": [
                    {
                        'node_path': '/grapes_meso_post',
                        'check_list': [
                            {
                                'type': 'variable',
                                'name': 'SMSDATE',
                                'value': {
                                    'type': 'date',
                                    'operator': 'equal',
                                    'fields': 'current'
                                }
                            },
                            {
                                'type': 'status',
                                'value': {
                                    'operator': 'in',
                                    'fields': [
                                        "submitted",
                                        "active",
                                        "complete"
                                    ]
                                }
                            }
                        ]
                    }
                ]
            },
        },
        'response': {
            'nodes':[
                {
                    'node_path': node_path,
                    'check_list_result': array, see check_sms_node
                },
                ...
            ]
        }
    }
    :return:
    """
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

        takler_object_system_dict = data_store.save_task_check_to_nmp_model_system(
            owner, repo,
            message_data, unfit_node_list
        )

        unfit_nodes_blob_id = None
        for a_blob in takler_object_system_dict['blobs']:
            if isinstance(a_blob, UnfitNodesBlob):
                unfit_nodes_blob_id = a_blob.ticket_id
                weixin_message['data']['unfit_nodes_blob_id'] = unfit_nodes_blob_id
        print(unfit_nodes_blob_id)

        post_message = {
            'app': 'nmp_broker',
            'event': 'post_sms_task_check',
            'timestamp': datetime.datetime.utcnow(),
            'data': {
                'type': 'takler_object',
                'blobs': [blob.to_mongo().to_dict() for blob in takler_object_system_dict['blobs']],
                'trees': [blob.to_mongo().to_dict() for blob in takler_object_system_dict['trees']],
                'commits': [blob.to_mongo().to_dict() for blob in takler_object_system_dict['commits']],
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

        # weixin_app = weixin.WeixinApp(
        #     weixin_config=current_app.config['BROKER_CONFIG']['weixin_app'],
        #     cloud_config=current_app.config['BROKER_CONFIG']['cloud']
        # )
        # weixin_app.send_sms_node_task_warn(weixin_message)

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
