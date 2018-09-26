# coding: utf-8
import pytest


def test_handle_sms_node_check_message_method(app):
    from nmp_broker.common.workflow.node_check_message_handler import handle_node_check_message
    with app.app_context():
        owner = 'nwp_xp'
        repo = 'nwpc_op'
        message_data = {
            'owner': 'nwp_xp',
            'repo': 'nwpc_op',
            'time': '2018-09-21T15:20:59.667581',
            'request': {
                'task': {
                    'name': 'grapes_meso_post',
                    'type': 'sms-node',
                    'trigger': [
                        {
                            'type': 'time',
                            'time': '11:35:00'
                        }
                    ],
                    "nodes": [
                        {
                            'node_path': '/grapes_meso_post',
                            'check_list': [
                                {
                                    'type': 'variable',
                                    'name': 'SMSDATE',
                                    'value': {
                                        'type': 'date',
                                        'operator': 'equal',
                                        'fields': 'current'
                                    }
                                },
                                {
                                    'type': 'status',
                                    'value': {
                                        'operator': 'in',
                                        'fields': [
                                            "submitted",
                                            "active",
                                            "complete"
                                        ]
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            'response': {
                'nodes': [
                    {
                        'node_path': '/grapes_meso_post',
                        'check_list_result': [
                            {
                                'type': 'variable',
                                'is_condition_fit': False,
                                'name': 'SMSDATE',
                                'expected_value': '20180926',
                                'value': '20180925'
                            },
                            {
                                'type': 'status',
                                'is_condition_fit': True,
                                'expected_value': [
                                    "submitted",
                                    "active",
                                    "complete"
                                ],
                                'value': 'active'
                            }
                        ]
                    }
                ]
            }
        }

        handle_node_check_message(owner, repo, message_data)
