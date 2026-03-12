import datetime
from quart import Blueprint, request
from quart_rate_limiter import rate_limit

from core import user_db, SECRET
from _libs.Flask import create_response
from _libs.Jwt import encode_jwt
from _libs.Data import Password, Username

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
@rate_limit(20, datetime.timedelta(minutes=3))
async def login_endpoint():
    try:
        data: dict = await request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = await user_db.get(username=username, password=password)

        if user is not None:
            user_id = user.get("id")
            token_payload = {
                "id": user_id,
                "exp": int((datetime.datetime.now() + datetime.timedelta(minutes=6)).timestamp()),
            }

            token = await encode_jwt(payload=token_payload, secret=SECRET)
            response = await create_response(200, "success", {"message": 0}, cookie=(token, 6 * 60))
            return response

        return await create_response(400, "error", {"message": "Incorrect credentials"})
    except Exception as e: #Ho modificato leggermente per poter vedere l'eccezione "errore interno al server" 
        import traceback 
        traceback.print_exc()
        return await create_response(500, "error", {"message": str(e)})
    


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

    user = await user_db.add(username, password)

    if user:
        token_payload = {
            "id": user,
            "exp": int(
                (datetime.datetime.now() + datetime.timedelta(minutes=6)).timestamp()
            ),
        }

        token = await encode_jwt(payload=token_payload, secret=SECRET)

        response = await create_response(
            200, "success", {"message": 0}, cookie=(token, 1000000 * 60)
        )

        return response
    return await create_response(400, "error", {"message": "User already exist"})
