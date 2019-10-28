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
import time

from tests.conftest import PARAMS


def get_token(client):
    r = client.post(
        "/token", data=dict(username="demo", password="demo", grant_type="password")
    )
    return r.json()["access_token"]


def test_petition_not_found(client):
    some_name = "random_fake_name_not_exists_and_puria_expects_a_404_status_code"
    r = client.get(f"/petitions/{some_name}")
    assert r.status_code == 404


def test_petition_creation(client):
    token = get_token(client)

    r = client.post(
        "/petitions",
        json=PARAMS.CREATION,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )
    assert r.status_code == 201
    assert "link" in r.json()


def test_retrieve_petition_no_server(client, salt):
    address = "http://example.com"
    r = client.get(f"/petitions/petition_{salt}?address={address}")
    assert r.status_code == 502


def test_retrieve_petition_without_tally(client, salt):
    time.sleep(3)
    print(f"petition_{salt}")
    r = client.get(f"/petitions/petition_{salt}")
    assert r.status_code == 200
    assert r.json()["petition"]
    assert r.json()["tally"] is None


def test_sign_petition(client, salt):
    token = get_token(client)
    r = client.post(
        f"/petitions/petition_{salt}/sign",
        json=PARAMS.SIGN,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 220


def test_duplicate_sign(client, salt):
    token = get_token(client)
    r = client.post(
        f"/petitions/petition_{salt}/sign",
        json=PARAMS.SIGN,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 220


def test_tally(client, salt):
    token = get_token(client)
    r = client.post(
        f"/petitions/petition_{salt}/tally",
        json=PARAMS.TALLY,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )
    assert r.status_code == 200
    assert "link" in r.json()


def test_retrieve_petition_with_tally(client, salt):
    time.sleep(2)
    r = client.get(f"/petitions/petition_{salt}")
    assert r.status_code == 200
    assert r.json()["petition"]
    assert r.json()["tally"]


def test_sign_tallied_petition(client, salt):
    token = get_token(client)
    r = client.post(
        f"/petitions/petition_{salt}/sign",
        json=PARAMS.SIGN,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200


def test_duplicate_sign_petition(client):
    assert False


def test_count_non_tallied_petition():
    assert False


def test_count_empty_petition():
    assert False


def test_count_petition():
    assert False
