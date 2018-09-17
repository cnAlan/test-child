# coding=utf-8

from flask import request, jsonify, json
from sqlalchemy import and_, func

from nmp_broker.common.database import db
from nmp_broker.api_v3 import api_v3_app
from nwpc_monitor.model import Repo, Owner, OrgUser, DingtalkUser, DingtalkWarnWatch


@api_v3_app.route('/workflow/repos/<owner>/<repo>/alert/dingtalk/watch/watchers')
def get_repo_warning_dingtalk_watch_users(owner: str, repo: str):
    """
    返回关注该项目的用户
    :param owner:
    :param repo:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'repo': repo,
                'warning': {
                    'type': 'dingtalk',
                    'watching_user_list': [
                        {
                            'owner_name': owner_object.owner_name,
                            'warn_watch': {
                                'start_date_time': ding_talk_warn_watch_object.start_date_time,
                                'end_date_time': ding_talk_warn_watch_object.end_date_time
                            },
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
    repo_query = db.session.query(Repo).filter(Owner.owner_name == owner).filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    repo_object = repo_query_result[0]

    watch_user_query = db.session.query(Owner, DingtalkUser, DingtalkWarnWatch). \
        filter(DingtalkWarnWatch.repo_id == repo_object.repo_id). \
        filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id). \
        filter(DingtalkUser.user_id == Owner.owner_id). \
        order_by(Owner.owner_name)
    watch_user_query_result = watch_user_query.all()

    user_list = []
    for (owner_object, ding_talk_user_object, ding_talk_warn_watch_object) in watch_user_query_result:
        an_user = {
            'owner_name': owner_object.owner_name,
            'warn_watch': {
                'start_date_time': ding_talk_warn_watch_object.start_date_time,
                'end_date_time': ding_talk_warn_watch_object.end_date_time
            },
            'is_watching': True
        }
        user_list.append(an_user)

    result = {
        'data': {
            'owner': owner,
            'repo': repo,
            'warning': {
                'type': 'dingtalk',
                'watching_user_list': user_list
            }
        }
    }

    return jsonify(result)


@api_v3_app.route('/workflow/repos/<owner>/<repo>/alert/dingtalk/watch/watchers/suggested')
def get_repo_warning_watch_suggested_user(owner: str, repo: str):
    """
    返回该项目的推荐关注用户列表
    :param owner:
    :param repo:
    :return:

        正常情况
        {
            'data': {
                'owner': owner,
                'repo': repo,
                'warning': {
                    'type': 'dingtalk',
                    'suggested_user_list': [
                        {
                            'owner_name': owner_name,
                            'is_watching': true or false

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
        filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo: {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    owner_object, repo_object = repo_query_result[0]

    suggested_user_list = []

    if owner_object.owner_type == 'user':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(DingtalkUser.user_id == owner_object.owner_id). \
            subquery()
    elif owner_object.owner_type == 'org':
        suggested_user_dingtalk_user_id_query = db.session.query(Owner.owner_name, DingtalkUser.dingtalk_user_id). \
            filter(OrgUser.org_id == owner_object.owner_id). \
            filter(OrgUser.user_id == Owner.owner_id). \
            filter(DingtalkUser.user_id == Owner.owner_id).\
            subquery()
    else:
        result = {
            'error': 'owner type {owner_type} is not supported'.format(owner_type=owner_object.owner_type)
        }
        return jsonify(result)

    suggested_user_query = db.session.query(suggested_user_dingtalk_user_id_query.c.owner_name, DingtalkWarnWatch). \
        outerjoin(DingtalkWarnWatch,
                  and_(
                    DingtalkWarnWatch.dingtalk_user_id == suggested_user_dingtalk_user_id_query.c.dingtalk_user_id,
                    DingtalkWarnWatch.repo_id == repo_object.repo_id
                  )
        ).order_by(suggested_user_dingtalk_user_id_query.c.owner_name)

    suggested_user_query_result = suggested_user_query.all()
    for (an_user_name, a_dingtalk_user) in suggested_user_query_result:
        suggested_user_list.append({
            "owner_name": an_user_name,
            "is_watching": a_dingtalk_user and True or False,
            # "warn_watch":{
            #     "start_date_time": None,
            #     "end_date_time": None
            # }
        })

    result = {
        'data': {
            'owner': owner,
            'repo': repo,
            'warning': {
                'type': 'dingtalk',
                'suggested_user_list': suggested_user_list
            }
        }
    }

    return jsonify(result)


@api_v3_app.route('/workflow/repos/<owner>/<repo>/alert/dingtalk/watch/watcher/<user>', methods=['POST'])
def create_dingtalk_watcher(owner, repo, user):
    """
    user关注owner/repo项目

    POST /repos/<owner>/<repo>/alert/dingtalk/watch/watcher/<user>

    Input: none

    Response:

    {
        'data': {
            'status': 'ok'
        }
    }

    """
    query_user_result = Owner.query_owner_by_owner_name(db.session, user)
    if 'error' in query_user_result:
        result = {
            'error': "get owner error",
            'data': {
                'message': query_user_result['error']
            }
        }
        return result
    elif query_user_result['data']['owner'] is None:
        result = {
            'error': "owner doesn't exist.",
            'data': {
            }
        }
        return result

    user_object = query_user_result['data']['owner']

    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo: {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    owner_object, repo_object = repo_query_result[0]

    # query watcher

    watcher_query = db.session.query(func.count('*'), DingtalkUser.dingtalk_user_id).\
        filter(DingtalkWarnWatch.repo_id == repo_object.repo_id).\
        filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id).\
        filter(DingtalkUser.user_id == user_object.owner_id)

    watcher_count, dt_user_id = watcher_query.first()

    # already watched
    if watcher_count > 0:
        result = {
            'data': {
                'status': 'ok',
                'message': 'already watched'
            }
        }
        return jsonify(result)

    # insert watcher
    new_watcher = DingtalkWarnWatch()
    new_watcher.repo_id = repo_object.repo_id
    new_watcher.dingtalk_user_id = dt_user_id

    db.session.add(new_watcher)
    db.session.commit()

    return jsonify({
        'data': {
            'status': 'ok'
        }
    })


@api_v3_app.route('/workflow/repos/<owner>/<repo>/alert/dingtalk/watch/watcher/<user>', methods=['DELETE'])
def delete_dingtalk_watcher(owner, repo, user):
    """
    取消user对owner/repo项目的关注

    DELETE /repos/<owner>/<repo>/alert/dingtalk/watch/watcher/<user>

    Input: none

    Response:

    {
        'data': {
            'status': 'ok'
        }
    }

    """
    user_query = db.session.query(DingtalkUser).\
        filter(Owner.owner_name == user).\
        filter(DingtalkUser.user_id == Owner.owner_id)

    dingtalk_user_result = user_query.all()

    if len(dingtalk_user_result) == 0:
        result = {
            'error':'user doesn\'t exist or user doesn\'t has a dingtalk id'
        }
        return jsonify(result)

    elif len(dingtalk_user_result) > 1:
        result = {
            'error': 'multi user or multi dingtalk id'
        }
        return jsonify(result)

    dingtalk_user_object = user_query[0]

    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo: {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    owner_object, repo_object = repo_query_result[0]

    watcher_query = db.session.query(DingtalkWarnWatch).\
        filter(DingtalkWarnWatch.repo_id == repo_object.repo_id).\
        filter(DingtalkWarnWatch.dingtalk_user_id == dingtalk_user_object.dingtalk_user_id)

    watcher_list = watcher_query.all()

    for a_watcher in watcher_list:
        db.session.delete(a_watcher)
    db.session.commit()

    result = {
        'data': {
            'status': 'ok'
        }
    }

    return jsonify(result)


@api_v3_app.route('/workflow/repos/<owner>/<repo>/alert/dingtalk/watch/watchers', methods=['POST'])
def create_dingtalk_watchers(owner, repo):
    """
    批量关注owner/repo项目

    POST /repos/<owner>/<repo>/alert/dingtalk/watch/watchers

    Input:

    {
        'users': [
            user1, user2, user3, ...
        ]
    }

    Response:

    {
        'data': {
            'status': 'ok',
            'watch_result': [
                {
                    'user': user,
                    'error': error，可选
                    'data': {
                        'status': status,
                        'message': message，可选
                    }
                }

            ]
        }
    }

    """
    users_string = request.form['users']
    users = json.loads(users_string)

    # check owner and repo
    repo_query = db.session.query(Owner, Repo). \
        filter(Owner.owner_name == owner). \
        filter(Owner.owner_id == Repo.owner_id). \
        filter(Repo.repo_name == repo)

    repo_query_result = repo_query.all()

    if len(repo_query_result) == 0:
        result = {
            'error': 'no repo: {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)
    elif len(repo_query_result) > 1:
        result = {
            'error': 'more than 1 {owner}/{repo}'.format(owner=owner, repo=repo)
        }
        return jsonify(result)

    owner_object, repo_object = repo_query_result[0]

    watch_result = []
    for user in users:
        # TODO: 2016.06.29 与create_dingtalk_watcher重复，需要优化
        # check user
        query_user_result = Owner.query_owner_by_owner_name(db.session, user)
        if 'error' in query_user_result:
            result = {
                'user': user,
                'error': "get owner error",
                'data': {
                    'message': query_user_result['error']
                }
            }
            watch_result.append(result)
            continue
        elif query_user_result['data']['owner'] is None:
            result = {
                'user': user,
                'error': "owner doesn't exist.",
                'data': {
                }
            }
            watch_result.append(result)
            continue

        user_object = query_user_result['data']['owner']

        # query watcher
        watcher_query = db.session.query(func.count('*'), DingtalkUser.dingtalk_user_id).\
            filter(DingtalkWarnWatch.repo_id == repo_object.repo_id).\
            filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id).\
            filter(DingtalkUser.user_id == user_object.owner_id)

        watcher_count, dt_user_id = watcher_query.first()

        # already watched
        if watcher_count > 0:
            result = {
                'user': user,
                'data': {
                    'status': 'ok',
                    'message': 'already watched'
                }
            }
            watch_result.append(result)
            continue

        # insert watcher
        new_watcher = DingtalkWarnWatch()
        new_watcher.repo_id = repo_object.repo_id
        new_watcher.dingtalk_user_id = dt_user_id

        db.session.add(new_watcher)
        db.session.commit()

        result = {
            'user': user,
            'data': {
                'status': 'ok'
            }
        }
        watch_result.append(result)

    result = {
        'data': {
            'status': 'ok',
            'watch_result': watch_result
        }
    }

    return jsonify(result)