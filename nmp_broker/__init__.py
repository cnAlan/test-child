# coding=utf-8
from datetime import datetime, time, timedelta, date
from pathlib import Path

from flask import Flask
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter, ValidationError

from nmp_broker.common.config import load_config


class NwpcMonitorBrokerApiJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, timedelta):
            return {'day': obj.days, 'seconds': obj.seconds}
        return JSONEncoder.default(self, obj)


class NoStaticConverter(BaseConverter):
    def to_python(self, value):
        if value == 'static':
            raise ValidationError()
        return value

    def to_url(self, value):
        return str(value)


def create_app(config_file_path=None):

    static_folder = str(Path(Path(__file__).parent.parent, "static"))
    template_folder = str(Path(Path(__file__).parent.parent, "templates"))
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.config.from_object(load_config(config_file_path))
    app.json_encoder = NwpcMonitorBrokerApiJSONEncoder
    app.url_map.converters['no_static'] = NoStaticConverter

    with app.app_context():
        import nmp_broker.common.database

        from nmp_broker.main import main_app
        app.register_blueprint(main_app, url_prefix="")

        from nmp_broker.api_v2 import api_v2_app
        app.register_blueprint(api_v2_app, url_prefix="/api/v2")

        from nmp_broker.api_v3 import api_v3_app
        app.register_blueprint(api_v3_app, url_prefix="/api/v3")

    return app
