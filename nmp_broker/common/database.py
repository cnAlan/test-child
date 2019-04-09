# coding=utf-8
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import redis
from mongoengine import connect

db = SQLAlchemy(current_app)

redis_host = current_app.config['BROKER_CONFIG']['redis']['host']['ip']
redis_port = current_app.config['BROKER_CONFIG']['redis']['host']['port']
redis_client = redis.Redis(host=redis_host, port=redis_port)

mongodb_client = connect(
    current_app.config['BROKER_CONFIG']['mongodb']['collection'],
    host=current_app.config['BROKER_CONFIG']['mongodb']['host']['ip'],
    port=current_app.config['BROKER_CONFIG']['mongodb']['host']['port'])
