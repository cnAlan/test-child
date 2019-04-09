# coding=utf-8
from .filters import long_time_operation_job_filter, nwp_pd_long_time_upload_job_filter

filter_module_list = [
    long_time_operation_job_filter,
    nwp_pd_long_time_upload_job_filter
]


def apply_filters(job_items):
    filter_results = []
    for a_filter_module in filter_module_list:
        a_filter_object = a_filter_module.create_filter()
        filter_name = a_filter_object['name']
        a_filter = a_filter_object['filter']
        target_job_items = a_filter.filter(job_items)
        filter_results.append({
            'name': filter_name,
            'target_job_items': target_job_items
        })
    return filter_results
