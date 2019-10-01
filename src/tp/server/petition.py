from urllib.error import URLError

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from environs import Env
from pydantic import UrlStr
from tp.lib.sawtooth import SawtoothHelper
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED

router = APIRouter()
security = OAuth2PasswordBearer(tokenUrl="/token")
env = Env()
env.read_env()


@router.get("/keygen", tags=["Petitions"], summary="Creates a `private_key`")
async def keygen():
    sh = SawtoothHelper(None)
    return sh.private_key


@router.post(
    "/create",
    tags=["Petitions"],
    summary="Creates a new petition",
    status_code=HTTP_201_CREATED,
)
def create(
    petition_id: str,
    credential: str,
    verify: str,
    address: UrlStr = "http://localhost:8090/batches",
    private_key: str = None,
    token: str = Security(security),
):
    sh = SawtoothHelper(None, pk=private_key if private_key else None)
    sh.set_url(address)
    payload = dict(
        action="create", keys=credential, data=verify, petition_id=petition_id
    )
    try:
        sh.post(payload)
    except URLError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Sawtooth server address is not available",
        )
