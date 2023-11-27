from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from userapp.services.user_service import UserService
from userapp.models.user import (
    SignupBody,
    SigninBody,
    UserSchemaWithoutPassword,
)


class UserRouter(APIRouter):
    def __init__(
        self,
        service: UserService,
    ):
        super().__init__()
        self._service = service

        self.add_api_route(
            "/",
            self.index,
            methods=["GET"],
            responses={
                200: {
                    "description": 'Redirect to Swagger URL "/redoc"',
                },
            },
        )

        self.add_api_route(
            "/api/users",
            self.list_users,
            methods=["GET"],
            response_model=list[UserSchemaWithoutPassword],
        )

        self.add_api_route(
            "/api/users/{username}",
            self.get_user,
            methods=["GET"],
            response_model=UserSchemaWithoutPassword,
        )

        self.add_api_route(
            "/api/users",
            self.signup,
            methods=["POST"],
        )

        self.add_api_route(
            "/api/signin",
            self.signin,
            methods=["POST"],
        )

        self.add_api_route(
            "/api/signin",
            self.signout,
            methods=["DELETE"],
        )

    def index(self):
        return RedirectResponse("/redoc")

    def list_users(self):
        # debug purpose for sample app.
        users = self._service.list_users()
        return users

    def get_user(self, username, request: Request):
        all_cookies = request.cookies
        user = self._service.get_user(username, all_cookies)
        return user

    def signup(self, body: SignupBody):
        self._service.signup(body)
        return {}

    def signin(self, body: SigninBody):
        cookies = self._service.signin(body)
        # add session cookies
        response = JSONResponse(content={})
        [response.set_cookie(key=t[0], value=t[1]) for t in cookies.items()]
        return response

    def signout(self, request: Request):
        all_cookies = request.cookies
        delete_cookie_keys: list[str] = self._service.signout(all_cookies)
        # delete session cookies whether signin or not
        response = JSONResponse(content={})
        for key in delete_cookie_keys:
            response.delete_cookie(key=key)
        return response
