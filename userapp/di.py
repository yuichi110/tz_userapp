import userapp.parameter as prm
from userapp.repositories.user.abstract import AbstractUserRepository
from userapp.repositories.user.mock import MockUserRepository
from userapp.repositories.session.abstract import AbstractSessionRepository
from userapp.repositories.session.mock import MockSessionRepository
from userapp.services.user_service import UserService


class DiContainer:
    def __init__(self, parameter: prm.Parameter):
        self._parameter = parameter

    def get_service(self) -> UserService:
        # logger = self._get_logger()
        user_repository = self._get_user_repository()
        session_repository = self._get_session_repository()
        return UserService(user_repository, session_repository)

    def _get_logger(self):
        ...

    def _get_user_repository(self) -> AbstractUserRepository:
        repo_type = self._parameter.user_repository_type
        if repo_type == prm.USER_REPOSITORY_TYPE_MOCK:
            return MockUserRepository()
        else:
            raise ValueError

    def _get_session_repository(self) -> AbstractSessionRepository:
        repo_type = self._parameter.session_repository_type
        if repo_type == prm.SESSION_REPOSITORY_TYPE_MOCK:
            return MockSessionRepository()
        else:
            raise ValueError
