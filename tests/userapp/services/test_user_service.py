import json
import pytest
from userapp.services.user_service import UserService
from userapp.repositories.session.mock import MockSessionRepository
from userapp.repositories.user.mock import MockUserRepository
from userapp.models.user import SigninBody, SignupBody
from userapp.exceptions import ClientException


def test_all():
    # please create tests for each method
    service = UserService(MockUserRepository(), MockSessionRepository())

    # list_users()
    users = service.list_users()
    assert len(json.loads(users)) == 2

    # signup
    j = SignupBody(
        username="tanzu",
        email="tanzu@vmware.com",
        password1="p@ssw0rd",
        password2="p@ssw0rd",
    ).model_dump_json()
    service.signup(j)
    users = service.list_users()
    assert len(json.loads(users)) == 3

    with pytest.raises(ClientException) as exc_info:
        service.signup(
            SignupBody(
                username="tanzu",
                email="tanzu@vmware.com",
                password1="p@ssw0rd",
                password2="p@ssw0rd",
            ).model_dump_json()
        )
    assert exc_info.type is ClientException

    # signin
    j = SigninBody(
        username_or_email="tanzu",
        password="p@ssw0rd",
    ).model_dump_json()
    cookies = service.signin(j)

    with pytest.raises(ClientException) as exc_info:
        service.signin(
            SigninBody(
                username_or_email="guest",
                password="p@ssw0rd",
            ).model_dump_json()
        )
    assert exc_info.type is ClientException

    # get user
    service.get_user("tanzu", cookies)
