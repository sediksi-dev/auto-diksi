from helpers.auth import auth
from fastapi import APIRouter, Depends, HTTPException
from .keyword.controllers import SeederKeyword
from .schemas import (
    GenerateResponse,
    GeneratePayload,
    FindImagesResponse,
    FindImagesPayload,
    UploadPayload,
    UploadResponse,
)


router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    dependencies=[Depends(auth)],
)


@router.post("/queue")
async def queue():
    seed = SeederKeyword()
    return seed.queue()


@router.post("/generate", response_model=GenerateResponse)
async def generate_seeds(payload: GeneratePayload):
    seed = SeederKeyword()
    keyword = payload.keyword
    lang_target = payload.lang_target
    mode = payload.mode
    try:
        results = seed.generate(keyword, lang_target, mode)
        return {
            "status": "success",
            "message": "Successfully generated seed",
            "data": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Error generating seed: {e}"}


@router.post("/find-images", response_model=FindImagesResponse)
async def find_images(payload: FindImagesPayload):
    seed = SeederKeyword()
    original_articles = payload.original_articles
    try:
        results = seed.find_featured_images(original_articles)
        return {
            "status": "success",
            "message": "Successfully found image",
            "data": results,
        }
    except Exception as e:
        return {"status": "error", "message": f"Error finding images: {e}"}


@router.post("/upload", response_model=UploadResponse)
def upload(draft_id: int, payload: UploadPayload):
    seed = SeederKeyword()
    try:
        data = seed.upload(draft_id, payload)
        return {
            "status": "success",
            "message": "Successfully uploaded seed",
            "data": data,
        }
    except Exception as e:
        return {"status": "error", "message": f"Error uploading seed: {e}"}


@router.post("/run")
def run():
    seed = SeederKeyword()
    data = seed.get_keyword_id()
    draft_id = data["id"]
    keyword = data["keyword"]
    lang_target = data["language"]
    mode = data["mode"]

    seed.update_keyword_status(draft_id, "pending")
    try:
        try:
            rewrited = seed.generate(keyword, lang_target, mode)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while generating article: {e}"
            )

        try:
            original_article = rewrited.article
            images = seed.find_featured_images(original_article)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while finding images: {e}"
            )

        try:
            upload_data = UploadPayload(
                article=rewrited.model_dump(),
                image=images.model_dump(),
            )
            uploaded = seed.upload(draft_id, upload_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while uploading: {e}")

        seed.update_keyword_status(
            id=draft_id, status="published", public_url=uploaded.link
        )

        return {
            "status": "success",
            "message": "Successfully ran seeder",
            "data": uploaded,
        }

    except HTTPException as e:
        seed.update_keyword_status(id=draft_id, status="error")
        return {
            "status": "error",
            "message": f"Error while running seeder: {e}",
        }
