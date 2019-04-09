# coding: utf-8
from datetime import datetime, time, timedelta, date

from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter, ValidationError
from bson import ObjectId


class NMPBrokerApiJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, timedelta):
            return {'day': obj.days, 'seconds': obj.seconds}
        elif isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)


class NoStaticConverter(BaseConverter):
    def to_python(self, value):
        if value == 'static':
            raise ValidationError()
        return value

    def to_url(self, value):
        return str(value)
