# from helpers.auth import auth
from fastapi import (
    APIRouter,
    # Depends,
)
from .keyword.controllers import SeederKeyword

router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    # dependencies=[Depends(auth)],
)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/generate")
def generate_seeds(keyword: str, lang_target: str, mode: str = "default"):
    seed = SeederKeyword()
    results = seed.generate(keyword, lang_target, mode)
    return results
