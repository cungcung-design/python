import bcrypt

from services.auth_service import AuthService


class FakeDatabase:
    def __init__(self):
        password = bcrypt.hashpw(
            b"password",
            bcrypt.gensalt(),
        ).decode()

        self.users = [
            (
                1,
                "admin",
                password,
                "admin",
                1,
            )
        ]

    def fetch_all(self, query, params):
        if params and len(params) > 0:
            username = params[0]
            for user in self.users:
                if user[1] == username:
                    return [user]
        return []


def test_valid_login():
    db = FakeDatabase()
    auth = AuthService(db)

    user = auth.authenticate("admin", "password")

    assert user is not None
    assert user["username"] == "admin"
    assert user["role"] == "admin"


def test_invalid_password():
    db = FakeDatabase()
    auth = AuthService(db)

    user = auth.authenticate("admin", "wrongpassword")

    assert user is None


def test_nonexistent_user():
    db = FakeDatabase()
    auth = AuthService(db)

    user = auth.authenticate("nonexistent", "password")

    assert user is None
