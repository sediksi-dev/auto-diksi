import argparse
import os
import uuid


def init_modules(module_name):
    directories = ["models", "routers", "services"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
        create_module(module_name)


def delete_modules(module_name):
    directories = ["models", "routers", "services"]
    id = uuid.uuid4()
    # check if .trash folder exists
    if not os.path.exists(".trash"):
        os.makedirs(".trash")

    for directory in directories:
        if os.path.exists(f"app/{directory}/{module_name}.py"):
            # create confirmation message to delete the file
            print(f"Delete app/{directory}/{module_name}.py")
            # move file to .trash folder
            os.rename(
                f"app/{directory}/{module_name}.py",
                f".trash/{directory}-{module_name}-{id}.py",
            )


def create_module(module_name):
    directories = ["models", "routers", "services"]
    switcher = {
        "models": create_model,
        "routers": create_router,
        "services": create_service,
    }

    for directory in directories:
        if not os.path.exists(f"app/{directory}"):
            os.makedirs(f"app/{directory}")

        # check if file exists
        if os.path.exists(f"app/{directory}/{module_name}.py"):
            print(f"File app/{directory}/{module_name}.py already exists")
            continue

        with open(f"app/{directory}/{module_name}.py", "w") as f:
            f.write(switcher[directory](module_name))


def create_router(module_name: str):
    prefix = module_name.replace("_", "-")
    classes = "".join([x.capitalize() for x in module_name.split("_")])
    return f"""# Router handlers for api/{prefix} endpoint
from fastapi import APIRouter
from app.services.{module_name} import getAll
from app.models.{module_name} import {classes}


router = APIRouter(prefix="/{prefix}")


@router.get("/", response_model=list[{classes}])  # /api/{module_name}
def get_{module_name}():
    return getAll()
"""


def create_service(module_name):
    classes = "".join([x.capitalize() for x in module_name.split("_")])
    return f"""# Business logic for {module_name}
# Import some external modules here
from app.models.{module_name} import {classes}


def getAll():
    responses: list[{classes}] = [
        {classes}(id=1),
    ]
    return responses
"""


def create_model(module_name):
    classes = "".join([x.capitalize() for x in module_name.split("_")])
    return f"""# Models definition for users
from pydantic import BaseModel


class {classes}(BaseModel):
    id: int
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI untuk mengelola proyek Python")
    parser.add_argument(
        "command", choices=["create", "delete"], help="Perintah yang akan dijalankan"
    )
    parser.add_argument("module", help="Nama modul")

    args = parser.parse_args()

    if args.command == "create":
        init_modules(args.module)
    elif args.command == "delete":
        delete_modules(args.module)
