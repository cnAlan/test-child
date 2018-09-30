# coding=utf-8
from flask import request, jsonify, json, current_app
import datetime
import requests
import gzip

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import weixin, data_store

from nmp_broker.plugins.loadleveler import long_time_operation_job_warn

REQUEST_POST_TIME_OUT = 20

@api_v3_app.route('/server/sessions/<host>/<user>/workload/status', methods=['POST'])
def receive_loadleveler_status(host, user):
    """

    :param user:
    :return:

    POST
        message: json string of loadleveler collection result
            {
                app: nwpc_hpc_collector.loadleveler_status,
                type: 'command',
                time: "%Y-%m-%d %H:%M:%S",
                data: {
                    request: {
                        sub_command: args.sub_command,
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

    message_data = message['data']

    key, value = data_store.save_hpc_loadleveler_status_to_cache(user, message)

    if 'error' not in message:
        plugin_result = long_time_operation_job_warn.warn_long_time_operation_job(user, message)
        if plugin_result:
            # if False:
            if not plugin_result['data']['warn_flag']:
                print("Found long time operation jobs. But there is no new one...Skip")
            else:
                print("Found new long time operation jobs. Send warn message.")

                takler_object_system_dict = data_store.save_abnormal_jobs_to_nmp_model_system(
                    user, 'hpc', plugin_result)

                abnormal_jobs_blob_id = None
                for a_blob in takler_object_system_dict['blobs']:
                    if (a_blob['data']['type'] == 'hpc_loadleveler_status' and
                        a_blob['data']['name'] == 'abnormal_jobs'
                    ):
                        abnormal_jobs_blob_id = a_blob['id']
                print(abnormal_jobs_blob_id)

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

                website_url = current_app.config['BROKER_CONFIG']['hpc']['loadleveler_status']['cloud']['put']['url'].format(
                    user=user
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
                weixin_app.send_loadleveler_status_warning_message(
                    user, plugin_result, abnormal_jobs_blob_id)

    print("post loadleveler status to cloud: user=", user)
    post_data = {
        'message': json.dumps(value)
    }
    post_url = current_app.config['BROKER_CONFIG']['hpc']['loadleveler_status']['cloud']['put']['url'].format(
        user=user
    )

    print('gzip the data...')
    gzipped_post_data = gzip.compress(bytes(json.dumps(post_data), 'utf-8'))
    print('gzip the data...done')
    response = requests.post(
        post_url,
        data=gzipped_post_data,
        headers={
            'content-encoding': 'gzip'
        },
        timeout=REQUEST_POST_TIME_OUT
    )
    print("post loadleveler status to cloud done:  response=", response)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)
