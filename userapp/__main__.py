from flask import Flask, request, jsonify, Response
from pydantic import BaseModel
import json

from userapp.parameter import Parameter
from userapp.models.user import (
    BlankJsonSchema,
    SignupBody,
    SigninBody,
    UserSchemaWithoutPassword,
)
from userapp.di import DiContainer
from userapp.exceptions import ClientException, ServerException

app = Flask(__name__)


# inject dependency


def build_service():
    params = Parameter()
    params.load()
    dic = DiContainer(params)
    return dic.get_service()


service = build_service()


# error handling. needs more error type


def handle_client_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = getattr(error, "code", 400)
    return response


def handle_expected_server_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = getattr(error, "code", 500)
    return response


def handle_unexpected_server_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = getattr(error, "code", 500)
    return response


app.register_error_handler(ClientException, handle_client_error)
app.register_error_handler(ServerException, handle_expected_server_error)
app.register_error_handler(Exception, handle_unexpected_server_error)

# routing


@app.route("/api/users", methods=["GET"])
def list_users():
    # debug purpose for sample app.
    users = service.list_users()
    return get_json_response(users)


@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):
    _, cookies = get_request_param()
    user = service.get_user(username, cookies)
    return get_json_response(user)


@app.route("/api/users", methods=["POST"])
def create_user():
    body, _ = get_request_param()
    obj = get_model_from_json(body, SignupBody)
    service.signup(obj)
    return get_json_response(BlankJsonSchema())


@app.route("/api/signin", methods=["POST"])
def signin():
    body, _ = get_request_param()
    obj = get_model_from_json(body, SigninBody)
    cookies = service.signin(obj)
    # add session cookies
    response = get_json_response(BlankJsonSchema())
    [response.set_cookie(t[0], t[1]) for t in cookies.items()]
    return response


@app.route("/api/signin", methods=["DELETE"])
def signout():
    _, cookies = get_request_param()
    delete_cookie_keys: list[str] = service.signout(cookies)
    # delete session cookies
    response = get_json_response(BlankJsonSchema())
    for key in delete_cookie_keys:
        response.delete_cookie(key)
    return response


# utility


def get_request_param() -> tuple[str, dict]:
    body = request.data.decode("utf-8")
    cookies = request.cookies
    return body, cookies


def get_model_from_json(
    json_data: str,
    data_model: BaseModel,
) -> BaseModel:
    try:
        d = json.loads(json_data)
    except Exception:
        raise ClientException("invalid json format")
    try:
        obj = data_model.model_validate(d)
    except Exception:
        raise ClientException("invalid request api schema")
    return obj


def get_json_response(
    obj: list[BaseModel] | BaseModel,
    status: int = 200,
) -> Response:
    if isinstance(obj, list):
        obj_list = obj
        json_data = json.dumps([o.model_dump() for o in obj_list])
    else:
        json_data = json.dumps(obj.model_dump())
    response = app.response_class(
        response=json_data,
        status=status,
        mimetype="application/json",
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
