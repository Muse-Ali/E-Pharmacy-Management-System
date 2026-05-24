from pathlib import Path
from models.Medicine import Pharmacy, Medicine

DATA_PATH = Path(__file__).resolve().parent / "data" / "Medicine.txt"

FILE_HEADER = "name|price|stock|expiry_date"


def parse_inventory(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def is_column_header_line(line: str) -> bool:
    return line.strip().lower() == FILE_HEADER.lower()


def load_medicine(path: Path, pharmacy: Pharmacy) -> None:
    pharmacy.clear()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if is_column_header_line(line):
                    continue
                parts = line.split("|", 3)
                if len(parts) != 4:
                    continue
                name, price, stock, expiry_date = parts
                try:
                    medicine = Medicine(
                        name=name.strip(),
                        price=float(price.strip()),
                        stock=int(stock.strip()),
                        expiry_date=expiry_date.strip(),
                    )
                    pharmacy.add_medicine(medicine)
                except ValueError:
                    continue
    except FileNotFoundError:
        # ✨ ADDED: file uusan jirin — otomaatig u samee header-ka
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(FILE_HEADER + "\n")


def save_medicine(path: Path, pharmacy: Pharmacy) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(FILE_HEADER + "\n")
        for med in pharmacy.all():
            f.write(f"{med.name}|{med.price}|{med.stock}|{med.expiry_date}\n")