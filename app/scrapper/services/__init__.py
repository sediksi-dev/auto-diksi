from .cuakz import cuakz
from fastapi import HTTPException


def controller(endpoint):
    if endpoint == "cuakz":
        return cuakz

    raise HTTPException(status_code=404, detail="Endpoint not found")
