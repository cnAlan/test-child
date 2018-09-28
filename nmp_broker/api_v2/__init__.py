# coding=utf-8
from flask import Blueprint

api_v2_app = Blueprint('api_v2_app', __name__, template_folder='template')

import nmp_broker.api_v2.api_org
import nmp_broker.api_v2.api_repo
import nmp_broker.api_v2.api_hpc
import nmp_broker.api_v2.api_nofitication
import nmp_broker.api_v2.api_workflow
