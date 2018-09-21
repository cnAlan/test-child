# coding=utf-8

from nmp_broker.common import data_store


def is_new_abort_task_found(owner: str, repo: str, previous_server_status, error_task_dict_list:list):
    """
    是否发现新的出错任务

    问题：
        如果大量作业出错，可能会导致发送大量警报
    :param owner:
    :param repo:
    :param previous_server_status:
    :param error_task_dict_list:
    :return:
    """

    new_error_task_found = True

    if previous_server_status == 'abo' \
            or previous_server_status.name.lower() == 'aborted':
        new_error_task_found = False
        cached_error_task_value = data_store.get_error_task_list_from_cache(owner, repo)
        if cached_error_task_value is None:
            return True
        cached_error_task_name_list = [a_task_item['path'] for a_task_item in
                                       cached_error_task_value['error_task_list'] ]
        for a_task in error_task_dict_list:
            if a_task['path'] not in cached_error_task_name_list:
                new_error_task_found = True
                break

    return new_error_task_found


def is_new_abort_root_found(owner: str, repo: str, previous_server_status: str, current_server_status: str='abo'):
    """
    是否刚发现根节点为出错状态

    问题：
        当有其它 suite 已经出错时，如果有新的 suite 出错，不会发送警报
    :param owner:
    :param repo:
    :param previous_server_status:
    :param current_server_status:
    """

    if previous_server_status != 'abo' and current_server_status == 'abo':
        return True
    else:
        return False
