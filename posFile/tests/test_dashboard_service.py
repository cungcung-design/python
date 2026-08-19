from unittest.mock import MagicMock

from services.report_service import ReportService


class FakeDashboardDatabase:
    def __init__(self):
        self.today_sales = 1500.0
        self.today_transactions = 25
        self.total_products = 120

    def fetch_all(self, query, params=None):
        normalized = " ".join(query.lower().split())
        if "coalesce(sum(total), 0)" in normalized and "date(date) = curdate()" in normalized:
            return [(self.today_sales,)]
        if "count(*)" in normalized and "date(date) = curdate()" in normalized:
            return [(self.today_transactions,)]
        if "count(*)" in normalized and "from items" in normalized:
            return [(self.total_products,)]
        return []


def test_get_dashboard_stats():
    db = FakeDashboardDatabase()
    service = ReportService(db)
    stats = service.get_dashboard_stats()
    assert stats["today_sales"] == 1500.0
    assert stats["today_transactions"] == 25
    assert stats["total_products"] == 120


def test_get_dashboard_stats_zero():
    db = FakeDashboardDatabase()
    db.today_sales = 0.0
    db.today_transactions = 0
    db.total_products = 0
    service = ReportService(db)
    stats = service.get_dashboard_stats()
    assert stats["today_sales"] == 0.0
    assert stats["today_transactions"] == 0
    assert stats["total_products"] == 0