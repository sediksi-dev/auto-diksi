from fastapi import APIRouter
from .services import controller
from .schema import GetInfoResponse, GetAllPosts
from modules.wp.schema import WpEndpoint
from typing import List

router = APIRouter(prefix="/scrapper", tags=["scrapper"])


@router.get("/")
def read_root():
    return {
        "info": "This endpoint is not meant to be accessed directly. Please use the API documentation at /docs or /redoc."
    }


@router.get("/{module_name}", response_model=GetInfoResponse)
def get_bot_info(module_name: str):
    config = controller(module_name)
    return config.info


@router.get("/{module_name}/all", response_model=List[GetAllPosts])
def get_posts(module_name: str, _from: WpEndpoint, post_type: str = "posts"):
    """Get posts from source or target"""
    config = controller(module_name)
    return config.wp.get_posts(_from, post_type)
