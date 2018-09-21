# coding: utf-8
import pytest


def test_handle_ecflow_status_method(app):
    from nmp_broker.common.workflow.message_handler import handle_status_message
    with app.app_context():
        message_data = {
            'owner': 'nwp_xp',
            'repo': 'nwpc_op',
            'time': '2018-09-21T15:20:59.667581',
            'status': {
                "name": "",
                "node_type": "root",
                "node_path": "/",
                "path": "/",
                "status": "aborted",
                "children": [
                    {
                        "name": "windroc_test_suite",
                        "children": [
                            {
                                "name": "initial",
                                "children": [],
                                "node_type": "task",
                                "node_path": "/windroc_test_suite/initial",
                                "path": "/windroc_test_suite/initial",
                                "status": "complete"
                            }
                        ],
                        "node_type": "suite",
                        "node_path": "/windroc_test_suite",
                        "path": "/windroc_test_suite",
                        "status": "complete"
                    },
                    {
                        "name": "grapes_meso_3km_post",
                        "node_type": "suite",
                        "node_path": "/grapes_meso_3km_post",
                        "path": "/grapes_meso_3km_post",
                        "status": "aborted",
                        "children": [
                            {
                                "name": "00",
                                "node_type": "family",
                                "node_path": "/grapes_meso_3km_post/00",
                                "path": "/grapes_meso_3km_post/00",
                                "status": "aborted",
                                "children": [
                                    {
                                        "name": "initial",
                                        "children": [],
                                        "node_type": "task",
                                        "node_path": "/grapes_meso_3km_post/00/initial",
                                        "path": "/grapes_meso_3km_post/00/initial",
                                        "status": "aborted"
                                    },
                                ]
                            }
                        ]
                    }
                ]
            }
        }

        handle_status_message(message_data)
