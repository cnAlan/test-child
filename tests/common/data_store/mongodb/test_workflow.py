# coding: utf-8
from datetime import datetime

from .fixture import app


def test_save_server_status(app):
    with app.app_context():
        from nmp_broker.common.data_store.mongodb.workflow import save_server_status_to_nmp_model_system
        owner = 'nwpc_xp'
        repo = 'nwpc_op'
        server_name = 'nwpc_op'
        current_time = datetime.utcnow().replace(microsecond=0)
        message = {
            'time': current_time.isoformat(),
            'status': {
                'name': '',
                'node_type': 'root',
                'node_path': '/',
                'path': '/',
                'status': 'aborted',
                'children': []
            }
        }

        error_task_dict_list = [
            {
                'path': '/f1/t1',
                'name': 't1',
                'status': 'aborted'
            },
            {
                'path': '/f2/t2',
                'name': 't2',
                'status': 'aborted'
            },
        ]

        result = save_server_status_to_nmp_model_system(
            owner,
            repo,
            server_name,
            message,
            error_task_dict_list
        )

        blobs = result['blobs']
        trees = result['trees']
        commits = result['commits']

        assert len(blobs) == 2
        assert len(trees) == 1
        assert len(commits) == 1

        # check blobs
        status_blob = blobs[0]
        aborted_tasks_blob = blobs[1]
        assert aborted_tasks_blob['data']['content']['status_blob_ticket_id'] == status_blob['ticket_id']

        # check trees
        tree = trees[0]
        tree_nodes = tree['data']['nodes']
        status_node = tree_nodes[0]
        assert status_node['blob_ticket_id'] == status_blob['ticket_id']
        aborted_tasks_node = tree_nodes[1]
        assert aborted_tasks_node['blob_ticket_id'] == aborted_tasks_blob['ticket_id']

        # check commits
        commit = commits[0]
        assert commit['data']['tree_ticket_id'] == tree['ticket_id']
