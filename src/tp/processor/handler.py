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
import random
import string

import cbor2
from sawtooth_sdk.processor.exceptions import InvalidTransaction, InternalError
from sawtooth_sdk.processor.handler import TransactionHandler
from tp.processor.payload import Payload, ACTION
from hashlib import sha512
from zenroom.zenroom import zencode_exec_rng

FAMILY_NAME = "DECODE_PETITION"
LOG = logging.getLogger(__name__)


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
            self.payload = Payload(transaction.payload)
            self.seed = "".join(
                random.SystemRandom().choice(string.ascii_letters + string.digits)
                for _ in range(2048)
            )
            self.make_action()
        except Exception as e:
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

    def create_petition(self):
        zencode = f"""Scenario 'coconut': "Create a new petition"
        Given that I am known as 'identifier'
        and I have my keypair
        and I have a signed credential
        and I use the verification key by 'issuer_identifier'
        When I aggregate all the verification keys
        and I generate a credential proof
        and I create a new petition '{self.payload.petition_id}'
        Then print all data
        """
        petition, _ = zencode_exec_rng(
            script=zencode,
            random_seed=bytearray(self.seed, "utf=8"),
            keys=self.payload.keys,
            data=self.payload.data,
        )
        self.save_petition_state(petition)
        LOG.debug("PETITION CREATED")

    def sign_petition(self):
        zencode = """Scenario 'coconut': "Add a signature to the petition"
        Given that I receive a signature
        and I receive a petition
        When a valid petition signature is counted
        Then print all data
        """
        petition, _ = zencode_exec_rng(
            script=zencode,
            random_seed=bytearray(self.seed, "utf=8"),
            keys=self.lookup_petition(),
            data=self.payload.data,
        )
        self.save_petition_state(petition)
        LOG.debug("PETITION SIGNED")

    def tally_petition(self):
        zencode = """Scenario 'coconut': "Close the petition, formally 'the tally'"
        Given that I am known as 'identifier'
        and I have my keypair
        and I receive a petition
        When I tally the petition
        Then print all data
        """
        petition, _ = zencode_exec_rng(
            script=zencode,
            random_seed=bytearray(self.seed, "utf=8"),
            keys=self.payload.keys,
            data=self.lookup_petition(),
        )
        self.save_petition_state(petition)
        LOG.debug("PETITION TALLIED")

    def lookup_petition(self):
        state = self.context.get_state([self.get_address()])
        try:
            return cbor2.loads(state[0].petition)
        except IndexError:
            return {}
        except:  # noqa
            raise InternalError("Failed to load petition")

    def save_petition_state(self, petition):
        state = dict(petition=json.dumps(json.loads(petition), sort_keys=True))
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
