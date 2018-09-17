# coding=utf-8
from nmp_broker.main import main_app
from nmp_broker.common.data_store import get_owner_by_name

from flask import jsonify,render_template, abort


@main_app.route('/')
def get_index_page():
    return render_template("index.html")


@main_app.route('/<owner>')
@main_app.route('/orgs/<owner>/<path:path>')
def get_owner_page(owner, path=None):
    owner_object = get_owner_by_name(owner)

    if owner_object is None:
        return abort(404)

    if owner_object.owner_type == "org":
        return get_org_page(owner)
    elif owner_object.owner_type == "user":
        return get_user_page(owner, path=path)
    else:
        result = {'error':'wrong'}
        return jsonify(result)


def get_user_page(user, path=None):
    return render_template("user.html", user=user)


def get_org_page(org):
    return render_template("organization.html", org=org)


@main_app.route('/<owner>/<repo>')
@main_app.route('/<owner>/<repo>/')
def get_repo_page(owner, repo):
    return render_template('repo.html', owner=owner, repo=repo)


@main_app.route('/<no_static:owner>/<repo>/<path:path>')
def get_repo_path_page(owner, repo, path):
    return render_template('repo.html', owner=owner, repo=repo, path=path)
