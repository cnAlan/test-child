# coding=utf-8
import requests
from flask import json

from nmp_broker.common.data_store.redis.alert import (
    save_dingtalk_access_token_to_cache, get_dingtalk_access_token_from_cache)
from nmp_broker.common.data_store.rmdb import get_ding_talk_warn_user_list

REQUEST_POST_TIME_OUT = 20


class Auth(object):
    def __init__(self, config: dict):
        """
        :param config:
            {
                "name": "TokenConfig",
                "type": "record",
                "fields": [
                    {"name": "corp_id", type: "string"},
                    {"name": "corp_secret", type: "string"},
                    {"name": "url", type: "string"},
                ]
            }
        :return:
        """
        self.corp_id = config['corp_id']
        self.corp_secret = config['corp_secret']
        self.url = config['url']

    def get_access_token_from_server(self) -> dict:
        headers = {'content-type': 'application/json'}
        url = self.url.format(
            corp_id=self.corp_id, corp_secret=self.corp_secret
        )

        token_response = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=REQUEST_POST_TIME_OUT
        )

        response_json = token_response.json()
        print(response_json)
        if response_json['errcode'] == 0:
            access_token = response_json['access_token']
            save_dingtalk_access_token_to_cache(access_token)
            result = {
                'status': 'ok',
                'access_token': access_token
            }
        else:
            result = {
                'status': 'error',
                'errcode': response_json['errcode']
            }
        return result

    def get_access_token_from_cache(self) -> str:
        return get_dingtalk_access_token_from_cache()

    def save_access_token_to_cache(self, access_token: str) -> None:
        return save_dingtalk_access_token_to_cache(access_token)

    def get_access_token(self) -> str:
        dingtalk_access_token = get_dingtalk_access_token_from_cache()
        if dingtalk_access_token is None:
            self.get_access_token_from_server()
            dingtalk_access_token = get_dingtalk_access_token_from_cache()
        return dingtalk_access_token


class DingTalkApp(object):
    def __init__(self, ding_talk_config:dict, cloud_config:dict):
        self.ding_talk_config = ding_talk_config
        self.cloud_config = cloud_config

        self.auth = Auth(self.ding_talk_config['token'])

    def send_warning_message(self, warning_data):
        """
        :param warning_data:
            {
                "name": "WarningData",
                "namespace": "WeixinApp",
                "type": "record",
                "fields": [
                    {"name": "owner", type: "string"},
                    {"name": "repo", type: "string"},
                    {"name": "sms_server_name", type: "string"},
                    {"name": "message_datetime", type: "datetime"},
                    {"name": "suite_error_map", type: "array"},
                    {"name": "aborted_tasks_blob_id", type: "int"},
                ]
            }
        :return:
        """
        warn_user_list = get_ding_talk_warn_user_list(warning_data['owner'], warning_data['repo'])

        print('Get new error task. Pushing warning message...')

        auth = Auth(self.ding_talk_config['token'])
        dingtalk_access_token = auth.get_access_token()

        if warning_data['aborted_tasks_blob_id']:
            message_url = (self.cloud_config['base']['url'] + '/{owner}/{repo}/aborted_tasks/{id}').format(
                owner=warning_data['owner'],
                repo=warning_data['repo'],
                id=warning_data['aborted_tasks_blob_id']
            )
        else:
            message_url = self.cloud_config['base']['url']

        warning_post_url = self.ding_talk_config['warn']['url'].format(
            dingtalk_access_token=dingtalk_access_token
        )

        form_suite_error_list = []
        for a_suite_name in warning_data['suite_error_map']:
            a_suite_item = warning_data['suite_error_map'][a_suite_name]
            if len(a_suite_item['error_task_list']) > 0:
                form_suite_error_list.append({
                    'name': a_suite_item['name'],
                    'count': len(a_suite_item['error_task_list'])
                })

        warning_post_message = {
            "touser":"|".join(warn_user_list),
            "agentid": self.ding_talk_config['warn']['agentid'],
            "msgtype":"oa",
            "oa": {
                "message_url": message_url,
                "head": {
                    "bgcolor": "ffff0000",
                    "text": "业务系统报警"
                },
                "body":{
                    "title":"业务系统运行出错",
                    "content":"{sms_server_name} 出错，请查看\n出错 suite 列表：".format(sms_server_name=warning_data['sms_server_name']),
                    "form":[
                        {
                            "key": "日期 : ",
                            "value": "{error_date}".format(error_date=warning_data['message_datetime'].strftime("%Y-%m-%d"))
                        },
                        {
                            "key": "时间 : ",
                            "value": "{error_time}".format(error_time=warning_data['message_datetime'].strftime("%H:%M:%S"))
                        }
                    ]
                }
            }
        }
        for a_suite in form_suite_error_list:
            warning_post_message['oa']['body']['form'].insert(0, {
                'key': a_suite['name'] + ' : ',
                'value': a_suite['count']
            })

        warning_post_headers = {'content-type': 'application/json'}
        warning_post_data = json.dumps(warning_post_message)

        result = requests.post(
            warning_post_url,
            data=warning_post_data,
            verify=False,
            headers=warning_post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())
