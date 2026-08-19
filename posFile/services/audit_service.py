from datetime import datetime

from database.database import Database


class AuditService:
    def __init__(self, db: Database):
        self.db = db

    def log(
        self,
        user_id,
        action,
        entity_type=None,
        entity_id=None,
        description=None,
    ):
        try:
            self.db.execute_query(
                """
                INSERT INTO audit_logs
                    (user_id, action, entity_type, entity_id, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    action,
                    entity_type,
                    entity_id,
                    description,
                    datetime.now(),
                ),
            )
        except Exception:
            pass
