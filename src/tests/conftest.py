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

import pytest
from starlette.testclient import TestClient
from tp.server.main import app
from url64 import url64

_salt = int(time.time())


@pytest.fixture(scope="session", autouse=True)
def salt(request):
    print(f"INIT: petition_{salt}")
    return _salt


@pytest.fixture(scope="session", autouse=True)
def client(request):
    return TestClient(app)


def get_petition_name():
    u64 = url64.encode(f"petition_{_salt}")
    return f"u64:{u64}"


def get_clear_petition_name():
    return f"petition_{_salt}"


class PARAMS:
    CREATION = {
        "petition_id": get_clear_petition_name(),
        "petition_request": {
            "petition": {
                "uid": get_petition_name(),
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
    TALLY = {
        "zenroom": {
            "curve": "goldilocks",
            "encoding": "url64",
            "version": "1.0.0+68f2ba8",
            "scenario": "simple",
        },
        "Alice": {
            "credentials": {
                "s": "u64:BCXBxSbzILQoWYCBIeMYxt2-MKdLEqDIF-SmmzyXpEx6AMMutSn3PhPxBYEMfixVuQJuTe93FNfbgYFVL5RGVEZsSoLGB53zw3pWmWWOgCkPQy3D4ikjoQv3TQv_UEqmnQ",
                "h": "u64:BDokjEscxc9dE3MpPVFTKJ-WD1VRx3rcvHOyAlsQifwoukL9hQI1y9qfALfcS1_DqiCCvSg15FFev8kSW1yC-NxTuxCM5urU-PV5BeLQEKJSROntjYZfcBbm4kru7XI7UQ",
            },
            "credential_keypair": {
                "public": "u64:BE8ERC16Xsdg3PaGDwLYgEoagKWC1Eb-88aXg09qhvTv_onrHigAR5bbtFMcyWF9_xOeiY9Xvrt1lcdpWmwbKc_FThYOKj8ezwPlkZ5a75karo-d762W5EzuXw-76gI7_w",
                "private": "u64:StbYmlCs7YlIm3UmSpBoEwgdFRFaJuB2j4H10p7wRYY",
            },
        },
    }
    SIGN = {
        "zenroom": {
            "curve": "goldilocks",
            "encoding": "url64",
            "version": "1.0.0+68f2ba8",
            "scenario": "simple",
        },
        "petition_signature": {
            "uid_signature": "u64:BCXArfu1cpRB904Qu6O5ON03CUiSkwjtPhqKKn50qLQHQyJ3cJlM3J1GEFZ-Ldq7-xfM_7JL8mk6Q_SzZIRXQZbjTu_gchJYlLd4--72U4CCojBzucMOQLkXyhJ78gPSfQ",
            "proof": {
                "kappa": "u64:CleP8_tpvl8QBf1uZu1A5uipimRzsRFz7tOHXa_ncU-Ykv_iWH-Jb5kIzTM8LMm1FjqNdnB98kEfFLm7USwkL44OfHgkpv7IcON2LGoHqfQoo3uHiXLtDs4zD1yPiCKCHGYnYkdclPvHgg4G9dOkWdFzn8raEqHtBdcxvkyKv6JGQdWFXYnJNMsqj2ZjaSFQS8ujluHb8Djo6jh0Tr-iZK-H6-wsUYmYyiKjKy7JgVHCzhn0E-bN7AOKvnYCFWU6",
                "pi_v": {
                    "rr": "u64:BlEmpi82BtwfHXuM1lNgiz1pr79PTUB-G2Dg0qtKiCY",
                    "c": "u64:fqknZ5myi7XVIbyj8mOhM2Gnx8EuN0tvSqTHMzxfsVc",
                    "rm": "u64:owS8pw1ACeC60fViM7YJWuOjonbaFb8Y7xPQlJ86cO4",
                },
                "nu": "u64:BCmFLie4opeq8pywTmkEb6is9Eimey59ubwKV2VRqsKf5xD2noVk_ly4nT0VrCsSYVSMv6xe9rxclwTfj2nOqRt48Pvw-zx2_DphKvvCI1So-0oUNGNuv9KKAYkm5eFQ9g",
                "sigma_prime": {
                    "h_prime": "u64:BDoNPGMvgKMnOzYEazQtPE5uHND3j3qnQ6uEbcc7egdHVWgO5q5d2WubOjB0CzAyHVKOBvk_8S0mpR3YLwyaIAu4vQBXMUQqkoy1_Lnu_7JPXcD-iQoB-87rE9726e02HQ",
                    "s_prime": "u64:BAUfi7Wmq_RjO7CukhbdbTrH4d7F-sZvlivvCJtVzP4Jul0Dfr7yLCEELcWtsuWG6kX_XTbiRRsorEfaSLw0iI9z9iUXhomXThmWxLzvyb7lhrHOOJwD2Se9PrPODWlYkw",
                },
            },
            "uid_petition": get_petition_name(),
        },
    }
