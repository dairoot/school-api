#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name="School-Api",
    author="dairoot",
    version="1.0",
    license='MIT',
    author_email="623815825@qq.com",
    description="School SDK for Python",
    url='https://github.com/dairoot/school-api',
    packages=find_packages(),
    package_data={'school_api': ['check_code/theta.dat'], },
    include_package_data=True,
    platforms='any',
    zip_safe=False,

    install_requires=[
        'requests',
        'redis',
        'bs4',
        'Image',
        'numpy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)
