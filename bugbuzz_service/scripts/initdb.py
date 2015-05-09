from __future__ import unicode_literals
import os

import click
from alembic import command
from alembic.config import Config

from bugbuzz_service.db.tables import metadata
from bugbuzz_service.models import setup_database
from . import subcommand


@subcommand
@click.command('initdb', short_help='initialize database')
@click.option('--upgrade/--no-upgrade', default=True)
@click.pass_context
def cli(ctx, upgrade):
    settings = ctx.obj['settings']
    settings = setup_database({}, **settings)
    engine = settings['engine']

    import bugbuzz_service
    base_dir = os.path.dirname(os.path.dirname(bugbuzz_service.__file__))
    alembic_dir = os.path.join(base_dir, 'alembic')

    alembic_cfg = Config()
    alembic_cfg.set_main_option(
        'script_location',
        os.environ.get('ALEMBIC_DIR', alembic_dir),
    )
    alembic_cfg.set_main_option('sqlalchemy.url', settings['sqlalchemy.url'])

    if engine.name == 'postgresql':
        alembic_version = engine.execute(
            "SELECT relname FROM "
            "pg_class AS c JOIN pg_namespace AS n ON n.oid=c.relnamespace "
            "WHERE n.nspname=current_schema() AND relname = 'alembic_version'"
        ).scalar()
        # we have no alembic stamp, create it
        if alembic_version is None:
            click.echo('Add alembic stamp to head ...')
            command.stamp(alembic_cfg, 'head')
        # we already have alembic stamp in database, and we want to upgrade
        elif upgrade:
            click.echo('Upgrading database to head')
            command.upgrade(alembic_cfg, 'head')

    metadata.create_all(engine)
    click.echo('Done')
