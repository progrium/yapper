#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import join

setup(
    name = 'Yapper',
    version = '0.9',
    description = 'A Jabber/XMPP interface for Growl',
    author = 'Jeff Lindsay',
    author_email = 'progrium@gmail.com',
    license = 'MIT',
    url = 'http://github.com/progrium/yapper',
    
    packages = find_packages(exclude=['*.tests']),
    package_data = {'': ['templates/*']},
    data_files = [(join('twisted', 'plugins'), [join('twisted', 'plugins', 'yapper_plugin.py')])],
    zip_safe = False,
    entry_points = {'console_scripts':['yapper = yapper.manager:run'],},
    install_requires = [
        #'TwistedCore>=8.2.0',
        'py-Growl>=0.0.7',
    ],
    dependency_links = [
        'http://tmrc.mit.edu/mirror/twisted/Core/8.2/TwistedCore-8.2.0.tar.bz2',
        'http://tmrc.mit.edu/mirror/twisted/Core/8.2/TwistedWords-8.2.0.tar.bz2',
    ],

)