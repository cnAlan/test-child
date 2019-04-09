# coding: utf-8
from nmp_model.rmdb import Owner, Repo, DingtalkUser, DingtalkWarnWatch, Util
from nmp_broker.common.database import db


# mysql
def get_owner_by_name(owner_name: str):
    result = Owner.query_owner_by_owner_name(db.session, owner_name)
    if 'error' in result:
        return None

    return result['data']['owner']


def get_repos_by_owner_name(owner_name: str):
    return Repo.query_repos_by_owner_name(db.session, owner_name)


def get_repo_members_by_org_name(org_name):
    return Util.query_repo_members_by_org_name(db.session, org_name)


def get_ding_talk_warn_user_list(owner: str, repo: str) -> list:
    query = db.session.query(Owner, Repo, DingtalkUser, DingtalkWarnWatch).filter(Repo.owner_id == Owner.owner_id)\
        .filter(Repo.repo_name == repo)  \
        .filter(Owner.owner_name == owner) \
        .filter(DingtalkWarnWatch.repo_id == Repo.repo_id) \
        .filter(DingtalkWarnWatch.dingtalk_user_id == DingtalkUser.dingtalk_user_id)

    warn_to_user_list = []
    for (owner_object, repo_object, dingtalk_user_object, dingtalk_warn_watch_object) in query.all():
        userid = dingtalk_user_object.dingtalk_member_userid
        print(userid)
        warn_to_user_list.append(userid)

    return warn_to_user_list


def get_new_64bit_ticket():
    batch_id = None
    engine = db.engine
    connection = engine.connect()
    trans = connection.begin()
    try:
        connection.execute("REPLACE INTO tickets_64 (stub) VALUES ('a');")
        (batch_id,) = connection.execute('SELECT LAST_INSERT_ID() AS id').fetchone()
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    return batch_id
