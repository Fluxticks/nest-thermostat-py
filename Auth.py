class Auth:
    __slots__ = ("_project_id", "_access_token", "_refresh_token")

    def __init__(self, project_id: str, access_token: str, refresh_token: str):
        self._project_id = project_id
        self._access_token = access_token
        self._refresh_token = refresh_token
