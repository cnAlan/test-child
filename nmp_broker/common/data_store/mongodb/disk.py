# coding: utf-8
import datetime

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

