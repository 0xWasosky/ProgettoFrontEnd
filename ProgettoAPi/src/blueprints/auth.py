import datetime
import uuid 
from quart import Blueprint, request
from quart_rate_limiter import rate_limit
from argon2 import PasswordHasher

from core import user_db, SECRET
from _libs.Flask import create_response
from _libs.Jwt import encode_jwt
from _libs.Data import Password, Username



auth = Blueprint("auth", __name__, url_prefix="/auth")

hasher = PasswordHasher()


@auth.route("/login", methods=["POST"])
@rate_limit(20, datetime.timedelta(minutes=3))
async def login_endpoint():
    data: dict = await request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = await user_db.get("username", username, ["id", "password"])



    user_id = user.get("id")

    token_payload = {
        "id": user_id,
        "exp": int(
            (datetime.datetime.now() + datetime.timedelta(minutes=6)).timestamp()
        ),
    }
    token = await encode_jwt(payload=token_payload, secret=SECRET)
    response = await create_response(200, "success", {"message": 0}, cookie=token)
    return response


#Sì avevo riaperto il register per poter testare l'applicazione ora è richiuso
#Da frontEnd è ancora presente il componente, penso di tenerlo nel caso in cui ci serve a qualcosa
#e secondo me è anche una buona idea tenere il codice di questo endpoint
#In ogni caso se non vogliamo la registrazione possiamo tranquillamente togliere il link che 
#porta al componente Registre.vue, potrebbe essere codice rindondante ed inutile ma secondo me conviene tenerlo
#Lo ho leggermente modificato ma giusto per renderlo più solido quindi realmente ho modificato
#solamnete l'inserimento che ora viene fatto con un dizionario (righe 82-90) la cui chiave è semplicemente username
#ed adesso l'hashing delle password è espplicito(riga 87)
@auth.route("/register", methods=["POST"])
@rate_limit(20, datetime.timedelta(minutes=3))
async def register_endpoint():
    data: dict = await request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not await Username.check(username):
        return await create_response(
            400,
            "error",
            {
                "message": "The username can not contain any symbol other than the underscore and it must be between 5 and 20 characters."
            },
        )

    if not await Password.check(password):
        return await create_response(
            400,
            "error",
            {
                "message": "The password must contain 1 symbol, 1 number, 1 uppercase letter and 1 lowercase letter it also has to be between 16 and 64 characters. "
            },
        )

    new_user_id = str(uuid.uuid4())
    created = await user_db.add(
        {
            "id": new_user_id,
            "username": username,
            "password": hasher.hash(password),
        },
        "username",
    )

    if created:
        token_payload = {
            "id": new_user_id,
            "exp": int(
                (datetime.datetime.now() + datetime.timedelta(minutes=6)).timestamp()
            ),
        }

        token = await encode_jwt(payload=token_payload, secret=SECRET)

        response = await create_response(
            200, "success", {"message": 0}, cookie=token
        )

        return response
    return await create_response(400, "error", {"message": "User already exist"})
