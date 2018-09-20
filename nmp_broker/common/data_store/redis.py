# coding: utf-8
from flask import json

from nmp_broker.common.database import redis_client

# redis
dingtalk_access_token_key = "dingtalk_access_token"


def get_dingtalk_access_token_from_cache() -> str:
    dingtalk_access_token = redis_client.get(dingtalk_access_token_key)
    dingtalk_access_token = dingtalk_access_token.decode()
    return dingtalk_access_token


def save_dingtalk_access_token_to_cache(access_token: str) -> None:
    redis_client.set(dingtalk_access_token_key, access_token)
    return


weixin_access_token_key = "weixin_access_token"


def get_weixin_access_token_from_cache() -> str or None:
    weixin_access_token = redis_client.get(weixin_access_token_key)
    if weixin_access_token is None:
        return None
    weixin_access_token = weixin_access_token.decode()
    return weixin_access_token


def save_weixin_access_token_to_cache(access_token: str) -> None:
    redis_client.set(weixin_access_token_key, access_token)
    return


def get_error_task_list_from_cache(owner: str, repo: str)-> dict:
    error_task_key = "{owner}/{repo}/sms/task/error".format(owner=owner, repo=repo)
    cached_error_task_value = json.loads(redis_client.get(error_task_key).decode())
    return cached_error_task_value


def save_error_task_list_to_cache(owner: str, repo: str, error_task_value: dict)->None:
    error_task_key = "{owner}/{repo}/sms/task/error".format(owner=owner, repo=repo)
    redis_client.set(error_task_key, json.dumps(error_task_value))
    return
