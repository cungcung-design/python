from unittest.mock import MagicMock

from services.audit_service import AuditService


class FakeAuditDatabase:
    def __init__(self):
        self.logs = []

    def execute_query(self, query, params=None):
        self.logs.append(params)


def test_audit_log_created():
    db = FakeAuditDatabase()
    service = AuditService(db)
    service.log(1, "LOGIN_SUCCESS", "User", 1, "Admin logged in")
    assert len(db.logs) == 1
    assert db.logs[0][0] == 1
    assert db.logs[0][1] == "LOGIN_SUCCESS"
    assert db.logs[0][2] == "User"
    assert db.logs[0][3] == 1
    assert db.logs[0][4] == "Admin logged in"


def test_audit_log_without_user():
    db = FakeAuditDatabase()
    service = AuditService(db)
    service.log(None, "LOGIN_FAILED", "User", None, "Failed login")
    assert len(db.logs) == 1
    assert db.logs[0][0] is None


def test_audit_log_database_error_is_swallowed():
    class FailingDatabase:
        def execute_query(self, query, params=None):
            raise Exception("Database error")

    service = AuditService(FailingDatabase())
    service.log(1, "TEST", "Entity", 1, "description")
