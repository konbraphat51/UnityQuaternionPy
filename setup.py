from setuptools import find_packages, setup
from pathlib import Path

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

#get README file
readme = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="UnityQuaternionPy",
    version="0.1.2",
    description="Immitation of UnityEngine.Quaternion in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="konbraphat51",
    author_email="konbraphat51@gmail.com",
    url="https://github.com/konbraphat51/UnityQuaternionPy",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.8",
    package_data={},
    include_package_data=True,
    install_requires=requirements_from_file("requirements.txt"),
    license="MIT License",
    zip_safe=False,
    keywords=[
        "fromscratch",
        "math",
        "quaternion",
        "geometry",
        "rotation",
        "3d",
        "game",
        "Topic :: Multimedia :: Graphics :: 3D Modeling"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Utilities",
    ],
    entry_points={
        # "console_scripts": [
        # ],
    },
    project_urls={},
)
