# coding=utf-8
from flask import Blueprint

api_v3_app = Blueprint('api_v3_app', __name__, template_folder='template')

import nmp_broker.api_v3.server
import nmp_broker.api_v3.workflow
import nmp_broker.api_v3.util
import nmp_broker.api_v3.alert
