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
#

from datetime import datetime, timedelta

import jwt
from environs import Env
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()
env = Env()
env.read_env()
with env.prefixed("JWT_"):
    algorithm = env("ALGORITHM")
    subject = env("TOKEN_SUBJECT")
    expiry = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
    username = env("USERNAME")
    password = env("PASSWORD")
    secret = env("RANDOM_SECRET")


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:  # pragma: no cover
        expire = datetime.utcnow() + timedelta(minutes=expiry)

    to_encode.update({"exp": expire, "sub": subject})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def auth(u, p):
    if u == username and p == password:
        return True
    return False


@router.post(
    "/token",
    tags=["API auth"],
    summary="Obtain OAuth2/Bearer token for protected API calls",
)
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not auth(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=expiry)
    access_token = create_access_token(
        data={"username": form_data.username, "password": form_data.password},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
