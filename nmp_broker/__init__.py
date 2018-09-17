# coding=utf-8
from pathlib import Path

from flask import Flask

from .common.config import load_config
from .common.routing_util import NMPBrokerApiJSONEncoder, NoStaticConverter


def create_app(config_file_path=None):

    static_folder = str(Path(Path(__file__).parent.parent, "static"))
    template_folder = str(Path(Path(__file__).parent.parent, "templates"))
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.config.from_object(load_config(config_file_path))
    app.json_encoder = NMPBrokerApiJSONEncoder
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
