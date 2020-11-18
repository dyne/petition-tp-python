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
import json
import logging
import traceback
import hashlib
from json import JSONDecodeError

import cbor2
from sawtooth_sdk.processor.exceptions import InvalidTransaction, InternalError
from sawtooth_sdk.processor.handler import TransactionHandler
from tp.processor.payload import Payload, ACTION
from hashlib import sha512
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile


class ZenroomException(Exception):
    pass


FAMILY_NAME = "DECODE_PETITION"
LOG = logging.getLogger(__name__)

def zencode_exec_rng(script, random_seed, keys, data):
    with NamedTemporaryFile() as fk, NamedTemporaryFile() as fd:
        fd.write(data.encode())
        fd.seek(0)
        fk.write(keys.encode())
        fk.seek(0)
        config = f"RNGSEED=hex:{hashlib.sha512(random_seed).hexdigest()}"
        p = Popen(['zenroom', '-z', '-k', fk.name, '-a', fd.name, '-c', config], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        result = p.communicate(input=script.encode())
        LOG.error(result)
        return result[0].decode().trim()

class PetitionTransactionHandler(TransactionHandler):
    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ["1.0"]

    @property
    def namespaces(self):
        return [sha512(FAMILY_NAME.encode("utf-8")).hexdigest()[0:6]]

    def get_address(self):
        pid = sha512(self.payload.petition_id.encode("utf-8")).hexdigest()[-64:]
        return self.namespaces[0] + pid

    def apply(self, transaction, context):
        try:
            self.context = context
            self.transaction = transaction
            self.payload = Payload(transaction.payload)
            self.make_action()
        except Exception as e:
            LOG.error(traceback.format_exc())
            raise InvalidTransaction(
                "An error happened tying to process tx, see logs " + str(e)
            )

    def make_action(self):
        action = self.payload.action
        if action == ACTION.CREATE:
            self.create_petition()
        if action == ACTION.SIGN:
            self.sign_petition()
        if action == ACTION.TALLY:
            self.tally_petition()
        if action == ACTION.COUNT:
            self.count_petition()
        if action == ACTION.SHOW:
            self.lookup_petition()

    def create_petition(self):
        zencode = f"""
Scenario credential
Scenario petition: approve
    Given that I have a 'verifier' inside 'MadHatter'
    Given I have a 'credential proof'
    Given I have a 'petition'
    When I aggregate the verifiers
    When I verify the credential proof
    When I verify the new petition to be empty
    Then print the 'petition'
    Then print the 'verifiers'
    Then print the 'uid' as 'string' inside 'petition' 
        """
        try:

            result = zencode_exec_rng(
                script=self.fill_template_contracts(zencode),
                random_seed=bytearray(str(self.transaction.payload), "utf-8"),
                keys=self.payload.keys,
                data=self.payload.data,
            )
            self.save_petition_state(result)
            LOG.debug("PETITION CREATED")
        except ZenroomException as z:
            raise InvalidTransaction("-> Petition not created") from z

    def sign_petition(self):
        zencode = """Scenario coconut: aggregate petition signature
Given that I have a valid 'petition signature'
and I have a valid 'petition'
and I have a valid 'verifiers'
When the petition signature is not a duplicate
and the petition signature is just one more
and I add the signature to the petition
Then print the 'petition'
and print the 'verifiers'
        """
        try:
            petition = zencode_exec_rng(
                script=zencode,
                random_seed=bytearray(str(self.transaction.payload), "utf-8"),
                keys=self.lookup_petition(),
                data=self.payload.keys,
            )
            self.save_petition_state(petition)
            LOG.debug("PETITION SIGNED")
        except ZenroomException as z:
            raise InvalidTransaction("-> Petition not signed") from z

    def tally_petition(self):
        zencode = """Scenario coconut: tally petition
Given that I am 'identifier'
and I have my valid 'credential keypair'
and I have a valid 'petition'
When I create a petition tally
Then print all data
        """
        try:
            petition = self.lookup_petition()
            tally = zencode_exec_rng(
                script=self.fill_template_contracts(zencode),
                random_seed=bytearray(str(self.transaction.payload), "utf-8"),
                keys=self.payload.keys,
                data=petition,
            )
            LOG.debug("PETITION TALLIED")
            self.save_petition_state(petition, tally)
            LOG.info(tally)
        except ZenroomException as z:
            raise InvalidTransaction("-> Petition not tallied") from z

    def count_petition(self):
        zencode = """Scenario coconut: count petition
Given that I have a valid 'petition'
and I have a valid 'petition tally'
When I count the petition results
Then print the 'results'
            """
        try:
            petition = zencode_exec_rng(
                script=zencode,
                random_seed=bytearray(str(self.transaction.payload), "utf-8"),
                keys=self.payload.keys,
                data=self.lookup_petition(),
            )
            LOG.debug("PETITION COUNT")
            LOG.info(petition)
        except ZenroomException as z:
            raise InvalidTransaction("-> Can not count petition") from z

        return petition

    def lookup_petition(self):
        state = self.context.get_state([self.get_address()])
        try:
            return cbor2.loads(state[0].data)["petition"]
        except IndexError:
            return {}
        except JSONDecodeError:
            raise InvalidTransaction("Invalid petition object, should be a valid JSON")
        except:  # noqa
            raise InternalError("Failed to load petition")

    def save_petition_state(self, petition, tally=None):
        try:
            state = dict(
                petition=json.dumps(json.loads(petition), sort_keys=True), tally=tally
            )
        except JSONDecodeError:
            raise InvalidTransaction("Invalid petition object, should be a valid JSON")
        self.save_state(state)

    def save_state(self, state):
        encoded_state = cbor2.dumps(state)
        state = {self.get_address(): encoded_state}
        LOG.debug(
            f"Saving state with context_id [{self.payload.petition_id}] as : {state}"
        )
        try:
            self.context.set_state(state)
        except Exception:
            raise InvalidTransaction("State error")

    def fill_template_contracts(self, template):
        for k, v in self.payload.placeholders:
            template = template.replace(f"'{k}'", f"'{v}'")
        return template
