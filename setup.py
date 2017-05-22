from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
try:
    import bugbuzz_service
    version = bugbuzz_service.__version__
except ImportError:
    pass

tests_require = [
    'mock',
    'webtest',
    'WSGIProxy2',
    'requests',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'pytest-capturelog',
    'pytest-mock',
]

setup(
    name='bugbuzz-service',
    version=version,
    packages=find_packages(exclude=('tests', )),
    install_requires=[
        'waitress>=0.8,<0.9',
        'pyramid_tm>=0.8,<0.9',
        'pyramid_debugtoolbar>=2.2,<2.3',
        'boto>=2.34.0,<3.0',
        'Pyramid>=1.5.2,<1.6',
        'SQLAlchemy>=0.9,<1.0',
        'zope.sqlalchemy>=0.7,<0.8',
        'transaction>=1.4,<1.5',
        'click>=3.3,<4.0',
        'pytz>=2014.10,<2015',
        'alembic>=0.7,<0.8',
        'psycopg2>=2.7,<2.8',
        'pyramid-handy>=0.1.1,<0.2',
        'dateutils',
        'paste>=2.0.1,<2.1',  # for dev translogger only
        'pubnub>=3.7.1,<3.8',
        'raven>=5.1.1,<6.0',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
    entry_points="""\
    [paste.app_factory]
    main = bugbuzz_service:main
    [console_scripts]
    bugbuzz_service = bugbuzz_service.scripts.__main__:main
    """,
)
