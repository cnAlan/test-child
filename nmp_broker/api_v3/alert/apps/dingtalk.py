# coding=utf-8
from flask import jsonify, current_app

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import ding_talk

REQUEST_POST_TIME_OUT = 20


@api_v3_app.route('/alert/apps/dingtalk/access_token/get', methods=['GET'])
def get_dingtalk_access_token():
    auth = ding_talk.Auth(current_app.config['BROKER_CONFIG']['ding_talk_app']['token'])
    result = auth.get_access_token_from_server()
    print(result)
    return jsonify(result)
