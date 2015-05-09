from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
try:
    import gf_world
    version = gf_world.__version__
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
    name='bugbuzz-api',
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
        'psycopg2>=2.6,<2.7',
        'pyramid-handy>=0.1.1,<0.2',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
    entry_points="""\
    [paste.app_factory]
    main = bugbuzz_api:main
    [console_scripts]
    bbapi = bugbuzz_api.scripts.__main__:main
    """,
)
