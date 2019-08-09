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
import logging

import cbor2
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler
from tp.processor.payload import Payload, ACTION
from hashlib import sha512

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
            self.payload = Payload(transaction.payload)
            self.make_action()
            self.save_state(context)
        except Exception as e:
            LOG.debug("Exception saving state", str(e))
            raise InvalidTransaction(
                "An error happened tying to process tx, see logs " + str(e)
            )

    def make_action(self):
        action = self.payload.action
        if action == ACTION.COUNT:
            self.count_petition()
        if action == ACTION.CREATE:
            self.create_petition()
        if action == ACTION.SIGN:
            self.sign_petition()
        if action == ACTION.SHOW:
            self.show_petition()
        if action == ACTION.TALLY:
            self.tally_petition()

    def count_petition(self):
        LOG.error("PETITION COUNTED")

    def create_petition(self):
        LOG.debug("PETITION CREATED")

    def sign_petition(self):
        LOG.error("PETITION SIGNED")

    def show_petition(self):
        LOG.error("PETITION SHOW")

    def tally_petition(self):
        LOG.error("PETITION TALLY")

    def save_state(self, context):
        state = dict(action=self.payload.action)
        encoded_state = cbor2.dumps(state)

        state = {self.get_address(): encoded_state}
        LOG.debug(
            f"Saving state with context_id [{self.payload.petition_id}] as : {state}"
        )
        try:
            context.set_state(state)
        except Exception:
            raise InvalidTransaction("State error")
