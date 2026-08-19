from datetime import datetime


def generate_receipt(cart: list, staff_name: str, total: float) -> str:
    lines = []
    lines.append("POS Receipt")
    lines.append("=" * 30)
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Staff: {staff_name}")
    lines.append("-" * 30)
    for item in cart:
        name, price, qty, item_total = item[1], item[2], item[3], item[4]
        lines.append(f"{name} x{qty} @ ${price:.2f} = ${item_total:.2f}")
    lines.append("-" * 30)
    lines.append(f"Total: ${total:.2f}")
    return "\n".join(lines)


def save_receipt_to_file(receipt_text: str, file_path: str):
    with open(file_path, "w") as f:
        f.write(receipt_text)
