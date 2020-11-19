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
import base64
import json
from json import JSONDecodeError
from urllib.error import URLError

import cbor2
import requests
import jwt
from fastapi import APIRouter, HTTPException, Security, Body
from fastapi.security import OAuth2PasswordBearer
from environs import Env
from jwt import PyJWTError
from pydantic import BaseModel
from requests.exceptions import ConnectionError
from tp.lib.sawtooth import SawtoothHelper
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
    HTTP_502_BAD_GATEWAY,
)
from tp.server.juicer import juice_create, juice_tally
from url64 import url64
# from zenroom.zenroom import zencode_exec

router = APIRouter()
security = OAuth2PasswordBearer(tokenUrl="/token")
env = Env()
env.read_env()
DEFAULT_SAWTOOTH_ADDRESS = env("SAWTOOTH_DEFAULT_ADDRESS", "http://localhost")


def _retrieve_petition(petition_id, address):
    sh = SawtoothHelper(None, None)
    sh.set_url(address)
    payload = dict(petition_id=petition_id)
    try:
        state = sh.get_state(payload, address)
    except (ConnectionError, JSONDecodeError):
        raise HTTPException(
            status_code=HTTP_502_BAD_GATEWAY,
            detail="Sawtooth server address is not available",
        )

    if not len(state["data"]):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Petition not Found")

    petition_object = cbor2.loads(base64.b64decode(state["data"][0]["data"]))
    petition_object["petition"] = json.loads(petition_object["petition"])
    if petition_object.get("tally", None):
        petition_object["tally"] = json.loads(petition_object["tally"])

    return petition_object


@router.get(
    "/{petition_id}",
    tags=["Petitions"],
    summary="Retrieves the petition payload by `id` and run the create contract and show the result",
    responses={
        404: {
            "content": {
                "application/json": {"example": {"detail": "Petition not Found"}}
            }
        },
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "petition": {
                            "petition": {
                                "owner": "u64:BE8ERC16Xsdg3PaGDwLYgEoagKWC1Eb-88aXg09qhvTv_onrHigAR5bbtFMcyWF9_xOeiY9Xvrt1lcdpWmwbKc_FThYOKj8ezwPlkZ5a75karo-d762W5EzuXw-76gI7_w",
                                "scores": {
                                    "neg": {"left": "u64:f38", "right": "u64:f38"},
                                    "pos": {"left": "u64:f38", "right": "u64:f38"},
                                },
                                "uid": "u64:cG9sbA",
                            },
                            "verifiers": {
                                "alpha": "u64:Ax9PWJpMePSumkm7L4n1bNaFMazOkGUNvkZe_kWXe0ZZdkkjQYd4vE6LEOW1QvVdNzb8QWFINrgaWp3e-9Qci4Ay7x0HdHxwwqGld-bLUNME1wVLBtWAAZSsAcAWAfQESYeLaDCAm9qjRV_ngYSo6L_EIRhoJExRhJfsoiA40UGksnmHdwJnih_v25SHTQ-EK7cIDyjAa6dhxUrOzNzKguR6lC2Wjf2HHpkYBFW6FEHmka-hB700X6dWA8lsrO37",
                                "beta": "u64:D0VgCzzAFJlVwbqJYNvKvoa18CWyoNBK0136o495PR91FItBdlrd81S9GG7_KxwOMsJKPJUeGOlnGH6aZ_OuIprHCWd5ij5vXhb0BDxGlN2g2FfO6c7bC_FVEPW0_8n1DJS00TwG_9a6No5-ZSrheQm24K-FeRBnJE6Hm8-Qd8wMWb6Ea-pMxc8dYecUeQA8PbESZgFBqJ2pWoBghhumDYlVBVAxA-UNeOb3-WcMIImSr93059aQUJADKzs2VywQ",
                            },
                            "zenroom": {
                                "curve": "goldilocks",
                                "encoding": "url64",
                                "scenario": "simple",
                                "version": "1.0.0+68f2ba8",
                            },
                        }
                    }
                }
            }
        },
        502: {
            "content": {
                "application/json": {
                    "example": {"detail": "Sawtooth server address is not available"}
                }
            }
        },
    },
)
async def get_one(petition_id: str, address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8008"):
    return _retrieve_petition(petition_id, address)


@router.post(
    "/",
    tags=["Petitions"],
    summary="Creates a new petition",
    status_code=HTTP_201_CREATED,
    responses={
        401: {
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            }
        },
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "link": "http://localhost:9009/batch_statuses?id=96144a0587574ffda6fdd36659a8522c8299b5b3037eb1ab0210c10e1121c5834fe901fdcfd5cbbf97c98b18193cc8e07c95c994708f22af8267452f6436d4e1"
                    }
                }
            }
        },
        502: {
            "content": {
                "application/json": {
                    "example": {"detail": "Sawtooth server address is not available"}
                }
            }
        },
    },
)
def create(
    petition_id: str = Body(...),
    petition_request: dict = Body(
        ...,
        example={
  "credential_proof": {
    "kappa": "Dqi7t2KSTl+xTzCn6Fpu4Yx9pfa8DrBnEVppVvS+5AkaTfkVrJtdbV+1zMECc4EnQp9Py4W3TZk9MyizU8HXrdnV08oc43WdBubxNNZvX4ur4xsMpxVXkLMIhxg/tYeQENo7UV94ucqYEbdC5nnhpnRn/wMtIu1eUZlC0VpriIVv6bkjugkALEMHIGrMW1eDCB8C8YwxQPuk8Qz5xi+OiJNsA41QWUM2VAVzHakyX7zT3m6oiL2sRobheKdnjJl7",
    "nu": "AlCKclBEjzz4eurdXzpoub+sF73/3RQvJjLW2Acm9nYQwjURhTnywSX4ynoFuUD3gg==",
    "pi_v": {
      "c": "OpYmwMmoswiMp/p80nl48t5/8jpXOcHDMsJcTT0cSmE=",
      "rm": "Gk5Tk8/tfZNK8G1tnX5/PdMh7MVtQVj36HMqCMnw9+g=",
      "rr": "0JJlnqZbX13y5CL6xB+niymG7o0t0SJ+H7wNAuxQ2TY="
    },
    "sigma_prime": {
      "h_prime": "Az8LmTpXk8EcQ77qiAQyTHtBsmSqLuESPFTYcW7wcXIqg3s2n1ZNA9PkN0Ayx1POhw==",
      "s_prime": "AhnnAhSOD61gCCjvL9rib030US2m4nTBiaS1j8tmj011WkCVybY7rMxqKnBpviBR/Q=="
    }
  },
  "petition": {
    "owner": "AxSggI9xzQ/RTjH2gRyFd+QHPCTqZucAihUyETUhVdJY9vohtmcGDFmEdOTHOTCeow==",
    "scores": {
      "neg": {
        "left": "f38=",
        "right": "f38="
      },
      "pos": {
        "left": "f38=",
        "right": "f38="
      }
    },
    "uid": "TW9yZV9wcml2YWN5X2Zvcl9hbGwh"
  },
  "uid": "More_privacy_for_all!",
  "verifiers": {
    "alpha": "P/0EVN5KUGszzll5GlO9yI3p1p80BaWp5UdJ/R4rrRYyxcBg93F3KKOEYJtrsJ4SBlxbo59jeWEi2WBRnBwClNI4YOD3ak2llLNp7y6NN3FbSKF6ZI1aoeD22rp/SUTTQVfT6vMtzXDHaE8KEWBnN87Gb5unt6tDj1kVhbE9scTV5G62ZpJBBB3aUTbQsDtCGWQlBWb0jImIaJ3ZndChwzUVy2DBnRC5nqVDzH8BJ5AtPO46qwo8M4EQ7dLPCv1h",
    "beta": "DxkhJCeC0LmNix2Q9XZxmHKwBv6fbYymNH6PGdvnOU6uD3NhZBbp+jA27kPon1CACigQ4IT/TpUGJwoy3M0o7l2x+mxPS6akE26kMrYARNC3fbYk6N9ugbjki8WX6uPQFheJJ1ZfSiiUQ02MFmIPTDKa0bRjXTyHak41+2SbQpPU1BYreIlIrDmzP8XrEaz0H0287Mg85L/iAXdtSpOk5qRyXm+lGa6QldyYkQ22xmNN6Ch0mIb3Ds9/e8EN1bM0"
  }
},
    ),
    verifier: dict = Body(
        ...,
        example={
  "MadHatter": {
    "verifier": {
      "alpha": "P/0EVN5KUGszzll5GlO9yI3p1p80BaWp5UdJ/R4rrRYyxcBg93F3KKOEYJtrsJ4SBlxbo59jeWEi2WBRnBwClNI4YOD3ak2llLNp7y6NN3FbSKF6ZI1aoeD22rp/SUTTQVfT6vMtzXDHaE8KEWBnN87Gb5unt6tDj1kVhbE9scTV5G62ZpJBBB3aUTbQsDtCGWQlBWb0jImIaJ3ZndChwzUVy2DBnRC5nqVDzH8BJ5AtPO46qwo8M4EQ7dLPCv1h",
      "beta": "DxkhJCeC0LmNix2Q9XZxmHKwBv6fbYymNH6PGdvnOU6uD3NhZBbp+jA27kPon1CACigQ4IT/TpUGJwoy3M0o7l2x+mxPS6akE26kMrYARNC3fbYk6N9ugbjki8WX6uPQFheJJ1ZfSiiUQ02MFmIPTDKa0bRjXTyHak41+2SbQpPU1BYreIlIrDmzP8XrEaz0H0287Mg85L/iAXdtSpOk5qRyXm+lGa6QldyYkQ22xmNN6Ch0mIb3Ds9/e8EN1bM0"
    }
  }
        },
    ),
    address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8090/batches",
    private_key: str = None,
    token: str = Security(security),
):
    _security_check(token)
    petition_id = petition_id or url64.decode(petition_request["petition"]["uid"][4:])
    payload = dict(
        action="create",
        keys=verifier,
        data=petition_request,
        placeholders=juice_create(verifier),
        petition_id=petition_id,
    )
    return _post(private_key, address, payload)


@router.post(
    "/{petition_id}/sign",
    tags=["Petitions"],
    summary="Adds a petition signature to the petition object (signs a petition)",
    status_code=HTTP_200_OK,
    responses={
        401: {
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            }
        },
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "link": "http://localhost:8090/batch_statuses?id=96144a0587574ffda6fdd36659a8522c8299b5b3037eb1ab0210c10e1121c5834fe901fdcfd5cbbf97c98b18193cc8e07c95c994708f22af8267452f6436d4e1"
                    }
                }
            }
        },
    },
)
def sign(
    petition_id: str,
    signature: dict = Body(
        ...,
        example={
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
                "uid_petition": "poll",
            },
        },
    ),
    address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8090/batches",
    private_key: str = None,
    token: str = Security(security),
):
    _security_check(token)
    payload = dict(action="sign", keys=signature, petition_id=petition_id)
    return _post(private_key, address, payload)


@router.post(
    "/{petition_id}/tally",
    tags=["Petitions"],
    summary="Tally a petition",
    status_code=HTTP_200_OK,
)
def tally_petition(
    petition_id: str,
    credentials: dict = Body(
        ...,
        example={
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
        },
    ),
    address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8090/batches",
    private_key: str = None,
    token: str = Security(security),
):
    _security_check(token)
    payload = dict(
        action="tally",
        keys=credentials,
        petition_id=petition_id,
        placeholders=juice_tally(credentials),
    )
    return _post(private_key, address, payload)


@router.post(
    "/remote_zencode_exec",
    tags=["Zencode"],
    summary="Execute generic contracts from remote urls",
    status_code=HTTP_200_OK,
)
def remote_zencode_exec(uid: str,
                 contract: str,
                 keys: str = None,
                 data: dict = Body(...),
                 address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8008/batches"):

    _contract_response = requests.get(contract, verify=False)
    if keys:
        _keys_response = requests.get(keys, verify=False)

    payload = dict(
        action="exec",
        contract=_contract_response.text,
        petition_id=uid,
        keys=_keys_response.text if keys else None,
        data=data,
    )
    return _post(None, address, payload)

@router.post(
    "/zencode_exec",
    tags=["Zencode"],
    summary="Execute generic contracts",
    status_code=HTTP_200_OK,
)
def zencode_exec(uid: str,
                 contract: str = Body(...),
                 data: dict = Body(...),
                 keys: dict = Body(...),
                 address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8008/batches"):
    payload = dict(
        action="exec",
        contract=contract,
        petition_id=uid,
        keys=keys,
        data=data,
    )
    return _post(None, address, payload)


@router.get(
    "/{petition_id}/count",
    tags=["Petitions"],
    summary="Count signatures on a tallied petition",
    status_code=HTTP_200_OK,
    responses={
        401: {
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            }
        },
        404: {
            "content": {
                "application/json": {"example": {"detail": "Petition not Found"}}
            }
        },
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "results": {"pos": 1, "neg": 0},
                        "zenroom": {
                            "curve": "goldilocks",
                            "encoding": "url64",
                            "version": "1.0.0+68f2ba8",
                            "scenario": "simple",
                        },
                    }
                }
            }
        },
    },
)
def count(
    petition_id: str,
    address: str = f"{DEFAULT_SAWTOOTH_ADDRESS}:8090",
    private_key: str = None,
    token: str = Security(security),
):
    _security_check(token)
    zencode = """Scenario coconut: count petition
Given that I have a valid 'petition'
and I have a valid 'petition tally'
When I count the petition results
Then print the 'results'
"""
    petition = _retrieve_petition(petition_id, address)
    """
    result = zencode_exec(
        script=zencode,
        data=json.dumps(petition["petition"]),
        keys=json.dumps(petition["tally"]),
    ).stdout
    return json.loads(result)
    """
    return {}


def _post(pk, address, payload):
    sh = SawtoothHelper(None, pk=pk if pk else None)
    sh.set_url(address)
    try:
        return sh.post(payload)
    except (URLError, ConnectionError):
        raise HTTPException(
            status_code=HTTP_502_BAD_GATEWAY,
            detail="Sawtooth server address is not available",
        )


def _security_check(token):
    if not _valid_token(token):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to play with this petition",
        )


def _valid_token(token):
    class TokenPayload(BaseModel):
        username: str = None
        password: str = None

    try:
        payload = jwt.decode(
            token, env("JWT_RANDOM_SECRET"), algorithms=env("JWT_ALGORITHM")
        )
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid token provided"
        )
    username = env("JWT_USERNAME")
    password = env("JWT_PASSWORD")
    if token_data.username == username and token_data.password == password:
        return True

    return False
