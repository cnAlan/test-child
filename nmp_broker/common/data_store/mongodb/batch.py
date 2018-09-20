# coding: utf-8
import datetime


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
                'blob_ticket_id': abnormal_jobs_blob.id
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
        'tree_ticket_id': tree_object.id,
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