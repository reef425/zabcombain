from setuptools import setup, find_packages
from os import path

NAME = 'zabcombain'


here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.md'),encoding='utf-8') as target:
    long_description = target.read()

setup(
    name = NAME,
    version = '1.0.2',
    license = 'LGPL',
    classifiers = [
         # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    description = 'zabbix support utitlits',
    long_description = long_description,
    url = '#',
    author = 'Reef',
    author_email = 'reef425@gmail.com',
    keywords = 'monitoring zabbix zabix api wxpython',
    packages = ['zabcombain'],
    install_requires = [
        'pyzabbix>=0.7.4',
    ],
    data_files = [('data', ['data/favicon.ico'])],
    entry_points = {
        'console_scripts':[
            'zabcombain=zabcombain:main',
        ],
        'gui_scripts':[
            'zabcombain=zabcombain:main',
        ]
    },
)
