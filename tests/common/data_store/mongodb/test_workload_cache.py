# coding: utf-8
from datetime import datetime
import pytest


def test_loadleveler_to_cache(app):
    with app.app_context():
        from nmp_broker.common.data_store.mongodb.workload import \
            save_workload_status_to_cache, get_workload_status_from_cache
        owner = 'nwpc_xp'
        repo = 'pi_nwp'
        current_time = datetime.utcnow().replace(microsecond=0)
        message = {
            'data': {
                'workload_system': 'loadleveler',
                'collected_time': current_time.isoformat(),
                'type': 'JobListContent',
                'request': {
                    'command': 'loadleveler_status',
                    'sub_command': 'collect',
                    'arguments': [],
                },
                'response': {
                    'items': [
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
                        }
                    ]
                }
            }
        }

        saved_status_cache = save_workload_status_to_cache(
            owner,
            repo,
            message
        )

        status_cache = get_workload_status_from_cache(
            owner,
            repo
        )

        assert status_cache.owner == owner
        assert status_cache.repo == repo
        status_data = status_cache.data
        assert status_data.collected_time.replace(microsecond=0) == current_time
        assert status_data.content.items == message['data']['response']['items']
