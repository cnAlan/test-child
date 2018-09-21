# coding: utf-8
import datetime
from nmp_broker.common.data_store.rmdb import get_new_64bit_ticket

from nmp_model.mongodb.tree import TreeData, Tree, TreeNode
from nmp_model.mongodb.commit import CommitData, Commit
from nmp_model.mongodb.workflow_cache import WorkflowCacheData, WorkflowCache


def save_server_status_to_nmp_model_system(
        owner: str, repo: str, server_name: str,
        message: dict,
        error_task_dict_list: list
) -> dict:
    """
    保存 sms server 状态到 mongodb 数据库，并返回保存对象的 dict 格式。

    :param owner:
    :param repo:
    :param server_name:
    :param message:
    :param error_task_dict_list:
    :return:
    """
    from nmp_model.mongodb.blobs.status import StatusContent, StatusBlobData, StatusBlob
    status_blob = StatusBlob(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=StatusBlobData(
            name='server_status',
            content=StatusContent(
                server_name=server_name,
                collected_time=message['time'],
                update_time=datetime.datetime.utcnow(),
                status=message['status']
            )
        )
    )
    status_blob.save()

    from nmp_model.mongodb.blobs.aborted_tasks import AbortedTasksContent, AbortedTasksBlobData, AbortedTasksBlob
    aborted_tasks_blob = AbortedTasksBlob(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=AbortedTasksBlobData(
            name='server_aborted_tasks',
            content=AbortedTasksContent(
                status_blob_ticket_id=status_blob.ticket_id,
                server_name='server_aborted_tasks',
                collected_time=message['time'],
                tasks=error_task_dict_list
            )
        )
    )
    aborted_tasks_blob.save()

    tree_object = Tree(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=TreeData(
            nodes=[
                TreeNode(
                    type='status',
                    name='server_status',
                    blob_ticket_id=status_blob.ticket_id
                ),
                TreeNode(
                    type='aborted_tasks',
                    name='server_aborted_tasks',
                    blob_ticket_id=aborted_tasks_blob.ticket_id
                )
            ]
        )
    )
    tree_object.save()

    commit_object = Commit(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=CommitData(
            committer='aix',
            type='status',
            tree_ticket_id=tree_object.ticket_id,
            committed_time=datetime.datetime.utcnow()
        )
    )
    commit_object.save()

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


def save_task_check_to_nmp_model_system(
        owner: str, repo: str,
        message_data: dict,
        unfit_node_list: list
) -> dict:
    from nmp_model.mongodb.blobs.unfit_nodes import UnfitNodesContent, UnfitNodesBlobData, UnfitNodesBlob, \
        UnfitNode, StatusCheckResult, VariableCheckResult

    unfit_nodes = []
    for an_unfit_node_dict in unfit_node_list:
        check_results = []
        for a_result_dict in an_unfit_node_dict['unfit_check_list']:
            check_type = a_result_dict['type']
            if check_type == 'status':
                check_result = StatusCheckResult(
                    is_condition_fit=a_result_dict['is_condition_fit'],
                    value=a_result_dict['value'],
                    expected_value=a_result_dict['expected_value']
                )
            elif check_type == 'variable':
                check_result = VariableCheckResult(
                    is_condition_fit=a_result_dict['is_condition_fit'],
                    variable_name=a_result_dict['name'],
                    expected_value=a_result_dict['expected_value'],
                    value=a_result_dict['value']
                )
            else:
                raise TypeError('check_type is not supported:', check_type)

            check_results.append(check_result)

        an_unfit_node = UnfitNode(
            node_path=an_unfit_node_dict['node_path'],
            check_results=check_results
        )
        unfit_nodes.append(an_unfit_node)

    unfit_nodes_blob = UnfitNodesBlob(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=UnfitNodesBlobData(
            name='check_task_unfit_nodes',
            content=UnfitNodesContent(
                name=message_data['request']['task']['name'],
                trigger=message_data['request']['task']['trigger'],
                check_time=datetime.datetime.utcnow(),
                unfit_nodes=unfit_nodes
            )
        )
    )
    unfit_nodes_blob.save()

    tree_object = Tree(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=TreeData(
            nodes=[
                TreeNode(
                    type="unfit_tasks",
                    name="check_task_unfit_nodes",
                    blob_ticket_id=unfit_nodes_blob.ticket_id
                )
            ]
        )
    )
    tree_object.save()

    commit_object = Commit(
        ticket_id=get_new_64bit_ticket(),
        owner=owner,
        repo=repo,
        data=CommitData(
            committer='broker',
            type='task_check',
            tree_ticket_id=tree_object.ticket_id,
            committed_time=datetime.datetime.utcnow()
        )
    )
    commit_object.save()
    
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


# WorkflowCache

def get_server_status_from_cache(owner: str, repo: str, server_name: str) -> dict or None:
    result_set = WorkflowCache.objects(owner=owner, repo=repo, data__server_name=server_name)
    if len(result_set) == 0:
        return None
    else:
        return result_set.first().to_dict()


def save_server_status_to_cache(owner: str, repo: str, server_name: str, message: dict) -> None:
    result_set = WorkflowCache.objects(owner=owner, repo=repo, data__server_name=server_name)

    data = WorkflowCacheData(
        server_name=server_name,
        collected_time=message['time'],
        update_time=datetime.datetime.utcnow(),
        status=message['status']
    )

    if len(result_set) == 0:
        server_status_cache = WorkflowCache(
            ticket_id=get_new_64bit_ticket(),
            owner=owner,
            repo=repo,
            data=data
        )
        server_status_cache.save()
    else:
        server_status_cache = result_set.first()
        server_status_cache.modify(data=data)

    return
