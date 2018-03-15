# coding=utf-8
# Created by OhBonsai at 2018/3/8
import sys

from setuptools import find_packages
from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

sketch_version = '20180315'

sketch_description = (
    'Ultimate Morphology Flask Boilerplate :) '
    'Enjoy it')


def check_before_upload():
    """Warn something is not present or is not recent.

    Raises:
    UserWarning
    """
    if None:
        raise UserWarning(
            "Build the frontend before uploading to PyPI!"
            + " (see docs/Developers-Guide.md)"
        )


if 'upload' in sys.argv:
    check_before_upload()

setup(
    name='sketch',
    version=sketch_version,
    description='flask boilerplate',
    long_description=sketch_description,
    license='Apache License, Version 2.0',
    maintainer='OhBonsai',
    maintainer_email='letbonsaibe@gmail.com',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Operating System :: Linux',
        'Programming Language :: Python',
    ],
    data_files=[('share/sketch', ['sketch.conf'])],
    packages=find_packages(),
    include_package_data=True,
    package_data={},
    zip_safe=False,
    scripts=['sktctl'],
    install_requires=[str(req.req) for req in parse_requirements(
        "requirements.txt", session=PipSession(),
    )],
)

