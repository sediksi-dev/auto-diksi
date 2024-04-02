from helpers.auth import auth
from fastapi import (
    APIRouter,
    Depends,
)
from .keyword.controllers import SeederKeyword
from .schemas import GenerateResponse


router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    dependencies=[Depends(auth)],
)


@router.post("/crawl")
async def crawl():
    return {"crawl": "crawl"}


@router.post("/generate", response_model=GenerateResponse)
async def generate_seeds(keyword: str, lang_target: str, mode: str = "default"):
    seed = SeederKeyword()
    try:
        results = seed.generate(keyword, lang_target, mode)
        return {
            "status": "success",
            "message": "Successfully generated seed",
            "data": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Error generating seed: {e}"}


@router.post("/find-images")
async def find_images():
    return {"find_images": "find_images"}
