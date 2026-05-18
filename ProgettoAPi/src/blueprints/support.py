import asyncio
import datetime
import os
import secrets
from quart import Blueprint, request
from quart_rate_limiter import rate_limit

from _libs.Flask import jwt_required, create_response

from core import classes_db, user_db, ADMIN_PWD_HASH, IMAGE_PWD_HASH

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from PIL import Image


admin = Blueprint("admin", __name__, url_prefix="/admin")


id = 1000
CLASS_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "images", "classes"
)
STUDENT_CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "files", "student_credentials.txt"
)
credentials_file_lock = asyncio.Lock()
access_password_hasher = PasswordHasher()

#Questa è la funzione "Incriminata" che facilita attacchi hacker potremmo
#Ti prego dammi dei consigli su cosa fare perché ora non ho proprio idea
def append_student_credentials(entry: dict[str, str]) -> None:
    os.makedirs(os.path.dirname(STUDENT_CREDENTIALS_FILE), exist_ok=True)

    with open(STUDENT_CREDENTIALS_FILE, "a", encoding="utf-8") as credentials_file:
        credentials_file.write(
            "\n".join(
                [
                    f"[{datetime.datetime.now().isoformat(timespec='seconds')}]",
                    f"Name: {entry['full_name']}",
                    f"Class: {entry['class']}",
                    f"Username: {entry['username']}",
                    f"Password: {entry['password']}",
                    "",
                ]
            )
        )


async def save_student_credentials(entry: dict[str, str]) -> None:
    async with credentials_file_lock:
        await asyncio.to_thread(append_student_credentials, entry)


def verify_access_password(password: str, password_hash: str) -> bool:
    if not isinstance(password, str) or len(password.strip()) == 0:
        return False

    try:
        return access_password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

@admin.route("/add", methods=["POST"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def studentts_endpoint(payload, token):
    global id

    students = payload.get("students")
    access_password = str(payload.get("access_password", ""))
    if not isinstance(students, list) or len(students) == 0:
        return await create_response(
            400, "error", {"message": "The students payload must be a non-empty list."}, True, token
        )

    if not verify_access_password(access_password, ADMIN_PWD_HASH):
        return await create_response(
            401, "error", {"message": "The access password is not correct."}, True, token
        )

    for student in students:
        name = str(student.get("name", "")).strip()
        surname = str(student.get("surname", "")).strip()
        class_ = str(student.get("class", "")).strip()
        email = str(student.get("email", "")).strip().lower()

        if not name or not surname or not class_ or not email:
            return await create_response(
                400,
                "error",
                {
                    "message": "Each student must include name, surname, class and email."
                },
                True,
                token,
            )

        if "@" not in email or email.count("@") != 1:
            return await create_response(
                400,
                "error",
                {"message": "Each student email must be a valid email address."},
                True,
                token,
            )

        password = "ChangeMeYouCunt"
        hash_ = PasswordHasher().hash(password)
        full_name = f"{name} {surname}"
        created = False
        base_username = email
        username = base_username
        suffix = 1

        while not created:
            created = await user_db.add(
                {
                    "id": id,
                    "username": username,
                    "password": hash_,
                    "full_name": full_name,
                    "class": class_,
                },
                "username",
            )

            if not created:
                username = f"{base_username}{suffix}"
                suffix += 1


        existing_students = await classes_db.get(class_, "students")
        if existing_students is False:
            await classes_db.add({"name": class_, "students": [full_name]}, "name")
        else:
            await classes_db.update("name", class_, "students", full_name, "$push")

        id = id + 1

    return await create_response(200, "success", {"message": 0}, True, token)



@admin.route("/addImage", methods=["PUT"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def add_image(payload, token):
    file_request = await request.files
    form_data = await request.form
    class_ = str(request.args.get("class", "")).strip()
    access_password = str(form_data.get("access_password", ""))

    if not verify_access_password(access_password, IMAGE_PWD_HASH):
        return await create_response(
            401, "error", {"message": "The access password is not correct."}, True, token
        )

    if not class_:
        return await create_response(
            400, "error", {"message": "The class argument is required."}, True, token
        )

    if await classes_db.get(class_, "students") is False:
        return await create_response(
            404, "error", {"message": "The class name does not exist."}, True, token
        )

    uploaded_file = file_request.get("file")

    if uploaded_file is None or not uploaded_file.filename:
        return await create_response(
            400, "error", {"message": "No file was provided."}, True, token
        )

    try:
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
    except Exception:
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
    os.makedirs(CLASS_IMAGES_DIR, exist_ok=True)

    await uploaded_file.save(os.path.join(CLASS_IMAGES_DIR, f"{class_}.jpeg"))

    return await create_response(200, "success", {"message": 0}, True, token)
