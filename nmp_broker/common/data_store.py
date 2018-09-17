# coding=utf-8
import datetime
#import json
from flask import json

from nmp_broker.common.database import db, mongodb_client, redis_client
from nwpc_monitor.model import Owner, Repo, DingtalkUser, DingtalkWarnWatch, Util

from nwpc_monitor.model.nwpc_takler import Commit, Tree, Blob

# mongodb
nwpc_monitor_platform_mongodb = mongodb_client.nwpc_monitor_platform_develop
sms_server_status = nwpc_monitor_platform_mongodb.sms_server_status
hpc_disk_usage_status = nwpc_monitor_platform_mongodb.hpc_disk_usage_status
hpc_disk_space_status = nwpc_monitor_platform_mongodb.hpc_disk_space_status
hpc_loadleveler_status = nwpc_monitor_platform_mongodb.hpc_loadleveler_status

# mysql

def get_owner_by_name(owner_name: str):
    result = Owner.query_owner_by_owner_name(db.session, owner_name)
    if 'error' in result:
        return None

    return result['data']['owner']

def get_repos_by_owner_name(owner_name: str):
    return Repo.query_repos_by_owner_name(db.session, owner_name)

def get_repo_members_by_org_name(org_name):
    return Util.query_repo_members_by_org_name(db.session, org_name)

def get_ding_talk_warn_user_list(owner: str, repo: str) -> list:
    query = db.session.query(Owner, Repo, DingtalkUser, DingtalkWarnWatch).filter(Repo.owner_id == Owner.owner_id)\
        .filter(Repo.repo_name == repo)  \
        .filter(Owner.owner_name == owner) \
        .filter(DingtalkWarnWatch.repo_id == Repo.repo_id) \
        .filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id)

    warn_to_user_list = []
    for (owner_object, repo_object, dingtalk_user_object, dingtalk_warn_watch_object) in query.all():
        userid = dingtalk_user_object.dingtalk_member_userid
        print(userid)
        warn_to_user_list.append(userid)

    return warn_to_user_list


def get_new_64bit_ticket():
    batch_id = None
    engine = db.engine
    connection = engine.connect()
    trans = connection.begin()
    try:
        connection.execute("REPLACE INTO tickets_64 (stub) VALUES ('a');")
        (batch_id,) = connection.execute('SELECT LAST_INSERT_ID() AS id').fetchone()
        trans.commit()
    except:
        trans.rollback()
        raise
    return batch_id

# takler_object_system

def save_sms_server_status_to_nwpc_takler_object_system(
        owner: str, repo: str, sms_name: str,
        message: dict,
        error_task_dict_list: list
) -> dict:
    """
    保存 sms server 状态到 mongodb 数据库，并返回保存对象的 dict 格式。

    :param owner:
    :param repo:
    :param sms_name:
    :param message:
    :param error_task_dict_list:
    :return:
    """
    status_blob = Blob()
    status_blob.id = get_new_64bit_ticket()
    status_blob.owner = owner
    status_blob.repo = repo
    status_blob_data = {
        'type': 'status',
        'name': 'sms_server_status',
        'content': {
            'sms_name': sms_name,
            'update_time': datetime.datetime.utcnow(),
            'collected_time': message['time'],
            'status': message['status']
        }
    }
    status_blob.set_data(status_blob_data)
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    blobs_collection.insert_one(status_blob.to_dict())

    aborted_tasks_blob = Blob()
    aborted_tasks_blob.id = get_new_64bit_ticket()
    aborted_tasks_blob.owner = owner
    aborted_tasks_blob.repo = repo
    aborted_tasks_blob_data = {
        'type': 'aborted_tasks',
        'name': 'sms_server_aborted_tasks',
        'content': {
            'status_blob_id': status_blob.id,
            'sms_name': sms_name,
            'update_time': datetime.datetime.utcnow(),
            'collected_time': message['time'],
            'tasks': error_task_dict_list
        }
    }
    aborted_tasks_blob.set_data(aborted_tasks_blob_data)
    blobs_collection.insert_one(aborted_tasks_blob.to_dict())

    tree_object = Tree()
    tree_object.id = get_new_64bit_ticket()
    tree_object.owner = owner
    tree_object.repo = repo
    tree_object_data = {
        'nodes': [
            {
                'type': 'status',
                'name': 'sms_server_status',
                'blob_id': status_blob.id
            },
            {
                'type': 'aborted_tasks',
                'name': 'sms_server_aborted_tasks',
                'blob_id': aborted_tasks_blob.id
            }
        ]
    }
    tree_object.set_data(tree_object_data)
    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object.to_dict())

    commit_object = Commit()
    commit_object.id = get_new_64bit_ticket()
    commit_object.owner = owner
    commit_object.repo = repo
    commit_object_data = {
        'committer': 'aix',
        'type': 'status',
        'tree_id': tree_object.id,
        'committed_time': datetime.datetime.utcnow()
    }
    commit_object.set_data(commit_object_data)
    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object.to_dict())

    # NOTE:
    #   如果只保存出错时的任务，Ref就失去意义

    # # find ref in mongodb
    # ref_collection = nwpc_monitor_platform_mongodb.refs
    #
    # ref_key = {
    #     'owner': owner,
    #     'repo': repo,
    #     'data.key': 'sms_server/status/head'
    # }
    # ref_found_result = ref_collection.find_one(ref_key)
    # if ref_found_result is None:
    #     ref_object = Ref()
    #     ref_object.id = get_new_64bit_ticket()
    #     ref_object.owner = owner
    #     ref_object.repo = repo
    #     ref_object_data = {
    #         'key': 'sms_server/status/head',
    #         'type': 'blob',
    #         'id': status_blob.id
    #     }
    #     ref_object.set_data(ref_object_data)
    #     # save
    #     ref_collection.update(ref_key, ref_object.to_dict(), upsert=True)
    # else:
    #     ref_found_result['data']['id'] = status_blob.id
    #     ref_found_result['timestamp'] = datetime.datetime.utcnow()
    #     # save
    #     ref_collection.update(ref_key, ref_found_result, upsert=True)
    return {
        'blobs': [
            status_blob.to_dict(),
            aborted_tasks_blob.to_dict()
        ],
        'trees': [
            tree_object.to_dict()
        ],
        'commits': [
            commit_object.to_dict()
        ]
    }


def save_sms_task_check_to_nwpc_takler_object_system(
        owner: str, repo: str,
        message_data: dict,
        unfit_node_list: list
) -> dict:
    unfit_nodes_blob = Blob()
    unfit_nodes_blob.id = get_new_64bit_ticket()
    unfit_nodes_blob.owner = owner
    unfit_nodes_blob.repo = repo
    status_blob_data = {
        'type': 'unfit_nodes',
        'name': 'sms_check_task_unfit_nodes',
        'content': {
            'name': message_data['request']['task']['name'],
            'trigger': message_data['request']['task']['trigger'],
            'unfit_node_list': unfit_node_list,
            'update_time': datetime.datetime.utcnow(),
        }
    }
    unfit_nodes_blob.set_data(status_blob_data)
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    blobs_collection.insert_one(unfit_nodes_blob.to_dict())

    tree_object = Tree()
    tree_object.id = get_new_64bit_ticket()
    tree_object.owner = owner
    tree_object.repo = repo
    tree_object_data = {
        'nodes': [
            {
                'type': 'unfit_tasks',
                'name': 'sms_check_task_unfit_nodes',
                'blob_id': unfit_nodes_blob.id
            }
        ]
    }
    tree_object.set_data(tree_object_data)
    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object.to_dict())

    commit_object = Commit()
    commit_object.id = get_new_64bit_ticket()
    commit_object.owner = owner
    commit_object.repo = repo
    commit_object_data = {
        'committer': 'broker',
        'type': 'task_check',
        'tree_id': tree_object.id,
        'committed_time': datetime.datetime.utcnow()
    }
    commit_object.set_data(commit_object_data)
    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object.to_dict())

    return {
        'blobs': [
            unfit_nodes_blob.to_dict()
        ],
        'trees': [
            tree_object.to_dict()
        ],
        'commits': [
            commit_object.to_dict()
        ]
    }


def save_loadleveler_status_to_nwpc_takler_object_system(
        owner: str, repo: str,
        plugin_result: dict
) -> dict:
    abnormal_jobs_blob = Blob()
    abnormal_jobs_blob.id = get_new_64bit_ticket()
    abnormal_jobs_blob.owner = owner
    abnormal_jobs_blob.repo = repo
    status_blob_data = {
        'type': 'hpc_loadleveler_status',
        'name': 'abnormal_jobs',
        'content': {
            'plugin_name': plugin_result['name'],
            'abnormal_job_list': plugin_result['data']['target_job_items'],
            'update_time': datetime.datetime.utcnow(),
        }
    }
    abnormal_jobs_blob.set_data(status_blob_data)
    blobs_collection = nwpc_monitor_platform_mongodb.blobs
    blobs_collection.insert_one(abnormal_jobs_blob.to_dict())

    tree_object = Tree()
    tree_object.id = get_new_64bit_ticket()
    tree_object.owner = owner
    tree_object.repo = repo
    tree_object_data = {
        'nodes': [
            {
                'type': 'hpc_loadleveler_status',
                'name': 'abnormal_jobs',
                'blob_id': abnormal_jobs_blob.id
            }
        ]
    }
    tree_object.set_data(tree_object_data)
    trees_collection = nwpc_monitor_platform_mongodb.trees
    trees_collection.insert_one(tree_object.to_dict())

    commit_object = Commit()
    commit_object.id = get_new_64bit_ticket()
    commit_object.owner = owner
    commit_object.repo = repo
    commit_object_data = {
        'committer': 'broker',
        'type': 'hpc_loadleveler_status',
        'tree_id': tree_object.id,
        'committed_time': datetime.datetime.utcnow()
    }
    commit_object.set_data(commit_object_data)
    commits_collection = nwpc_monitor_platform_mongodb.commits
    commits_collection.insert_one(commit_object.to_dict())

    return {
        'blobs': [
            abnormal_jobs_blob.to_dict()
        ],
        'trees': [
            tree_object.to_dict()
        ],
        'commits': [
            commit_object.to_dict()
        ]
    }


# sms

def get_sms_server_status_from_cache(owner: str, repo: str, sms_name: str) -> dict:
    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name
    }
    result = sms_server_status.find_one(key)
    return result


def save_sms_server_status_to_cache(owner: str, repo: str, sms_name: str, message: dict) -> None:
    key = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name
    }
    value = {
        'owner': owner,
        'repo': repo,
        'sms_name': sms_name,
        'update_time': datetime.datetime.utcnow(),
        'collected_time': message['time'],
        'status': message['status']
    }
    sms_server_status.update(key, value, upsert=True)

    return

# hpc
# disk usage


def get_hpc_disk_usage_status_from_cache(user: str) -> dict:
    key = {
        'user': user
    }
    result = hpc_disk_usage_status.find_one(key, {"_id": 0})
    return result


def save_hpc_disk_usage_status_to_cache(user: str, message: dict) -> tuple:
    key = {
        'user': user
    }
    value = {
        'user': user,
        'update_time': datetime.datetime.utcnow(),
        'message': message
    }
    hpc_disk_usage_status.update(key, value, upsert=True)
    return key, value


# disk space

def get_hpc_disk_space_status_from_cache() -> dict:
    key = {
        'user': 'hpc'
    }
    result = hpc_disk_space_status.find_one(key, {"_id": 0})
    return result


def save_hpc_disk_space_status_to_cache(message:str) -> tuple:
    key = {
        'user': 'hpc'
    }
    value = {
        'user': 'hpc',
        'update_time': datetime.datetime.utcnow(),
        'message': message
    }
    hpc_disk_space_status.update(key, value, upsert=True)
    return key, value


# loadleveler status

def save_hpc_loadleveler_status_to_cache(user: str, message: dict) -> tuple:
    key = {
        'data.user': user
    }
    value = {
        'app': 'nmp_broker',
        'event': 'post_sms_task_check',
        'data': {
            'user': user,
            'type': 'job_list',
            'update_time': datetime.datetime.utcnow(),
            'message': message
        }

    }
    hpc_loadleveler_status.update(key, value, upsert=True)
    return key, value


def get_hpc_loadleveler_status_from_cache(user: str) -> dict:
    key = {
        'owner': user
    }
    value = hpc_loadleveler_status.find_one(key, {"_id": 0})
    return value


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