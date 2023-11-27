import logging
import pytest
from userapp.services.user_service import UserService
from userapp.repositories.session.mock import MockSessionRepository
from userapp.repositories.user.mock import MockUserRepository
from userapp.models.user import SigninBody, SignupBody
from userapp.exceptions import ClientException


def test_all():
    # please create tests for each method
    logger = logging.getLogger()
    service = UserService(
        MockUserRepository(logger), MockSessionRepository(logger), logger
    )

    # list_users()
    users = service.list_users()
    assert len(users) == 2

    # signup
    o = SignupBody(
        username="tanzu",
        email="tanzu@vmware.com",
        password1="p@ssw0rd",
        password2="p@ssw0rd",
    )
    service.signup(o)
    users = service.list_users()
    assert len(users) == 3

    # signup dup username
    with pytest.raises(ClientException) as exc_info:
        service.signup(
            SignupBody(
                username="tanzu",
                email="tanzu2@vmware.com",
                password1="p@ssw0rd",
                password2="p@ssw0rd",
            )
        )
    assert exc_info.type is ClientException

    # signin
    o = SigninBody(
        username_or_email="tanzu",
        password="p@ssw0rd",
    )
    cookies = service.signin(o)

    # signin not exist user
    with pytest.raises(ClientException) as exc_info:
        service.signin(
            SigninBody(
                username_or_email="guest",
                password="p@ssw0rd",
            )
        )
    assert exc_info.type is ClientException

    # get user
    service.get_user("tanzu", cookies)
