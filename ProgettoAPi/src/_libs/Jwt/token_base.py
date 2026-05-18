import hmac
import json
import hashlib
import base64
import datetime


async def encode_jwt(
    payload: dict, secret: bytes, headers: dict = {"alg": "HS256", "typ": "JWT"}
) -> str | None:
    """
    Docstring for encode_jwt

    :param payload: Description
    :type payload: dict
    :param secret: Description
    :type secret: bytes
    :param headers: Description
    :type headers: dict
    :return: Description
    :rtype: str | None
    """

    try:
        payload = (
            base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        )
        headers = (
            base64.urlsafe_b64encode(json.dumps(headers).encode()).decode().rstrip("=")
        )

        hash_ = base64.urlsafe_b64encode(
            hmac.new(secret, f"{headers}.{payload}".encode(), hashlib.sha256).digest()
        ).decode()

        return f"{headers}.{payload}.{hash_.rstrip("=")}"
    except Exception as e:
        return None


async def decode_jwt(token: str) -> tuple[dict, dict] | None:
    """
    Docstring for decode_jwt

    :param token: Description
    :type token: str
    :return: Description
    :rtype: tuple[dict, dict] | None
    """

    try:
        data = token.split(".")

        headers = data[0]
        payload = data[1]

        return (
            json.loads(base64.urlsafe_b64decode(headers + "==")),
            json.loads(base64.urlsafe_b64decode(payload + "==")),
        )
    except Exception as e:
        return None


"""
async def update_jwt(token: str, secret: str, key: str, new_value: Any) -> str | None:
    try:
        headers, payload = decode_jwt(token)

        payload[key] = new_value

        return encode_jwt(payload, secret, headers)
    except Exception as e:
        return None
"""


async def verify_jwt(token: str, secret: bytes) -> bool | None:
    """
    Docstring for verify_jwt

    :param token: Description
    :type token: str
    :param secret: Description
    :type secret: bytes
    :return: Description
    :rtype: bool | None
    """

    try:
        data = token.split(".")

        headers = data[0]
        payload = data[1]

        hash_ = hmac.new(
            secret, f"{headers}.{payload}".encode(), hashlib.sha256
        ).digest()

        return hmac.compare_digest(hash_, base64.urlsafe_b64decode(data[2] + "=="))
    except:
        return None


async def is_expired(token: str) -> bool | None:
    """
    Docstring for is_expired

    :param token: Description
    :type token: str
    :return: Description
    :rtype: bool | None
    """

    try:
        decoded_jwt = await decode_jwt(token)
        exp = decoded_jwt[1].get("exp")

        if int(datetime.datetime.now().timestamp()) < exp:
            return False

        return False
    except Exception as e:
        return None
