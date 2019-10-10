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

salt = int(time.time())


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
    params = {
        "petition_id": "petition_test_%s" % salt,
        "petition_request": {
            "petition": {
                "uid": "u64:cG9sbA",
                "scores": {
                    "pos": {"right": "u64:f38", "left": "u64:f38"},
                    "neg": {"right": "u64:f38", "left": "u64:f38"},
                },
                "owner": "u64:BE8ERC16Xsdg3PaGDwLYgEoagKWC1Eb-88aXg09qhvTv_onrHigAR5bbtFMcyWF9_xOeiY9Xvrt1lcdpWmwbKc_FThYOKj8ezwPlkZ5a75karo-d762W5EzuXw-76gI7_w",
            },
            "zenroom": {
                "curve": "goldilocks",
                "encoding": "url64",
                "version": "1.0.0+68f2ba8",
                "scenario": "simple",
            },
            "credentials": {
                "s": "u64:BCXBxSbzILQoWYCBIeMYxt2-MKdLEqDIF-SmmzyXpEx6AMMutSn3PhPxBYEMfixVuQJuTe93FNfbgYFVL5RGVEZsSoLGB53zw3pWmWWOgCkPQy3D4ikjoQv3TQv_UEqmnQ",
                "h": "u64:BDokjEscxc9dE3MpPVFTKJ-WD1VRx3rcvHOyAlsQifwoukL9hQI1y9qfALfcS1_DqiCCvSg15FFev8kSW1yC-NxTuxCM5urU-PV5BeLQEKJSROntjYZfcBbm4kru7XI7UQ",
            },
            "credential_proof": {
                "kappa": "u64:FKbtHuq3lBqH7Qr_HgBLf4PrIkXDwl5QCahvHgxqssUoqWvcXhp3V1SNz8kN-U-iQPCivZvUVWIj-Dfl43yhvkxPxc3VqDSvUbkOEQMtMH2dvRpU3fXfBjoAcfYzTQGfMFrf8Gs6NX5P317pArTLRsT14VUUxh76TTli8rWGcHMiG3mwV6GxKaEW8zM3NtFTM52jrgUQxJUG2Fvm_PnOsuOMhCdX-Eet_uWOhaDSMbsAnJRoymjddQFTW0QOM2Yh",
                "pi_v": {
                    "rr": "u64:K9RdTZeP7EzbnguKY3bP2CbwuF18t2Nbdo71Ae42sTQ",
                    "rm": "u64:cmkbep4En-aqkRRUzOjHq15-Sk4mmiLvAZCVPcPpxRE",
                    "c": "u64:YFZFP-EBf2i-jfvjIWC4L76ca8tzF2QKGRcuVJe7zXQ",
                },
                "nu": "u64:BAhaW8309GkhbXBJ9KEH10SZYLkDXPWzbzKeRlOi-CDpPLc2wSM2jWzQsCKSv2GJzR5dmZajZTco9XmEQUS_2wpzUYjB0f24i3lRegAn_0fkwQlk5yzHWVGn8e8CrHmlPw",
                "sigma_prime": {
                    "h_prime": "u64:BAQWfg5tgd-D0J8_5by15W-Uv5ORlMEV7WZ6s-qXtN47S-zmVpCWTLTu_2Kh16ckTDi2znDak_-M3qlD1CFaEMXE2UBIfSVS18sTwIx3td_DGblt0_1HGZS2LjPYwnQU2A",
                    "s_prime": "u64:BFF0DoQivP5lY5pPtywrR_JAUVTTxO83o4ZhiUw6fKy5TeKUSlv9T2Mr44pzVP3QhS5xANN49tw_LAI7qT1gyolCzorzrZS1J5YITDzVtYUtm_G3BCo3T-o2x7hJ_kEXFg",
                },
            },
            "verifier": {
                "MadHatter": {
                    "alpha": "u64:Ax9PWJpMePSumkm7L4n1bNaFMazOkGUNvkZe_kWXe0ZZdkkjQYd4vE6LEOW1QvVdNzb8QWFINrgaWp3e-9Qci4Ay7x0HdHxwwqGld-bLUNME1wVLBtWAAZSsAcAWAfQESYeLaDCAm9qjRV_ngYSo6L_EIRhoJExRhJfsoiA40UGksnmHdwJnih_v25SHTQ-EK7cIDyjAa6dhxUrOzNzKguR6lC2Wjf2HHpkYBFW6FEHmka-hB700X6dWA8lsrO37",
                    "beta": "u64:D0VgCzzAFJlVwbqJYNvKvoa18CWyoNBK0136o495PR91FItBdlrd81S9GG7_KxwOMsJKPJUeGOlnGH6aZ_OuIprHCWd5ij5vXhb0BDxGlN2g2FfO6c7bC_FVEPW0_8n1DJS00TwG_9a6No5-ZSrheQm24K-FeRBnJE6Hm8-Qd8wMWb6Ea-pMxc8dYecUeQA8PbESZgFBqJ2pWoBghhumDYlVBVAxA-UNeOb3-WcMIImSr93059aQUJADKzs2VywQ",
                }
            },
            "verifiers": {
                "alpha": "u64:Ax9PWJpMePSumkm7L4n1bNaFMazOkGUNvkZe_kWXe0ZZdkkjQYd4vE6LEOW1QvVdNzb8QWFINrgaWp3e-9Qci4Ay7x0HdHxwwqGld-bLUNME1wVLBtWAAZSsAcAWAfQESYeLaDCAm9qjRV_ngYSo6L_EIRhoJExRhJfsoiA40UGksnmHdwJnih_v25SHTQ-EK7cIDyjAa6dhxUrOzNzKguR6lC2Wjf2HHpkYBFW6FEHmka-hB700X6dWA8lsrO37",
                "beta": "u64:D0VgCzzAFJlVwbqJYNvKvoa18CWyoNBK0136o495PR91FItBdlrd81S9GG7_KxwOMsJKPJUeGOlnGH6aZ_OuIprHCWd5ij5vXhb0BDxGlN2g2FfO6c7bC_FVEPW0_8n1DJS00TwG_9a6No5-ZSrheQm24K-FeRBnJE6Hm8-Qd8wMWb6Ea-pMxc8dYecUeQA8PbESZgFBqJ2pWoBghhumDYlVBVAxA-UNeOb3-WcMIImSr93059aQUJADKzs2VywQ",
            },
            "credential_keypair": {
                "public": "u64:BE8ERC16Xsdg3PaGDwLYgEoagKWC1Eb-88aXg09qhvTv_onrHigAR5bbtFMcyWF9_xOeiY9Xvrt1lcdpWmwbKc_FThYOKj8ezwPlkZ5a75karo-d762W5EzuXw-76gI7_w",
                "private": "u64:StbYmlCs7YlIm3UmSpBoEwgdFRFaJuB2j4H10p7wRYY",
            },
        },
        "verifier": {
            "zenroom": {
                "curve": "goldilocks",
                "encoding": "url64",
                "version": "1.0.0+68f2ba8",
                "scenario": "simple",
            },
            "MadHatter": {
                "verifier": {
                    "alpha": "u64:Ax9PWJpMePSumkm7L4n1bNaFMazOkGUNvkZe_kWXe0ZZdkkjQYd4vE6LEOW1QvVdNzb8QWFINrgaWp3e-9Qci4Ay7x0HdHxwwqGld-bLUNME1wVLBtWAAZSsAcAWAfQESYeLaDCAm9qjRV_ngYSo6L_EIRhoJExRhJfsoiA40UGksnmHdwJnih_v25SHTQ-EK7cIDyjAa6dhxUrOzNzKguR6lC2Wjf2HHpkYBFW6FEHmka-hB700X6dWA8lsrO37",
                    "beta": "u64:D0VgCzzAFJlVwbqJYNvKvoa18CWyoNBK0136o495PR91FItBdlrd81S9GG7_KxwOMsJKPJUeGOlnGH6aZ_OuIprHCWd5ij5vXhb0BDxGlN2g2FfO6c7bC_FVEPW0_8n1DJS00TwG_9a6No5-ZSrheQm24K-FeRBnJE6Hm8-Qd8wMWb6Ea-pMxc8dYecUeQA8PbESZgFBqJ2pWoBghhumDYlVBVAxA-UNeOb3-WcMIImSr93059aQUJADKzs2VywQ",
                }
            },
        },
    }
    r = client.post(
        "/petitions",
        json=params,
        headers={"Authorization": f"Bearer {token}"},
        allow_redirects=True,
    )
    assert r.status_code == 201
    assert "link" in r.json()


def test_retrieve_petition_no_server(client):
    address = "http://example.com"
    r = client.get(f"/petitions/petition_test_{salt}?address={address}")
    assert r.status_code == 502


def test_retrieve_petition(client):
    print(f"petition_test_{salt}")
    r = client.get(f"/petitions/petition_test_{salt}")
    assert r.status_code == 200
    assert r.json()["petition"]
    assert r.json()["tally"]
