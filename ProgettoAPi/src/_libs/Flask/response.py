import json
from functools import wraps

from quart import make_response, request, Response
from ..Jwt import verify_jwt, is_expired

from core import SECRET


async def create_response(
    status_code: int,
    type_: str,
    data: dict,
    existing: bool = False,
    cookie: tuple[str, int] | str = None,
    headers: list[dict[str, str]] = None,
) -> Response:
    """
    Docstring for create_response

    :param status_code: The status code of the response
    :type status_code: int
    :param type_: The type of the response: [success or error]
    :type type_: str
    :param data: The dict contsning the data payload of the response
    :type data: dict
    :param existing: True if the cookie doesnt have to be created False if it has to be created
    :type existing: bool
    :param cookie: The tuple containing thr cookie info and it has to be None if there is no token to be inclued in the response or the cookie as a string
    :type cookie: tuple[str, int] | str
    :param headers: A list containing the headers, the default is None
    :type headers: list[dict[str, str]]
    :return: Description
    :rtype: Response
    """

    payload = {"status": type_, "data": data}

    response = await make_response(json.dumps(payload))

    response.status_code = status_code

    if existing == True:
        response.headers["Cookie"] = cookie
    else:
        if not cookie is None:
            response.set_cookie(
                key="token",
                value=cookie[0],
                max_age=cookie[1],
                secure=True,
                httponly=True,
                samesite="Strict",
            )

    if not headers is None:
        for header_item in headers:
            for key, value in header_item.items():
                response[key] = value

    return response


def jwt_required(function):
    """
    Docstring for jwt_required

    :param function: Description
    """

    @wraps(function)  # https://docs.python.org/3/library/functools.html -> docs here
    async def wrapper(*args, **kwargs):
        """
        Docstring for wrapper

        :param args: Description
        :param kwargs: Description
        """

        token = request.cookies.get("token")
        payload = await request.get_json()

        if not token:
            response = await create_response(
                401, "error", {"message": "Token not found"}
            )

            return response
        elif not await verify_jwt(token, SECRET):
            response = await create_response(401, "error", {"mesage": "Invalid token"})

            return response

        elif await is_expired(token):
            response = await create_response(
                401, "error", {"message": "The token is expired"}
            )

            return response
        else:
            return await function(payload, token, *args, **kwargs)

    return wrapper
