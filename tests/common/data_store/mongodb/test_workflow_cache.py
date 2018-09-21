# coding: utf-8
from datetime import datetime
# from mongoengine import connect
import pytest


def test_save_to_cache(app):
    with app.app_context():
        from nmp_broker.common.data_store.mongodb.workflow import \
            get_server_status_from_cache, save_server_status_to_cache
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
                'status': 'active',
                'children': []
            }
        }

        # from nmp_broker.common.database import mongodb_client
        # mongodb_client.close()
        # connect('mongoenginetest', host='mongomock://localhost')

        save_server_status_to_cache(
            owner,
            repo,
            server_name,
            message
        )

        status_cache_dict = get_server_status_from_cache(
            owner,
            repo,
            server_name
        )

        assert status_cache_dict['owner'] == owner
        assert status_cache_dict['repo'] == repo
        status_data = status_cache_dict['data']
        assert status_data['server_name'] == server_name
        assert status_data['collected_time'].replace(microsecond=0) == current_time
        assert status_data['status'] == message['status']
