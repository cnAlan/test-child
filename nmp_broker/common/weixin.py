# coding=utf-8
from datetime import datetime
import requests
from flask import json, current_app
from collections import defaultdict

from nmp_broker.common.data_store.redis.alert import save_weixin_access_token_to_cache, get_weixin_access_token_from_cache

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
            save_weixin_access_token_to_cache(access_token)
            result = {
                'status': 'ok',
                'access_token': access_token
            }
        else:
            result = {
                'status': 'error',
                'errcode': response_json['errcode'],
                'errmsg': response_json['errmsg']
            }

        return result

    def get_access_token_from_cache(self) -> str:
        return get_weixin_access_token_from_cache()

    def save_access_token_to_cache(self, access_token: str) -> None:
        return save_weixin_access_token_to_cache(access_token)

    def get_access_token(self) -> str:
        weixin_access_token = get_weixin_access_token_from_cache()
        if weixin_access_token is None:
            self.get_access_token_from_server()
            weixin_access_token = get_weixin_access_token_from_cache()
        return weixin_access_token


class WeixinApp(object):
    def __init__(self, weixin_config:dict, cloud_config:dict):
        self.weixin_config = weixin_config
        self.cloud_config = cloud_config

        self.auth = Auth(self.weixin_config['token'])

    def send_warning_message(self, warning_data: dict):
        """
        :param warning_data:
            {
                "name": "WarningData",
                "namespace": "WeixinApp",
                "type": "record",
                "fields": [
                    {"name": "owner", type: "string"},
                    {"name": "repo", type: "string"},
                    {"name": "server_name", type: "string"},
                    {"name": "message_datetime", type: "datetime"},
                    {"name": "suite_error_map", type: "array"},
                    {"name": "aborted_tasks_blob_id", type: "int"},
                ]
            }
        :return:
        """
        # TODO: change server_name
        owner = warning_data['owner']
        repo = warning_data['repo']
        current_app.logger.info('[{owner}/{repo}] get error task. Pushing warning message to weixin...'.format(
            owner=owner, repo=repo
        ))

        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        warning_post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )

        if warning_data['aborted_tasks_blob_id']:
            message_url = (self.cloud_config['base']['url'] + '/{owner}/{repo}/aborted_tasks/{id}').format(
                owner=warning_data['owner'],
                repo=warning_data['repo'],
                id=warning_data['aborted_tasks_blob_id']
            )
        else:
            message_url = self.cloud_config['base']['url']

        form_suite_error_list = []
        for a_suite_name in warning_data['suite_error_map']:
            a_suite_item = warning_data['suite_error_map'][a_suite_name]
            if len(a_suite_item['error_task_list']) > 0:
                form_suite_error_list.append({
                    'name': a_suite_item['name'],
                    'count': len(a_suite_item['error_task_list'])
                })

        task_list = '出错系统列表：'
        for a_suite in form_suite_error_list:
            task_list += "\n" + a_suite['name'] + ' : ' + str(a_suite['count'])

        articles = [
            {
                "title": "业务系统：{server_name}运行出错".format(server_name=warning_data['server_name']),
                "picurl": "http://wx2.sinaimg.cn/large/4afdac38ly1feu4tqm9c6j21kw0sggmu.jpg",
                "url": message_url
            },
            {
                "title": "项目：{owner}/{repo}".format(
                    owner=warning_data['owner'],
                    repo=warning_data['repo']
                ),
                "url": message_url
            },
            {
                "title":
                    "日期 : {error_date}\n".format(
                        error_date=datetime.utcnow().strftime("%Y-%m-%d"))
                    + "时间 : {error_time}".format(
                        error_time=datetime.utcnow().strftime("%H:%M:%S")),
                "url": message_url
            },
            {
                "title": task_list,
                "url": message_url
            },
            {
                "title": '点击查看详情',
                "url": message_url
            }
        ]

        to_user = self.weixin_config['warn']['to_user']

        warning_post_message = {
            "touser": to_user,
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        warning_post_headers = {
            'content-type': 'application/json'
        }
        warning_post_data = json.dumps(warning_post_message,ensure_ascii=False).encode('utf8')

        result = requests.post(
            warning_post_url,
            data=warning_post_data,
            verify=False,
            headers=warning_post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        current_app.logger.info('[{owner}/{repo}] Pushing warning message to weixin...done. {result}'.format(
            owner=owner, repo=repo, result=result.json()
        ))

    def send_sms_node_task_warn(self, message):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        warning_post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )

        node_list_content = ''
        for a_unfit_node in message['data']['unfit_nodes']:

            node_list_content += a_unfit_node['node_path'] + ':'
            unfit_map = defaultdict(int)
            for a_check_condition in a_unfit_node['unfit_check_list']:
                unfit_map[a_check_condition['type']] += 1

            for (type_name, count) in unfit_map.items():
                node_list_content += " {type_name}[{count}]".format(
                    type_name=type_name, count=count)
            node_list_content += '\n'

        message_url = (self.cloud_config['base']['url'] + '/{owner}/{repo}/task_check/unfit_nodes/{id}').format(
            owner=message['data']['owner'],
            repo=message['data']['repo'],
            id=message['data']['unfit_nodes_blob_id']
        )
        to_user = self.weixin_config['warn']['to_user']

        articles = [
            {
                'title': "业务系统异常：{repo} 节点状态".format(repo=message['data']['repo']),
                "picurl": "http://wx2.sinaimg.cn/mw690/4afdac38ly1feqnwb44kkj2223112wfj.jpg",
                'url': message_url
            },
            {
                "title": "{owner}/{repo}".format(
                    owner=message['data']['owner'],
                    repo=message['data']['repo']
                ),
                "description": message['data']['task_name'],
                'url': message_url
            },
            {
                'title':
                    "日期 : {error_date}\n".format(
                        error_date=datetime.utcnow().strftime("%Y-%m-%d"))
                    + "时间 : {error_time}".format(
                        error_time=datetime.utcnow().strftime("%H:%M:%S")),
                'url': message_url
            },
            {
                "title": message['data']['task_name'] + " 运行异常",
                'url': message_url
            },
            {
                'title': '异常任务列表\n' + node_list_content,
                'description': '点击查看详情',
                'url': message_url
            }
        ]

        warning_post_message = {
            "touser": to_user,
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }

        warning_post_headers = {
            'content-type': 'application/json'
        }
        warning_post_data = json.dumps(warning_post_message, ensure_ascii=False).encode('utf8')

        result = requests.post(
            warning_post_url,
            data=warning_post_data,
            verify=False,
            headers=warning_post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())

    def send_sms_node_task_message(self, message_data):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )
        message_url = (self.cloud_config['base']['url'] + '/{owner}/{repo}/task_check/unfit_nodes/{id}').format(
            owner=message_data['owner'],
            repo=message_data['repo']
        )
        articles = [
            {
                "title": "业务系统：SMS节点状态检查",
                "picurl": "http://wx2.sinaimg.cn/large/4afdac38ly1feqnewxygsj20hs08wt8u.jpg",
                'url': message_url
            },
            {
                "title": "{owner}/{repo}".format(
                    owner=message_data['data']['owner'],
                    repo=message_data['data']['repo']
                ),
                "description": message_data['data']['task_name'],
                'url': message_url
            },
            {
                "title":
                    "{error_date} {error_time}".format(
                        error_date=datetime.utcnow().strftime("%Y-%m-%d"),
                        error_time=datetime.utcnow().strftime("%H:%M:%S")
                    ),
                'url': message_url
            },
            {
                "title": message_data['data']['task_name'] + " 运行正常",
                'url': message_url
            }
        ]

        to_user = self.weixin_config['warn']['to_user']
        post_message = {
            "touser": to_user,
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }

        post_headers = {
            'content-type': 'application/json'
        }
        post_data = json.dumps(post_message, ensure_ascii=False).encode('utf8')

        result = requests.post(
            post_url,
            data=post_data,
            verify=False,
            headers=post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())

    def send_loadleveler_status_warning_message(self, user, plugin_check_result, abnormal_jobs_blob_id):
        text = ""
        for a_owner in plugin_check_result['data']['categorized_result']:
            text += "\n{owner}:{number}".format(
                owner=a_owner,
                number=plugin_check_result['data']['categorized_result'][a_owner])
        message_url = (self.cloud_config['base']['url'] + '/hpc/{user}/loadleveler/abnormal_jobs/{abnormal_jobs_blob_id}').format(
            user=user,
            abnormal_jobs_blob_id=abnormal_jobs_blob_id
        )
        articles = [
            {
                "title": "业务系统：队列异常",
                "picurl": "http://wx2.sinaimg.cn/large/4afdac38ly1fg4b31u8dqj21kw0sgjto.jpg",
                "url": message_url
            },
            {
                "title":
                    "{error_date} {error_time}".format(
                        error_date=datetime.utcnow().strftime("%Y-%m-%d"),
                        error_time=datetime.utcnow().strftime("%H:%M:%S")
                    ),
                "url": message_url
            },
            {
                "title": "异常用户:" + text,
                "url": message_url
            }
        ]
        to_user = self.weixin_config['warn']['to_user']
        post_message = {
            "touser": to_user,
            "agentid": 2,
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        self.send_message(post_message)

    def send_message(self, message):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()

        post_url = self.weixin_config['warn']['url'].format(
            weixin_access_token=weixin_access_token
        )
        post_headers = {
            'content-type': 'application/json'
        }
        post_data = json.dumps(message, ensure_ascii=False).encode('utf8')

        result = requests.post(
            post_url,
            data=post_data,
            verify=False,
            headers=post_headers,
            timeout=REQUEST_POST_TIME_OUT
        )
        print(result.json())
