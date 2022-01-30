#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import setuptools
import runpy

version_meta = runpy.run_path("./inclusivewriting/version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inclusivewriting",
    version=VERSION,
    author="John Samuel",
    author_email="johnsamuelwrites@example.com",
    description="Python multilingual application for inclusive writing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsamuelwrites/inclusive",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={'inclusivewriting': 'inclusivewriting'},
    package_data = {"inclusivewriting": ["configuration.json", "resources/*/*.json", 
        "locales/*", "locales/*/*", "locales/*/*/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License" +
        " v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'rich>=10.9.0',
        'typer>=0.3.2',
        'babel>=2.9.1'
    ],
    python_requires='>=3.7',
)
