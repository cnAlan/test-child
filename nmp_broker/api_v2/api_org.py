# coding=utf-8

from flask import jsonify

from nmp_broker.api_v2 import api_v2_app
from nmp_broker.common import data_store
from nmp_broker.common.database import db

from nmp_model.rmdb import Repo, Owner, User, OrgUser, DingtalkUser, DingtalkWarnWatch, Util

from sqlalchemy import func


@api_v2_app.route('/orgs/<org>/repos')
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


@api_v2_app.route('/orgs/<org>/members')
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


# 报警

@api_v2_app.route('/orgs/<owner>/warning/dingtalk/watch/watchers/suggested')
def get_org_warning_watch_suggested_user(owner: str):
    """
    返回该组织的推荐关注用户列表
    :param owner:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'warning': {
                    'type': 'dingtalk',
                    'suggested_user_list': [
                        {
                            'owner_name': owner_name,
                            'is_watching': true or false,
                            'watching_repo_count': repo count
                        },
                        ...
                    ]
                }
            }
        }

        出错
        {
            'error': error message
        }
    """
    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id)

    repo_query_result = repo_query.all()

    repo_count = len(repo_query_result)

    if repo_count == 0:
        result = {
            'error': 'no repo for {owner}'.format(owner=owner)
        }
        return jsonify(result)

    repo_object_list = []
    (owner_object, repo_object) = repo_query_result[0]
    for (an_owner_object, a_repo_object) in repo_query_result:
        repo_object_list.append(a_repo_object)

    suggested_user_list = []

    if owner_object.owner_type == 'user':
        member_to_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(DingtalkUser.user_id == owner_object.owner_id). \
            subquery()
    elif owner_object.owner_type == 'org':
        member_to_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(Owner.owner_id == OrgUser.user_id). \
            filter(OrgUser.org_id == owner_object.owner_id). \
            filter(DingtalkUser.user_id == Owner.owner_id). \
            subquery()
    else:
        result = {
            'error': 'owner type {owner_type} is not supported'.format(owner_type=owner_object.owner_type)
        }
        return jsonify(result)

    dingtalk_warn_watch_query = db.session.query(DingtalkWarnWatch.id, DingtalkWarnWatch.dingtalk_user_id). \
        filter(DingtalkWarnWatch.repo_id == Repo.repo_id). \
        filter(Repo.owner_id == owner_object.owner_id). \
        subquery()

    # SELECT a.owner_name, COUNT(b.id) as repo_count
    # FROM (
    #    SELECT owner.owner_name, dingtalk_user.dingtalk_user_id FROM owner, org_user, dingtalk_user
    #    WHERE owner.owner_id = org_user.user_id
    #    AND org_user.org_id = 2
    #    AND dingtalk_user.user_id = owner.owner_id
    # ) as a
    # LEFT JOIN (
    # 	SELECT dingtalk_warn_watch.id, dingtalk_warn_watch.dingtalk_user_id FROM dingtalk_warn_watch, repo
    #     WHERE dingtalk_warn_watch.repo_id = repo.repo_id
    #     AND repo.owner_id = 2
    # ) as b
    # ON b.dingtalk_user_id = a.dingtalk_user_id
    # GROUP BY a.owner_name

    suggested_user_query = db.session.query(member_to_dingtalk_user_id_query.c.owner_name, func.count(dingtalk_warn_watch_query.c.id)). \
        outerjoin(
            dingtalk_warn_watch_query,
            member_to_dingtalk_user_id_query.c.dingtalk_user_id == dingtalk_warn_watch_query.c.dingtalk_user_id,
        ). \
        order_by(member_to_dingtalk_user_id_query.c.owner_name).\
        group_by(member_to_dingtalk_user_id_query.c.owner_name)

    suggested_user_query_result = suggested_user_query.all()
    for (an_user_name, repo_count) in suggested_user_query_result:
        suggested_user_list.append({
            "owner_name": an_user_name,
            "is_watching": False,
            "watching_repo_count": repo_count
        })

    result = {
        'data': {
            'owner': owner,
            'repo_count': repo_count,
            'warning': {
                'type': 'dingtalk',
                'suggested_user_list': suggested_user_list
            }
        }
    }

    return jsonify(result)


@api_v2_app.route('/orgs/<owner>/warning/dingtalk/watch/watchers')
def get_org_warning_dingtalk_watch_users(owner: str):
    """
    返回关注某组织下的项目的用户
    :param owner:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'warning': {
                    'type': 'dingtalk',
                    'watching_user_list': [
                        {
                            'owner_name': owner_object.owner_name,
                            # 'warn_watch': {
                            #     'start_date_time': ding_talk_warn_watch_object.start_date_time,
                            #     'end_date_time': ding_talk_warn_watch_object.end_date_time
                            # },
                            'is_watching': True
                        },
                        ...
                    ]
                }
        }

        出错
        {
            'error': error message
        }
    """
    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id)

    repo_query_result = repo_query.all()

    repo_count = len(repo_query_result)

    if repo_count == 0:
        result = {
            'error': 'no repo for {owner}'.format(owner=owner)
        }
        return jsonify(result)

    repo_object_list = []
    (owner_object, repo_object) = repo_query_result[0]
    for (an_owner_object, a_repo_object) in repo_query_result:
        repo_object_list.append(a_repo_object)

    watch_user_query = db.session.query(User.user_name, func.count(DingtalkWarnWatch.id)). \
        filter(Owner.owner_id == owner_object.owner_id). \
        filter(Repo.owner_id == Owner.owner_id). \
        filter(DingtalkWarnWatch.repo_id == Repo.repo_id). \
        filter(User.owner_id == DingtalkUser.user_id). \
        filter(DingtalkUser.dingtalk_user_id == DingtalkWarnWatch.dingtalk_user_id). \
        group_by(User.user_name)

    watch_user_query_result = watch_user_query.all()

    user_list = []
    for (user_name, watch_repo_count) in watch_user_query_result:
        an_user = {
            'owner_name': user_name,
            'watching_repo_count': watch_repo_count,
            'is_watching': True
        }
        user_list.append(an_user)

    result = {
        'data': {
            'owner': owner,
            'repo_count': repo_count,
            'warning': {
                'type': 'dingtalk',
                'watching_user_list': user_list
            }
        }
    }

    return jsonify(result)


@api_v2_app.route('/orgs/<owner>/warning/dingtalk/watch/watcher/<user>', methods=['POST'])
def create_org_dingtalk_watcher(owner, user):
    """
    user关注owner/repo项目

    POST /orgs/<owner>/warning/dingtalk/watch/watcher/<user>

    Input: none

    Response:

    {
        'data': {
            'status': 'ok'
        }
    }

    """
    # check owner
    query_user_result = Owner.query_owner_by_owner_name(db.session, owner)
    if 'error' in query_user_result:
        result = {
            'error': "get owner error",
            'data': {
                'message': query_user_result['error']
            }
        }
        return jsonify(result)
    elif query_user_result['data']['owner'] is None:
        result = {
            'error': "owner doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    owner_object = query_user_result['data']['owner']

    # check user
    user_sub_query = db.session.query(Owner). \
        filter(Owner.owner_name == user). \
        subquery()

    user_query = db.session.query(user_sub_query.c.owner_id, DingtalkUser). \
        outerjoin(DingtalkUser, DingtalkUser.user_id == user_sub_query.c.owner_id)

    user_query_result = user_query.all()

    if len(user_query_result) >1:
        result = {
            'error': "get user error",
            'data': {
                'message': 'we have more than one owner with a single name, please contact admin.'
            }
        }
        return jsonify(result)

    if user_query_result is None:
        result = {
            'error': "owner doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    user_id, ding_talk_user_object = user_query_result[0]

    if ding_talk_user_object is None:
        result = {
            'error': "owner's dingtalk user doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    # query repos owned by owner
    repo_query = db.session.query(Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id). \
        subquery()

    ding_talk_warn_query = db.session.query(DingtalkWarnWatch). \
        filter(DingtalkWarnWatch.dingtalk_user_id == ding_talk_user_object.dingtalk_user_id). \
        subquery()

    # query watcher
    watcher_query = db.session.query(repo_query.c.repo_id, ding_talk_warn_query.c.id). \
        outerjoin(
            ding_talk_warn_query,
            ding_talk_warn_query.c.repo_id == repo_query.c.repo_id
        )

    dt_warn_watch_result = watcher_query.all()

    for (a_repo_id, a_watch_id) in dt_warn_watch_result:
        if a_watch_id is None:
            # insert watcher
            new_watcher = DingtalkWarnWatch()
            new_watcher.repo_id = a_repo_id
            new_watcher.dingtalk_user_id = ding_talk_user_object.dingtalk_user_id
            db.session.add(new_watcher)

    db.session.commit()

    return jsonify({
        'data': {
            'status': 'ok'
        }
    })


@api_v2_app.route('/orgs/<owner>/warning/dingtalk/watch/watcher/<user>', methods=['DELETE'])
def delete_org_dingtalk_watcher(owner, user):
    """
    取消user对owner所有项目的关注

    DELETE /orgs/<owner>/warning/dingtalk/watch/watcher/<user>

    Input: none

    Response:

    {
        'data': {
            'status': 'ok'
        }
    }

    """

    # check owner
    query_user_result = Owner.query_owner_by_owner_name(db.session, owner)
    if 'error' in query_user_result:
        result = {
            'error': "get owner error",
            'data': {
                'message': query_user_result['error']
            }
        }
        return jsonify(result)
    elif query_user_result['data']['owner'] is None:
        result = {
            'error': "owner doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    owner_object = query_user_result['data']['owner']

    # check user
    user_sub_query = db.session.query(Owner). \
        filter(Owner.owner_name == user). \
        subquery()

    user_query = db.session.query(user_sub_query.c.owner_id, DingtalkUser). \
        outerjoin(DingtalkUser, DingtalkUser.user_id == user_sub_query.c.owner_id)

    user_query_result = user_query.all()

    if len(user_query_result) >1:
        result = {
            'error': "get user error",
            'data': {
                'message': 'we have more than one owner with a single name, please contact admin.'
            }
        }
        return jsonify(result)

    if user_query_result is None:
        result = {
            'error': "owner doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    user_id, ding_talk_user_object = user_query_result[0]

    if ding_talk_user_object is None:
        result = {
            'error': "owner's dingtalk user doesn't exist.",
            'data': {
            }
        }
        return jsonify(result)

    # query repos owned by owner
    repo_query = db.session.query(Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id). \
        subquery()

    # query watcher
    watcher_query = db.session.query(repo_query.c.repo_id, DingtalkWarnWatch). \
        filter(DingtalkWarnWatch.dingtalk_user_id == ding_talk_user_object.dingtalk_user_id). \
        filter(repo_query.c.repo_id == DingtalkWarnWatch.repo_id)

    dt_warn_watch_result = watcher_query.all()

    for (a_repo_id, a_dingtalk_warn_watch_object) in dt_warn_watch_result:
        db.session.delete(a_dingtalk_warn_watch_object)

    db.session.commit()

    return jsonify({
        'data': {
            'status': 'ok'
        }
    })
