
_PERMISSIONS = {
    "admin": {
        "products", "categories", "staff", "pos", "sales", "reports",
        "inventory", "cash", "settings", "dashboard",
    },
    "cashier": {
        "pos", "sales", "reports",
    },
    "staff": {
        "pos",
    },
}


class PermissionService:
    @staticmethod
    def can(role: str, permission: str) -> bool:
        return permission in _PERMISSIONS.get(role, set())
