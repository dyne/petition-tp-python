<h1 align="center">
  petition-tp-python<br/>
  <sub>Petition Transaction Processor for Hyperledger Sawtooth</sub>
</h1>

<p align="center">
  <a href="https://travis-ci.com/DECODEproject/{project_name}">
    <img src="https://travis-ci.com/DECODEproject/{project_name}.svg?branch=master" alt="Build Status">
  </a>
  <a href="https://dyne.org">
    <img src="https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%9D%A4%20by-Dyne.org-blue.svg" alt="Dyne.org">
  </a>
</p>

<br><br>

This repository implements the whole [DECODEproject](https://decodeproject.eu)'s Petition Pilot over the [Sawtooth](https://sawtooth.hyperledger.org/) blockchain distributed by the Linux Foundation's [Hyperledger](https://www.hyperledger.org/) consortium.

To facilitate the creation of transaction families based on [Zenroom VM](https://zenroom.dyne.org) and the [Zencode human-friendly language for smart-contracts](https://decodeproject.eu/blog/smart-contracts-english-speaker), this TP uses the [Sawtooth SDK](https://sawtooth.hyperledger.org/docs/core/releases/latest/sdks.html) in Python and the [zenroom-py](https://github.com/DECODEproject/zenroom-py) bindings.


***
## 🐳 Docker

```bash
docker-compose up --build
```

To run a transaction

```bash
docker exec -it petition-tp petition-tx --help
```

shows you all the commands available of the little petition-tx cli interface

#### keygen
```bash
docker exec -it petition-tp petition-tx keygen FILENAME
```

#### transaction
```bash
docker exec -it petition-tp petition-tx transaction --help
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
