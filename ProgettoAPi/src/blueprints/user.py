import datetime
from flask import Blueprint, request
from quart_rate_limiter import rate_limit

from core import user_db
from _libs.Flask import jwt_required, create_response
from _libs.Jwt import decode_jwt


user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/change_username", methods=["POST"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def username_endpoint(payload, token):

    decoded_token = await decode_jwt(token)
    id_ = decoded_token[1].get("id")

    username = payload.get("username")

    if id_ is None:
        return await create_response(400, "error", {"message": "The token is invalid"})

    user = await user_db.update("username", username, id_)

    if user:
        response = await create_response(
            200, "success", {"message": 0}, (token, 6 * 60)
        )

        return response

    return await create_response(400, "error", {"message": "The id is invliad"})


@user.route("/change_password", methods=["POST"])
@rate_limit(5, datetime.timedelta(minutes=3))
@jwt_required
async def password_endpoint(payload, token):

    decoded_token = await decode_jwt(token)
    id_ = decoded_token[1].get("id")

    old_password = payload.get("old_password")
    new_password = payload.get("new_password")

    if id_ is None:
        return await create_response(400, "error", {"error": "The token is invalid"})

    user = await user_db.update("password", new_password, id_, old_password)

    if user:
        response = await create_response(
            200, "success", {"message": 0}, (token, 6 * 60)
        )

        return response

    return await create_response(
        400,
        "error",
        {"message": "The id is invliad or the current password is incorrect"},
    )
