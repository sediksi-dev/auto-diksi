# from helper.auth import auth
from fastapi import (
    APIRouter,
    # Depends,
)


router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    # dependencies=[Depends(auth)],
)


@router.get("/")
def read_root():
    return {"Hello": "World"}
