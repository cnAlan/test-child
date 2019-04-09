# coding: utf-8
from flask import json

from nmp_broker.common.database import redis_client


# error task list

def get_error_task_list_from_cache(owner: str, repo: str)-> dict or None:
    error_task_key = "{owner}/{repo}/workflow/task/error".format(owner=owner, repo=repo)
    value = redis_client.get(error_task_key)
    if value is None:
        return None
    cached_error_task_value = json.loads(value.decode())
    return cached_error_task_value


def save_error_task_list_to_cache(owner: str, repo: str, error_task_value: dict)->None:
    error_task_key = "{owner}/{repo}/workflow/task/error".format(owner=owner, repo=repo)
    redis_client.set(error_task_key, json.dumps(error_task_value))
    return
