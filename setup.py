#!/usr/bin/env python
from setuptools import setup, find_packages
#from CiscoAutomationFramework import __version__

__version__ = '1.0.0'

description = '''The CiscoAutomationFramework is designed to be an interface for network engineers to 
issue commands and retrieve output from Cisco devices regardless of firmware so they can easily build automation 
scripts atop the framework and dont have to worry about the nuances of CLI scraping.'''


setup(
    name='CiscoAutomationFramework',
    version=__version__,
    packages=find_packages(),
    keywords='cisco automation framework network',
    url='https://github.com/superadm1n/CiscoAutomationFramework',
    license='Apache 2.0',
    author='Kyle Kowalczyk',
    author_email='kowalkyl@gmail.com',
    description='Framework for issuing commands and retrieving consistent data on Cisco devices',
    long_description=description,
    install_requires=['paramiko', 'pyserial==3.4'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9'
    ]
)
