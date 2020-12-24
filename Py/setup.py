#! -*- encoding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ssq',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'selenium==3.141.0', 
        'SQLAlchemy==1.3.20', 
        'click==7.1.2',
        'pandas==1.1.3'
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
