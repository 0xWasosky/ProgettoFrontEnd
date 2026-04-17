import os
import base64
import hashlib
import datetime
from quart import Blueprint, request, send_from_directory, Response
from quart_rate_limiter import rate_limit

from PIL import Image

from _libs.Flask import jwt_required, create_response
from _libs.Jwt import decode_jwt

from _libs.Data import File
from core import user_db


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

AUDIO_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "audio"
)
CLASS_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "images", "classes"
)
IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "images"
)

audio = FileStorage(AUDIO_DIR)
images = FileStorage(IMAGES_DIR)


@files.route("/audio/get")
@rate_limit(20, datetime.timedelta(minutes=3))
@jwt_required
async def get_audio(payload, token):
    name = hashlib.sha1(str(payload["id"]).encode()).hexdigest() + ".mp3"

    if not os.path.isfile(os.path.join(AUDIO_DIR, name)):
        return await create_response(
            400,
            "error",
            {"message": "The user id provided is not correct, try again"},
            True,
            token,
        )

    response = await send_from_directory(AUDIO_DIR, name)
    response.headers["Cache-Control"] = "no-store"

    return response

@files.route("/audio/student", methods=["GET"])
@rate_limit(20, datetime.timedelta(minutes=3))
@jwt_required
async def get_student_audio(_, token):
    username = str(request.args.get("username", "")).strip()

    if not username:
        return await create_response(
            400,
            "error",
            {"message": "The username argument is required."},
            True,
            token,
        )

    user = await user_db.get("username", username, ["id"])
    if not user or not user.get("id"):
        return await create_response(
            404,
            "error",
            {"message": "Student not found."},
            True,
            token,
        )

    file_name = hashlib.sha1(str(user["id"]).encode()).hexdigest() + ".mp3"
    file_path = os.path.join(AUDIO_DIR, file_name)

    if not os.path.isfile(file_path):
        return await create_response(
            404,
            "error",
            {"message": "Audio not found."},
            True,
            token,
        )

    response = await send_from_directory(AUDIO_DIR, file_name)
    response.headers["Cache-Control"] = "no-store"

    return response


@files.route("/audio/add", methods=["PUT"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def add_audio(_, token):
    file_request = await request.files

    if not await File.check(request.content_length, file_request["file"].filename):

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

    if not await audio.check(name):
        await audio.add(name)


    await file_request["file"].save(os.path.join(AUDIO_DIR, name))

    return await create_response(
        200, "success", {"message": 0}, True, token
    )

#Ho solo aggiunto questo endpoit per poter caricare le foto delle classi
@files.route("/image/get", methods=["GET"])
@rate_limit(20, datetime.timedelta(minutes=3))
@jwt_required
async def get_image(payload, token):
    user = await user_db.get("id", payload["id"], ["profile_image"])

    if not user or not user.get("profile_image"):
        return await create_response(
            404,
            "error",
            {"message": "Profile image not found"},
            True,
            token,
        )

    image_bytes = base64.b64decode(user["profile_image"])

    return Response(
        image_bytes,
        mimetype="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )

#Ho fatto anche l'enpoint per poter inviare a frontend le foto delle classi
@files.route("/class-image/get", methods=["GET"])
@rate_limit(20, datetime.timedelta(minutes=3))
@jwt_required
async def get_class_image(_, token):
    class_name = str(request.args.get("class", "")).strip()

    if not class_name:
        return await create_response(
            400,
            "error",
            {"message": "The class argument is required."},
            True,
            token,
        )

    file_name = f"{class_name}.jpeg"
    file_path = os.path.join(CLASS_IMAGES_DIR, file_name)

    if not os.path.isfile(file_path):
        return await create_response(
            404,
            "error",
            {"message": "Class image not found"},
            True,
            token,
        )

    response = await send_from_directory(CLASS_IMAGES_DIR, file_name)
    response.headers["Cache-Control"] = "no-store"

    return response


@files.route("/image/add", methods=["PUT"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def add_image(_, token):
    file_request = await request.files

    if not await File.check(request.content_length, file_request["file"].filename):

        return await create_response(
            400,
            "error",
            {
                "message": "The file you provided is not up to our standars, it might be a malicious file."
            },
            True,
            token
        )

    jwt = await decode_jwt(token)

    user_id = jwt[1].get("id")
    uploaded_file = file_request["file"]

    if Image.open(uploaded_file.stream).format != "JPEG":
        return await create_response(
            400,
            "error",
            {
                "message": "The file you provided is not up to our standars, it might be a malicious file."
            },
            True,
            token,
        )

    uploaded_file.stream.seek(0)
    image_bytes = uploaded_file.stream.read()
    encoded_image = base64.b64encode(image_bytes).decode("ascii")

    name = hashlib.sha1(str(user_id).encode()).hexdigest() + ".jpeg"


    if not await images.check(name):
        await images.add(name)
    
    await user_db.update("id", user_id, "profile_image", encoded_image, "$set")

    await uploaded_file.save(os.path.join(IMAGES_DIR, name))

    return await create_response(
        200, "success", {"message": 0}, True, token
    )
