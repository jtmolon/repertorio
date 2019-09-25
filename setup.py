#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script for repertorio library."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["requests"]

setup(
    author="Joao Molon",
    author_email="jtmolon@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
    description="A setlist.fm API wrapper.",
    install_requires=requirements,
    license="MIT license': 'License :: OSI Approved :: MIT License",
    long_description=readme,
    include_package_data=True,
    keywords="repertorio setlist set list setlistfm setlist.fm",
    name="repertorio",
    packages=find_packages(include=["repertorio"]),
    test_suite="tests",
    url="https://github.com/jtmolon/repertorio",
    version="0.0.1",
    zip_safe=False,
)
