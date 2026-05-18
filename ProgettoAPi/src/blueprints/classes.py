
import asyncio
import hashlib
import os
import datetime
from quart import Blueprint, request
from quart_rate_limiter import rate_limit

from core import classes_db, user_db
from _libs.Flask import jwt_required, create_response

classes = Blueprint("classes", __name__, url_prefix="/class")


AUDIO_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "audio"
)
CLASS_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "images", "classes"
)
STUDENT_CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "student_credentials.txt"
)

def get_audio_file_name(user_id) -> str:
    return hashlib.sha1(str(user_id).encode()).hexdigest() + ".mp3"


def has_audio_file(user_id) -> bool:
    if user_id is None:
        return False

    return os.path.isfile(os.path.join(AUDIO_DIR, get_audio_file_name(user_id))) 

def find_username_in_credentials_file(class_name: str, full_name: str) -> str | None:
    if not os.path.isfile(STUDENT_CREDENTIALS_FILE):
        return None

    matched_username = None
    current_entry: dict[str, str] = {}

    with open(STUDENT_CREDENTIALS_FILE, encoding="utf-8") as credentials_file:
        for raw_line in credentials_file:
            line = raw_line.strip()

            if not line:
                if (
                    current_entry.get("Class") == class_name
                    and current_entry.get("Name") == full_name
                ):
                    matched_username = current_entry.get("Username")

                current_entry = {}
                continue

            if ": " not in line:
                continue

            key, value = line.split(": ", 1)
            current_entry[key] = value

    if current_entry.get("Class") == class_name and current_entry.get("Name") == full_name:
        matched_username = current_entry.get("Username")

    return matched_username


async def build_student_summary(class_name: str, student) -> dict[str, str | bool | None]:
    full_name = ""
    username = None

    if isinstance(student, dict):
        full_name = str(student.get("full_name") or student.get("name") or "").strip()
        raw_username = str(student.get("username", "")).strip()
        username = raw_username or None
    else:
        full_name = str(student).strip()

    user = None

    if username:
        user = await user_db.get("username", username, ["id", "username", "full_name"])
        if user is False:
            user = None

    if user is None and full_name:
        user = await user_db.collection.find_one(
            {"full_name": full_name, "class": class_name},
            {"_id": 0, "id": 1, "username": 1, "full_name": 1},
        )

    if user is None and full_name:
        username = find_username_in_credentials_file(class_name, full_name)
        if username:
            user = await user_db.get("username", username, ["id", "username", "full_name"])
            if user is False:
                user = None

    resolved_name = full_name
    resolved_username = username
    has_audio = False

    if user:
        resolved_name = str(user.get("full_name") or resolved_name).strip()
        resolved_username = str(user.get("username") or resolved_username or "").strip() or None
        has_audio = has_audio_file(user.get("id"))

    return {
        "name": resolved_name,
        "username": resolved_username,
        "hasAudio": has_audio,
    }

async def get_classes():
    summaries = await classes_db.get_all_summaries()

    for class_summary in summaries:
        class_name = class_summary.get("name", "")
        class_summary["hasImage"] = os.path.isfile(
            os.path.join(CLASS_IMAGES_DIR, f"{class_name}.jpeg")
        )

    return summaries


@classes.route("/getClasses", methods=["GET"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def class_endpoint(_, token):
    return await create_response(
        200,
        "success",
        {"message": {"classes": await get_classes()}},
        True,
        token,
    )


@classes.route("/getClass", methods=["GET"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def studentts_endpoint(_, token):
    name = request.args.get("class")

    if name is None:
        return await create_response(
            400,
            "error",
            {"message": "The argument name is not present in the url."},
            True,
            token,
        )

    students = await classes_db.get(name, "students")

    if students is False:
        return await create_response(
            400,
            "error",
            {"message": "The class name does not exist."},
            True,
            token,
        )

    students = students or []

    student_summaries = await asyncio.gather(
        *(build_student_summary(name, student) for student in students)
    )

    return await create_response(
        200,
        "success",
        {"message": {"students": student_summaries}},
        True,
        token,
    )
