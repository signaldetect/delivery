from setuptools import setup

import os

APP_NAME = 'delivery'
VERSION = '0.2'
DESCRIPTION = 'OpenShift Python-3.3 / Django-1.6 Community Cartridge based ' \
              'application'
AUTHOR='signaldetect'
AUTHOR_EMAIL='signaldetect@gmail.com'

packages = [
     'Django<=1.6',
     'static3',
     'pytz',
     # 'mysql-connector-python',
     # 'pymongo',
     # 'psycopg2',
]

if ('REDISCLOUD_URL' in os.environ) and ('REDISCLOUD_PORT' in os.environ) and \
   ('REDISCLOUD_PASSWORD' in os.environ):
     packages.append('django-redis-cache')
     packages.append('hiredis')

setup(name=APP_NAME, version=VERSION, description=DESCRIPTION,
      author=AUTHOR, author_email=AUTHOR_EMAIL,
      url='https://pypi.python.org/pypi',
      install_requires=packages)
