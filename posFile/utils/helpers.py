def format_currency(amount: float) -> str:
    return f"${amount:.2f}"


def format_datetime(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
