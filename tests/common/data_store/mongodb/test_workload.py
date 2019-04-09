# coding: utf-8
from datetime import datetime

from nmp_model.mongodb.blobs.workload.abnormal_jobs import AbnormalJobsBlob
from nmp_model.mongodb.tree import Tree
from nmp_model.mongodb.commits.workload_commit import WorkloadCommit


def test_save_server_status(app):
    with app.app_context():
        from nmp_broker.common.data_store.mongodb.workload import save_abnormal_jobs_to_nmp_model_system
        owner = 'nwpc_xp'
        repo = 'nwpc_op'
        current_time = datetime.utcnow().replace(microsecond=0)
        plugin_result = {
            'data': {
                'workload_system': 'loadleveler',
                'user_name': 'nwp_xp',
                'collected_time': current_time,
                'plugins': [
                    {
                        'name': 'warn_long_time_operation_job'
                    }
                ],
                'target_job_items': [
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610339.0",
                                "value": "cma19n02.5610339.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610339.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100412/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:08 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:08"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                    {
                        "props": [
                            {
                                "text": "cma19n02.5610338.0",
                                "value": "cma19n02.5610338.0",
                                "id": "llq.id",
                                "data": "cma19n02.5610338.0"
                            },
                            {
                                "text": "nwp_qu",
                                "value": "nwp_qu",
                                "id": "llq.owner",
                                "data": "nwp_qu"
                            },
                            {
                                "text": "normal1",
                                "value": "normal1",
                                "id": "llq.class",
                                "data": "normal1"
                            },
                            {
                                "text": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "value": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm",
                                "id": "llq.job_script",
                                "data": "/cma/g5/nwp_qu/grapes_vtx/ZJ_Anal/FNL_X0/FNL_X0_2016100200/run/grapes.cm"
                            },
                            {
                                "text": "R",
                                "value": "Running",
                                "id": "llq.status",
                                "data": "R"
                            },
                            {
                                "text": "06/01 10:34",
                                "value": "Thu Jun  1 10:34:05 2017",
                                "id": "llq.queue_date",
                                "data": "2017-06-01 10:34:05"
                            },
                            {
                                "text": "100",
                                "value": "100",
                                "id": "llq.priority",
                                "data": 100.0
                            }
                        ]
                    },
                ]
            }
        }

        result = save_abnormal_jobs_to_nmp_model_system(
            owner,
            repo,
            plugin_result
        )

        blobs = result['blobs']
        trees = result['trees']
        commits = result['commits']

        assert len(blobs) == 1
        assert len(trees) == 1
        assert len(commits) == 1

        # check blobs
        abnormal_jobs_blob = blobs[0]
        assert isinstance(abnormal_jobs_blob, AbnormalJobsBlob)

        # check trees
        tree = trees[0]
        assert isinstance(tree, Tree)
        tree_nodes = tree.data.nodes
        abnormal_jobs_node = tree_nodes[0]
        assert abnormal_jobs_node.blob_ticket_id == abnormal_jobs_blob.ticket_id

        # check commits
        commit = commits[0]
        assert isinstance(commit, WorkloadCommit)
        assert commit.data.tree_ticket_id == tree.ticket_id
