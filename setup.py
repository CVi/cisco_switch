__author__ = 'CVi'

from setuptools import setup
import sys

if sys.version_info < (3, 0):
    raise Exception("cisco_switch requires Python 3.0 or higher.")

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cisco_switch',
      version='0.1.1',
      description='Manage a Cisco switch trough SNMP',
      long_description=readme(),
      url='http://github.com/chrivi/cisco_switch',
      author='Christoffer Viken',
      author_email='christoffer@viken.me',
      license='BSD',
      packages=['cisco_switch'],
      zip_safe=False,
      setup_requires=['pysnmp', 'pysnmp-mibs', 'pyasn1'])