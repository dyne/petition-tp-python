##############################################################################
#
#    Petition TP, Transaction processor for Decode Petition over sawtooth
#    Copyright (c) 2019-TODAY Dyne.org <http://dyne.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import setuptools

setuptools.setup(
    name="petition-tp-python",
    version="0.0.1",
    author="Puria Nafisi Azizi",
    author_email="puria@dyne.org",
    description="DECODE Petition Pilot Transaction Processor for Hyperledger Sawtooth",
    long_description_content_type="text/markdown",
    url="https://github.com/DECODEproject/petition-tp-python",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "petition-tp-python = tp.main:main",
            "petition = tp.client.main:main",
        ]
    },
    setup_requires=["pytest-runner"],
    tests_require=[],
    install_requires=[
        "cbor==1.0.0",
        "zenroom==1.0.6",
        "environs==5.2.1",
        "pre-commit==1.18.0",
        "sawtooth-sdk==1.1.5",
        "sawtooth-signing==1.1.5",
    ],
    python_requires=">=3.5",
    project_urls={
        "Zenroom": "https://zenroom.dyne.org",
        "DECODE": "https://decodeproject.eu",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security",
    ],
)
