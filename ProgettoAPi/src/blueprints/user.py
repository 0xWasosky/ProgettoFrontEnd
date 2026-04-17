import datetime
from flask import Blueprint, request
from quart_rate_limiter import rate_limit

from argon2 import PasswordHasher

from core import user_db
from _libs.Flask import jwt_required, create_response
from _libs.Jwt import decode_jwt
from _libs.Data import Password

user = Blueprint("user", __name__, url_prefix="/user")


hasher = PasswordHasher()


@user.route("/change_password", methods=["POST"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def password_endpoint(payload, token):

    decoded_token = await decode_jwt(token)
    id_ = decoded_token[1].get("id")

    old_password = payload.get("old_password")
    new_password = payload.get("new_password")

    old_hash = await user_db.get("id", id_, ["password"])
    
    if not old_hash:
        return await create_response(
            400,
            "error",
            {"message": "The user id is invalid"},
            True,
            request.cookies.get("token"), #Piccola modifica che sono andato a prendere da internet, non ha cambiato la logica in nessun modo
        )
    if not hasher.verify(old_hash["password"], old_password):
        return await create_response(
            400, "error", {"message": "The old password is not correct"}, True, token
        )

    if not Password.check(new_password):
        return await create_response(
            400,
            "error",
            {
                "message": "The password must contain 1 symbol, 1 number, 1 uppercase letter and 1 lowercase letter it also has to be between 16 and 64 characters. "
            },
            True,
            token,
        )

    await user_db.update("id", id_, "password", hasher.hash(new_password), "$set")

    return await create_response(200, "success", {"message": 0}, True, token)
