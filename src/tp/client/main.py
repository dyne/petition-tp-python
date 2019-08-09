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
from urllib.error import URLError

import click as click
from tp.client.sawtooth import SawtoothHelper
from hashlib import sha512

sh = SawtoothHelper(None)


@click.group()
def main():
    pass


@main.command()
@click.argument("out", type=click.File("w"), default="-", required=False)
def keygen(out):
    click.secho("Private key created!", fg="green")
    click.echo(sh.private_key, file=out)


@main.command()
@click.option(
    "--credential",
    type=click.File("rb"),
    required=True,
    help="A file that contains a Credential signature",
)
@click.option(
    "--verify",
    type=click.File("rb"),
    required=True,
    help="a file that contains a Credential Issuer Verify Signature ",
)
@click.option(
    "-p",
    "--private-key",
    type=click.File("rb"),
    help="If specified loads a private key from a file else automatically a new key is generated",
)
@click.option(
    "-a",
    "--address",
    help="Rest API server address",
    default="http://localhost:8090/batches",
)
@click.argument(
    "petition-id", required=True
)  # , help="Petition unique identifier string")
def create(petition_id, credential, verify, address, private_key):
    sh.set_url(address)
    payload = dict(
        action="create",
        keys=credential.read().decode(),
        data=verify.read().decode(),
        petition_id=petition_id,
    )
    _send_command(payload)


def _generate_address(family_name, payload):
    namespace = sha512(family_name.encode("utf-8")).hexdigest()[0:6]
    petition = sha512(payload["petition_id"].encode("utf-8")).hexdigest()[-64:]
    return namespace + petition


def _send_command(payload):
    family_name = "DECODE_PETITION"
    family_version = "0.1"
    address = _generate_address(family_name, payload)
    try:
        response = sh.post(payload, family_name, family_version, address)
        click.secho(str(response), fg="green")
    except URLError:
        click.secho("ADDRESS ERROR: please double check your -a option", fg="red")


main.add_command(create)
