import click
from flask import Blueprint

from .integrations.aws import import_aws_data

integrations = Blueprint('integrations', __name__)

@integrations.cli.command('update')
@click.argument('name')
def update(name):
    """ Downloads latest data from cloud provider """
    print("Downloading latest {} data".format(name))
    if name == 'aws':
        import_aws_data()