#!/usr/bin/env python
"""
run a simple nmp_broker server.
"""
import click
import os
import sys

if 'NWPC_MONITOR_PLATFORM_BASE' in os.environ:
    sys.path.append(os.environ['NWPC_MONITOR_PLATFORM_BASE'])


@click.command()
@click.option('-c', '--config-file', help='config file path')
def runserver(config_file):
    """
    DESCRIPTION
        Run nwpc monitor broker.
    """

    from nmp_broker import create_app
    app = create_app(config_file)

    app.run(
        host=app.config['BROKER_CONFIG']['host']['ip'],
        port=app.config['BROKER_CONFIG']['host']['port']
    )


if __name__ == '__main__':
    runserver()
