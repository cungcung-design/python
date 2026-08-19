# Smart POS

A Point-of-Sale (POS) system built with Python and Tkinter, using MySQL (`pos_db`) as the backend database.

## Version

Current version: **1.1.0**

## Changelog

### v1.1.0

**Added:**
- Low-stock detection and inventory alerts
- Inventory filtering and search
- Advanced sales reports with CSV/PDF export
- Database backup and restore
- Audit logs with action tracking
- Settings page (store name, currency, receipt footer, low-stock threshold)
- Validation and error handling utilities
- Automated tests with pytest

**Improved:**
- Dashboard with real-time stats
- Inventory workflow
- Database schema and indexes
- Application responsiveness

## Project Structure

```
posFile/
├── main.py                    # Application entry point
├── config/
│   └── config.py              # Database configuration
├── database/
│   ├── __init__.py
│   ├── database.py            # Database connection and schema setup
│   └── setup.sql              # Fresh database schema
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   ├── staff.py
│   └── sale.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── product_service.py
│   ├── inventory_service.py
│   ├── sales_service.py
│   ├── cash_service.py
│   ├── report_service.py
│   ├── audit_service.py
│   └── permission_service.py
├── ui/
│   ├── __init__.py
│   ├── styles/
│   │   ├── colors.py
│   │   ├── fonts.py
│   │   └── styles.py
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── header.py
│   │   ├── stat_card.py
│   │   └── data_table.py
│   └── pages/
│       ├── login.py
│       ├── dashboard.py
│       ├── pos.py
│       ├── products.py
│       ├── inventory.py
│       ├── categories.py
│       ├── staff.py
│       ├── sales.py
│       ├── cash_management.py
│       ├── reports.py
│       ├── settings.py
│       └── audit.py
├── utils/
│   ├── helpers.py
│   ├── validators.py
│   └── receipt.py
├── tests/
│   ├── test_auth_service.py
│   ├── test_product_service.py
│   ├── test_cart.py
│   ├── test_sales_service.py
│   ├── test_cash_service.py
│   ├── test_register_service.py
│   ├── test_dashboard_service.py
│   ├── test_permission_service.py
│   ├── test_audit_service.py
│   └── test_validators.py
├── assets/
│   ├── images/
│   ├── icons/
│   └── logo/
├── requirements.txt
├── README.md
└── .gitignore
```

## Database

1. The project uses MySQL and the database is named `pos_db`.
2. Run `database/setup.sql` in MySQL to initialize the schema.
3. The application should use `pos_db`.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Update database credentials in `config/config.py` or `.env` if needed.

3. Run the application:
    ```bash
    python main.py
    ```

4. Run tests:
    ```bash
    python -m pytest -v
    ```

## Default Login

- Username: `admin`
- Password: `password`
