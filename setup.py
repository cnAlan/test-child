# coding=utf-8
from setuptools import setup

setup(
    name='nmp-broker',

    version='4.0',

    description='A broker for NWPC monitor platform.',
    long_description=__doc__,

    packages=['nmp_broker'],

    include_package_data=True,

    zip_safe=False,

    install_requires=[
        'click',
        'Flask',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'pymongo',
        'PyYAML',
        'redis',
        'requests',
        'SQLAlchemy'
    ]
)