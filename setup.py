#!/usr/bin/env python
import setuptools
from awstool import (__author__, __license__,
                     APP_NAME, APP_VERSION, APP_DESCRIPTION)

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'boto3',
    'requests',
    'beautifulsoup4',
    'pyyaml'
]

setuptools.setup(
    name=APP_NAME,
    version=APP_VERSION,
    author=__author__,
    author_email="zhan9san@163.com",
    description=APP_DESCRIPTION,
    long_description=long_description,
    license=__license__,
    long_description_content_type="text/markdown",
    url="https://github.com/zhan9san/aws-tool",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['awstool=awstool.cli:main']},
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
