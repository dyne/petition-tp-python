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
    entry_points={
        "console_scripts": [
            "petition-tp-python = tp.processor.main:main",
            "petition = tp.client.main:main",
        ]
    },
    install_requires=[
        "click==7.0",
        "cbor2==4.1.2",
        #        "zenroom==1.0.6",
        "environs==5.2.1",
        "pre-commit==1.18.0",
        "sawtooth-sdk==1.1.5",
        "sawtooth-signing==1.1.5",
    ],
    python_requires=">=3.5",
)
