from __future__ import unicode_literals

from pyramid.config import Configurator

from .models import setup_database
from .settings import default_settings


__version__ = '0.0.0'
__git_revision__ = 'Unknown'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.

    """
    app_settings = default_settings.copy()
    app_settings.update(settings)

    # setup database
    app_settings = setup_database(global_config, **app_settings)
    config = Configurator(
        settings=app_settings,
    )
    config.add_tween('pyramid_handy.tweens.allow_origin_tween_factory')
    config.add_tween('pyramid_handy.tweens.api_headers_tween_factory')
    config.add_tween('pyramid_handy.tweens.basic_auth_tween_factory')
    config.include('.renderers')
    config.include('.api')

    config.scan(categories=('pyramid', ))
    return config.make_wsgi_app()
