import os
import hashlib
import datetime
from quart import Blueprint, request, send_from_directory
from quart_rate_limiter import rate_limit

from _libs.Flask import jwt_required, create_response
from _libs.Jwt import decode_jwt

from _libs.Data import File


class FileStorage:
    def __init__(self, dir_name: str) -> None:
        self.dir_name = dir_name

        self.dir_content = os.listdir(dir_name)

    async def check(self, name: str) -> bool:
        return name in self.dir_content

    async def add(self, name):
        if not name in self.dir_content:
            self.dir_content.append(name)

        return True


files = Blueprint("files", __name__, url_prefix="/files")

file_storage = FileStorage("./files")


@files.route("/get")
@rate_limit(20, datetime.timedelta(minutes=3))
@jwt_required
async def file_endpoint(payload, token):
    name = hashlib.sha1(str(payload["id"]).encode()).hexdigest() + ".mp3"

    if not await file_storage.check(name):
        return await create_response(
            400,
            "error",
            {"message": "The user id provided is not correct, try again"},
            True,
            token,
        )

    return await send_from_directory("./files", name)


@files.route("/add", methods=["PUT"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def add_endpoint(_, token):
    file_request = await request.files

    if not await File.check(
        request.content_type, request.content_length, file_request["file"].filename
    ):

        return await create_response(
            400,
            "error",
            {
                "message": "The file you provided is not up to our standars, it might be a malicious file."
            },
            True,
            request.cookies.get("token"),
        )

    jwt = await decode_jwt(token)

    user_id = jwt[1].get("id")

    name = hashlib.sha1(str(user_id).encode()).hexdigest() + ".mp3"

    if not await file_storage.check(name):
        await file_request["file"].save(f"./files/{name}")
        await file_storage.add(name)

    return await create_response(
        200, "success", {"message": 0}, True, request.cookies.get("token")
    )
