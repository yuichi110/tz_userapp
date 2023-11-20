from flask import Flask, request, jsonify, Response
from userapp.parameter import Parameter
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
    users_json = service.list_users()
    return get_json_response(users_json)


@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):
    _, cookies = get_request_param()
    user_json = service.get_user(username, cookies)
    return get_json_response(user_json)


@app.route("/api/users", methods=["POST"])
def create_user():
    body, _ = get_request_param()
    service.signup(body)
    return get_json_response("{}")


@app.route("/api/signin", methods=["POST"])
def signin():
    body, _ = get_request_param()
    cookies = service.signin(body)
    # add session cookies
    response = get_json_response("{}")
    [response.set_cookie(t[0], t[1]) for t in cookies.items()]
    return response


# utility


def get_request_param() -> tuple[str, dict]:
    body = request.data.decode("utf-8")
    cookies = request.cookies
    return body, cookies


def get_json_response(json_data: str, status: int = 200) -> Response:
    response = app.response_class(
        response=json_data,
        status=status,
        mimetype="application/json",
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
