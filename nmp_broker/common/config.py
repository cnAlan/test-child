"""
config.py

use environment var
"""
import os
import yaml


class Config(object):
    def __init__(self, config_path):
        with open(config_path) as config_file:
            config_dict = yaml.load(config_file)
            broker_config = config_dict['broker']
            self.BROKER_CONFIG = broker_config

            if 'debug' in broker_config:
                debug_config = broker_config['debug']
                if 'flask_debug' in debug_config:
                    flask_debug = debug_config['flask_debug']
                    if flask_debug is True:
                        self.DEBUG = True
                    elif flask_debug is not True:
                        self.DEBUG = False

            if 'mysql' in broker_config:
                mysql_config = broker_config['mysql']

                mysql_host = mysql_config['host']
                mysql_ip = mysql_host['ip']
                mysql_port = mysql_host['port']
                mysql_user = mysql_config['user']
                mysql_password = mysql_config['password']
                mysql_database = mysql_config['database']
                mysql_charset = mysql_config['charset']

                pool_recycle = mysql_config['pool_recycle']

                self.SQLALCHEMY_DATABASE_URI = \
                    "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
                        user=mysql_user,
                        password=mysql_password,
                        host=mysql_ip,
                        port=mysql_port,
                        database=mysql_database,
                        charset=mysql_charset
                    )

                self.SQLALCHEMY_POOL_RECYCLE = pool_recycle
                self.SQLALCHEMY_TRACK_MODIFICATIONS = False

    def load_config(self, config_path):
        pass


def load_config(config_file_path: None or str = None) -> None or Config:
    """
    load config from config_file_path. If config file_path is None,
    use environment variable NWPC_MONITOR_BROKER_CONFIG as config_file_path.

    :param config_file_path: None or config file path string.
    :return: None or a Config object.
    """
    if config_file_path is None:
        if 'NMP_BROKER_CONFIG' in os.environ:
            config_file_path = os.environ['NMP_BROKER_CONFIG']
        else:
            return None
        
    print("config file path:", config_file_path)

    config_object = Config(config_file_path)

    return config_object
