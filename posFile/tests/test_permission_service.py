from services.permission_service import PermissionService

def test_admin_can_manage_products():
    assert PermissionService.can("admin", "products")

def test_cashier_can_use_pos():
    assert PermissionService.can("cashier", "pos")

def test_cashier_cannot_manage_staff():
    assert not PermissionService.can("cashier", "staff")

def test_staff_cannot_use_cash():
    assert not PermissionService.can("staff", "cash")

def test_unknown_role_has_no_permissions():
    assert not PermissionService.can("unknown", "products")