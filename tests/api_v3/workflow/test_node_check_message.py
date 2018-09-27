# coding: utf-8
import pytest


def test_sms_node_check_message(app):
    from flask import json
    client = app.test_client()
    owner = 'nwp_xp'
    repo = 'nwpc_op'
    message_data = {
        'owner': owner,
        'repo': repo,
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

    message = {
        'data': message_data
    }

    data = {
        'message': json.dumps(message)
    }

    rv = client.post("/api/v3/workflow/repos/{owner}/{repo}/node-check".format(
        owner=owner, repo=repo
    ), data=data)
    assert 'status' in rv.json and rv.json['status'] == 'ok'
