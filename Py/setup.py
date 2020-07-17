#! -*- encoding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ssq',
    version='0.1',
	packages=find_packages(),
    install_requires=['selenium>=3.141.0', 'SQLAlchemy'],
    package_data={
        'Spider': ['downloader/*.json', 'downloader/geckodriver', 'SQLite/SQL/*.sql']
    },
	entry_points={
		'console_scripts': [
			'ssq = Spider.main:main'
		]
	},
    author='babybabyCloud',
    author_email='364847242@qq.com'
)
