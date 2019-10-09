<h1 align="center">
  petition-tp-python<br/>
  <sub>Petition Transaction Processor for Hyperledger Sawtooth</sub>
</h1>

<p align="center">
  <a href="https://travis-ci.com/DECODEproject/petition-tp-python">
    <img src="https://travis-ci.com/DECODEproject/petition-tp-python.svg?branch=master" alt="Build Status">
  </a>
  <a href="https://dyne.org">
    <img src="https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%9D%A4%20by-Dyne.org-blue.svg" alt="Dyne.org">
  </a>
</p>

<br><br>

This repository implements the whole [DECODEproject](https://decodeproject.eu)'s Petition Pilot over the [Sawtooth](https://sawtooth.hyperledger.org/) blockchain distributed by the Linux Foundation's [Hyperledger](https://www.hyperledger.org/) consortium.

To facilitate the creation of transaction families based on [Zenroom VM](https://zenroom.dyne.org) and the [Zencode human-friendly language for smart-contracts](https://decodeproject.eu/blog/smart-contracts-english-speaker), this TP uses the [Sawtooth SDK](https://sawtooth.hyperledger.org/docs/core/releases/latest/sdks.html) in Python and the [zenroom-py](https://github.com/DECODEproject/zenroom-py) bindings.

***
## 🐝 API server

To run the http server locally, you need an ASGI server like 
[hypercorn](https://pgjones.gitlab.io/hypercorn/) or [uvicorn](https://www.uvicorn.org/).

Also a python virtual environment with all the library dependencies is needed,
follow the following instruction to set it up:

```bash
python3 -m venv venv
```
this creates a virtual environment inside the `venv` folder

```bash
source ./venv/bin/activate
```
this activate the virtual environment you'll see a prefix `(venv)` on your PS1 prompt.
From now on the libraries you install goes into that folder and are not system
wide and doesn't mess up things.

```bash
pip install --upgrade pip
pip install -e .
```

This upgrades the `pip` (package installer for python) to the latest version,
and installs all the python dependencies for the `petition-tp-python` package.


```bash
pip install fastapi[all]
pip install hypercorn
```
This install the ASGI server into your virtual environment and 
the other needed dependencies to run the server

```bash
hypercorn src.tp.server.main:app
```
This runs the server on the `8000` port.

To see the OpenAPI (former SwaggerUI) head to http://localhost:8000/docs

### ENV
to run the middleware some variable environment are needed, or you can use a
dotenv (a file called `.env` in the root of the project) with the following
content:

```bash
export JWT_ALGORITHM=HS256
export JWT_TOKEN_SUBJECT=access
export JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
export JWT_USERNAME=demo
export JWT_PASSWORD=demo
export JWT_RANDOM_SECRET=change_me_with_a_very_long_hex_string
```

**the username and paswword are the ones used within the OpenAPI ui**

***
## 🐳 Docker

```bash
docker-compose up --build
```

To run a transaction

```bash
docker exec -it petition-tp petition --help
```

shows you all the commands available of the little `petition` CLI interface

#### CREATE
```bash
docker exec -it petition-tp petition create --help
```

#### SIGN
```bash
docker exec -it petition-tp petition sign --help
```

#### SHOW
```bash
docker exec -it petition-tp petition show --help
```

#### TALLY
```bash
docker exec -it petition-tp petition tally --help
```

#### COUNT
```bash
docker exec -it petition-tp petition count --help
```

## 🔧 Configuration

Configuration are passed along ENV variables or .dotenv files, the available
variables are:

 * `SAWTOOTH_VALIDATOR_ENDPOINT`
 * `SAWTOOTH_REST_ENDPOINT`


***
## 😍 Acknowledgements

Copyright 🄯 2019 by [Dyne.org](https://www.dyne.org) foundation, Amsterdam

Designed, written and maintained by Puria Nafisi Azizi.

<img src="https://zenroom.dyne.org/img/ec_logo.png" class="pic" alt="Project funded by the European Commission">

This project is receiving funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement nr. 732546 (DECODE).


***
## 🌐 Links

[https://zenroom.org/](https://zenroom.org/)

[https://decodeproject.eu/](https://decodeproject.eu/)

[https://dyne.org/](https://dyne.org/)


***
## 👥 Contributing

Please first take a look at the [Dyne.org - Contributor License Agreement](CONTRIBUTING.md) then

1.  🔀 [FORK IT](../../fork)
2.  Create your feature branch `git checkout -b feature/branch`
3.  Commit your changes `git commit -am 'Add some fooBar'`
4.  Push to the branch `git push origin feature/branch`
5.  Create a new Pull Request
6.  :pray: Thank you


***
## 💼 License

    Petition TP, Transaction processor for Decode Petition over sawtooth
    Copyright (c) 2019 Dyne.org foundation, Amsterdam
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
