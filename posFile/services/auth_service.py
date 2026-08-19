import bcrypt

from database.database import Database


class AuthService:
    def __init__(self, db: Database, audit_service=None):
        self.db = db
        self.audit_service = audit_service

    def authenticate(self, username: str, password: str):
        try:
            rows = self.db.fetch_all(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    staff_id
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,),
            )

            if not rows:
                if self.audit_service:
                    self.audit_service.log(
                        None,
                        "LOGIN_FAILED",
                        "User",
                        None,
                        f"Failed login attempt for username: {username}",
                    )
                return None

            user_id, db_username, db_password, role, staff_id = rows[0]

            if not bcrypt.checkpw(password.encode("utf-8"), db_password.encode("utf-8")):
                if self.audit_service:
                    self.audit_service.log(
                        user_id,
                        "LOGIN_FAILED",
                        "User",
                        user_id,
                        f"Failed login attempt for username: {username}",
                    )
                return None

            if self.audit_service:
                self.audit_service.log(
                    user_id,
                    "LOGIN_SUCCESS",
                    "User",
                    user_id,
                    f"User {username} logged in successfully",
                )

            return {
                "id": user_id,
                "username": db_username,
                "role": role,
                "staff_id": staff_id,
            }

        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
