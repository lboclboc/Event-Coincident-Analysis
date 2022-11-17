#!/usr/bin/env python3
"""Install packackge for eca."""

from setuptools import find_packages, setup

version = {}
with open("eca/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name='Event-Coincident-Analysis',
    version=version['__version__'],
    packages=find_packages(exclude=["x.py"]),
    zip_safe=False,
    python_requires='>3.7.0',
#    install_requires=[
#        'python>=3.7',
#    ],
    entry_points={
        'console_scripts': [
            'eca=eca.__main__:main',
        ],
    },
#    package_data={'': ['static/*', 'templates/*']},
#    include_package_data=True,
)
