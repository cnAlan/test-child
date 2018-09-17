# coding=utf-8
import json
from collections import defaultdict
from nmp_broker.plugins.loadleveler import loadleveler_filter
from nwpc_hpc_model.loadleveler.filter_condition import get_property_data

from nmp_broker.common.database import redis_client


def save_long_time_operation_job_list_to_cache(user, job_items):
    key = "{user}/hpc/loadleveler/long_time_operation_job_warn/job_items".format(user=user)
    redis_client.set(key, json.dumps(job_items))


def get_long_time_operation_job_list_from_cache(user):
    key = "{user}/hpc/loadleveler/long_time_operation_job_warn/job_items".format(user=user)
    result = redis_client.get(key)
    if result is None:
        return None
    result = result.decode()
    return json.loads(result)


def warn_long_time_operation_job(user, message):
    job_items = message['data']['response']['items']
    filter_results = loadleveler_filter.apply_filters(job_items)
    long_time_result = filter_results[0]
    target_job_items = long_time_result['target_job_items']
    if len(target_job_items) > 0:
        print("there is long time job in loadleveler")
        warn_flag = True
        cached_job_items = get_long_time_operation_job_list_from_cache(user)
        if cached_job_items:
            warn_flag = False
            target_job_ids = [get_property_data(a_job, "llq.id") for a_job in target_job_items]
            cached_job_ids = [get_property_data(a_job, "llq.id") for a_job in cached_job_items]
            for a_job_id in target_job_ids:
                if a_job_id not in cached_job_ids:
                    warn_flag = True
                    break

        save_long_time_operation_job_list_to_cache(user, target_job_items)
        categorized_result = defaultdict(int)
        for a_job in target_job_items:
            owner = get_property_data(a_job, "llq.owner")
            categorized_result[owner] += 1
        return {
            'type': 'filter',
            'name': 'warn_long_time_operation_job',
            'data': {
                'warn_flag': warn_flag,
                'target_job_items': target_job_items,
                'categorized_result': categorized_result,
            }
        }
    else:
        return None
