from setuptools import setup, find_packages

import os

# Put here required packages
packages = ['Django==1.11.2',
            'static3',  # serve static files in the server
            'djangorestframework==3.6.3',
            'django-filter==1.0.4',
            'Markdown',
            'MySQL-python']

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    packages.append('django-redis-cache')
    packages.append('hiredis')

setup(name='MantidReports',
      version='1.0',
      description='RESTful services relatd to mantid',
      author='P.F.Peterson',
      author_email='petersonpr@ornl.gov',
      url='http://www.mantidproject.org',
      install_requires=packages,
      packages=find_packages(),
      include_package_data=True,
      )
