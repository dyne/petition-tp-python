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
from sawtooth_sdk.processor.handler import TransactionHandler
from tp.processor.petition_payload import Payload, ACTION


class PetitionTransactionHandler(TransactionHandler):

    NAMESPACE = "DECODE_PETITION"

    @property
    def family_name(self):
        return self.NAMESPACE

    @property
    def family_versions(self):
        return ["0.1", "1.0"]

    @property
    def namespaces(self):
        return [self.NAMESPACE]

    def apply(self, transaction, context):
        self.payload = Payload(transaction.payload)
        self.make_action()

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
        print("PETITION COUNTED")

    def create_petition(self):
        print("PETITION CREATED")

    def sign_petition(self):
        print("PETITION SIGNED")

    def show_petition(self):
        print("PETITION SHOW")

    def tally_petition(self):
        print("PETITION TALLY")
