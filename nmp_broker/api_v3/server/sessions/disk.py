# coding=utf-8
from flask import request, jsonify, json, current_app
import datetime
import requests
import gzip

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import data_store


REQUEST_POST_TIME_OUT = 20


@api_v3_app.route('/server/sessions/<host>/<user>/disk/usage', methods=['POST'])
def receive_disk_usage_message(host:str, user:str):
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

    key, value = data_store.save_hpc_disk_usage_status_to_cache(user, message)

    print("post disk usage to cloud: user=", user)
    post_data = {
        'message': json.dumps(value)
    }
    post_url = current_app.config['BROKER_CONFIG']['hpc']['disk_usage']['cloud']['put']['url'].format(
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

    print("post disk usage to cloud done: response=", response)

    result = {
        'status': 'ok'
    }
    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)


@api_v3_app.route('/server/sessions/<host>/<user>/disk/usage', methods=['GET'])
def get_disk_usage_message(host: str, user: str):
    start_time = datetime.datetime.utcnow()

    result = data_store.get_hpc_disk_usage_status_from_cache(user)

    end_time = datetime.datetime.utcnow()
    print(end_time - start_time)

    return jsonify(result)
