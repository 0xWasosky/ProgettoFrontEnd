import asyncio
import datetime
import os
import secrets
from quart import Blueprint, request
from quart_rate_limiter import rate_limit

from _libs.Flask import jwt_required, create_response

from core import classes_db, user_db, ADMIN_PWD, IMAGE_PWD

from argon2 import PasswordHasher
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

#Qui viene creato e registarto l'account di uno studente
#credo però che ci sia un problema con l'incremento degli id
#Qui ho sostanzialmente aggiunto il fatto che da risposte diverse
@admin.route("/add", methods=["POST"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def studentts_endpoint(payload, token):
    global id

    students = payload.get("students")
    if not isinstance(students, list) or len(students) == 0:
        return await create_response(
            400, "error", {"message": "The students payload must be a non-empty list."}, True, token
        )

    if request.headers.get("access") != ADMIN_PWD:
        return await create_response(
            401, "error", {"message": "The account does not have access to this function."}, True, token
        )

    for student in students:
        name = str(student.get("name", "")).strip()
        surname = str(student.get("surname", "")).strip()
        class_ = str(student.get("class", "")).strip()

        if not name or not surname or not class_:
            return await create_response(
                400,
                "error",
                {"message": "Each student must include name, surname and class."},
                True,
                token,
            )

        password = secrets.token_urlsafe(32)
        hash_ = PasswordHasher().hash(password) 
        full_name = f"{name} {surname}"
        created = False

        while not created:
            username = f"{name}.{surname}.{id}"
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
                id = id + 1

        try:
            await save_student_credentials(
                {
                    "full_name": full_name,
                    "class": class_,
                    "username": username,
                    "password": password,
                }
            )
        except OSError:
            await user_db.delete("username", username)
            return await create_response(
                500,
                "error",
                {
                    "message": "The student could not be saved to the credentials file. Please try again."
                },
                True,
                token,
            )

        existing_students = await classes_db.get(class_, "students")
        if existing_students is False:
            await classes_db.add({"name": class_, "students": [full_name]}, "name")
        else:
            await classes_db.update("name", class_, "students", full_name, "$push")

        id = id + 1

    return await create_response(200, "success", {"message": 0}, True, token)


#Qui invece viene inserita l'immagine della classe
#Alla fini rispetto alla tua versione ho solo aggiuto il fatto 
#da più risposte diverse perché mi serviva per il debug come sopra del resto
@admin.route("/addImage", methods=["PUT"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def add_image(payload, token):
    file_request = await request.files
    class_ = str(request.args.get("class", "")).strip()

    if request.headers.get("access") != IMAGE_PWD:
        return await create_response(
            401, "error", {"message": "The account does not have access to this function."}, True, token
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
