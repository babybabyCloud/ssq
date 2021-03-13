#! -*- encoding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ssq',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'httpx==0.17.0',
        'SQLAlchemy==1.3.20', 
        'click==7.1.2',
        'pandas==1.1.3',
        'beautifulsoup==4.9.3'
    ],
    package_data={
        'Spider': [
            'logging.json', 
            'downloader/geckodriver'
        ]
    },
	entry_points={
		'console_scripts': [
			'ssq = Spider.main:main'
		]
	},
    author='babybabyCloud',
    author_email='364847242@qq.com'
)
