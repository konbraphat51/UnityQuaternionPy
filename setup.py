# -*- coding: utf-8 -*-
# Copyright (C) 2023 AnimatedWordCloud Project
# https://github.com/konbraphat51/AnimatedWordCloud
#
# Licensed under the MIT License.
"""
Setup script for PyThaiNLP.

https://github.com/PyThaiNLP/pythainlp
"""
from setuptools import find_packages, setup

readme = """
(readme here)
"""


def requirements_from_file(file_name):
    return open(file_name).read().splitlines()


setup(
    name="UnityQuaternionPy",
    version="0.1.0",
    description="Immitation of UnityEngine.Quaternion in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="konbraphat51",
    author_email="",
    url="https://github.com/konbraphat51/UnityQuaternionPy/main",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.8",
    package_data={},
    include_package_data=True,
    install_requires=requirements_from_file("requirements.txt"),
    license="MIT License",
    zip_safe=False,
    keywords=[],
    classifiers=[],
    entry_points={
        # "console_scripts": [
        # ],
    },
    project_urls={},
)
