#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages


setup(
    name="School-Api",
    version="1.0",
    author="dairoot",
    author_email="623815825@qq.com",
    description="School SDK for Python",
    url='https://github.com/dairoot/school-api',
    packages=find_packages(),
    package_data={'school_api': ['check_code/theta.dat'], },
    include_package_data=True,

    install_requires=[
        'requests',
        'redis',
        'bs4',
        'Image'
    ],

    zip_safe=False
)
