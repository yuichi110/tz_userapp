USER_REPOSITORY_TYPE_MOCK = "mock"
SESSION_REPOSITORY_TYPE_MOCK = "mock"


class Parameter:
    def __init__(self):
        # user repo
        self.user_repository_type = USER_REPOSITORY_TYPE_MOCK
        self.user_repository_host = "0.0.0.0"
        self.user_reporitory_port = -1

        # session repo
        self.session_repository_type = SESSION_REPOSITORY_TYPE_MOCK
        self.session_repository_host = "0.0.0.0"
        self.session_reporitory_port = -1

    def load(self):
        self._load_user_repository_parameters()
        self._load_session_repository_parameters()

    def _load_user_repository_parameters(self):
        ...

    def _load_session_repository_parameters(self):
        ...
