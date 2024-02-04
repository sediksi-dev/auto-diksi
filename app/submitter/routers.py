from fastapi import APIRouter


router = APIRouter(prefix="/submitter", tags=["submitter"])


@router.post("/")
def read_root():
    return {
        "info": "This endpoint is not meant to be accessed directly. Please use the API documentation at /docs or /redoc."
    }
