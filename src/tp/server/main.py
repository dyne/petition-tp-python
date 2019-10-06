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

from fastapi import FastAPI
from .security import router as security_router
from .petition import router as petition_router

app = FastAPI(
    title="Sawtooth Petition API",
    description="Restful API for the Petition of the DDDC pilot project over sawtooth",
    version="0.0.1",
    redoc_url=None,
)

app.include_router(security_router)
app.include_router(petition_router, prefix="/petitions")
