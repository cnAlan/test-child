# coding=utf-8

from flask import jsonify

from nmp_broker.api_v3 import api_v3_app
from nmp_broker.common import data_store

import nmp_broker.api_v3.workflow.orgs.alert


@api_v3_app.route('/workflow/orgs/<org>/repos')
def get_org_repos(org):
    query_repo_result = data_store.get_repos_by_owner_name(org)
    if 'error' in query_repo_result:
        result = {
            'app': 'nmp_broker',
            'error': query_repo_result['error']
        }
        return jsonify(result)

    repos = []
    for an_repo in query_repo_result['data']['repos']:

        repo = {
            'id': an_repo.repo_id,
            'name': an_repo.repo_name,
            'description': an_repo.repo_description
        }
        sms_server_status = data_store.get_server_status_from_cache(org, an_repo.repo_name, an_repo.repo_name)
        if sms_server_status is not None:
            repo['update_time'] = sms_server_status['update_time']
        else:
            repo['update_time'] = None
        repos.append(repo)

    result = {
        'data': {
            'repos': repos
        }
    }

    return jsonify(result)


@api_v3_app.route('/workflow/orgs/<org>/members')
def get_org_members(org):
    query_member_result = data_store.get_repo_members_by_org_name(org)
    if 'error' in query_member_result:
        result = {
            'app': 'nmp_broker',
            'error': query_member_result['error']
        }
        return jsonify(result)

    members = []
    for an_member in query_member_result['data']['members']:
        members.append({
            'id': an_member.owner_id,
            'name': an_member.user_name
        })

    result = {
        'data': {
            'members': members
        }
    }

    return jsonify(result)

