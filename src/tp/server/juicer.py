#  Petition TP, Transaction processor for Decode Petition over sawtooth
#  Copyright (c) 2019. Dyne.org <http://dyne.org>
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


def juice_create(verifier):
    verifier_name = list(verifier.keys())
    verifier_name.remove("zenroom")

    return dict(verifier_name=verifier_name[0])


def juice_sign(signature):
    petition_signature = list(signature.keys())
    petition_signature.remove("zenroom")
    return dict(petition_signature=petition_signature[0])


def juice_tally(credentials):
    identifier = list(credentials.keys())
    identifier.remove("zenroom")
    return dict(identifier=identifier[0])
