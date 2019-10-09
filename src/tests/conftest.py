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
import pytest
from starlette.testclient import TestClient
from tp.server.main import app


@pytest.fixture(scope="session", autouse=True)
def client(request):
    return TestClient(app)