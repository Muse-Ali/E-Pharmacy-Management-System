from dataclasses import dataclass
from datetime import date


@dataclass
class Medicine:
    name: str         # Magaca dawada
    price: float      # Qiimaha la iibinayo
    stock: int        # Inta xabbo ee hadda taal
    expiry_date: str  # Taariikhda ay dhacayso (YYYY-MM-DD)

    def is_expired(self) -> bool:
        """Hubi haddii daawooyinku dhaceen"""
        try:
            exp = date.fromisoformat(self.expiry_date)
            return date.today() > exp
        except ValueError:
            return False

    def is_low_stock(self, threshold: int = 10) -> bool:
        """Hubi haddii stock yar yahay"""
        return self.stock <= threshold


class Pharmacy:
    def __init__(self):
        self.inventory: list[Medicine] = []

    def find_by_name(self, med_name: str) -> Medicine | None:
        for med in self.inventory:
            if med.name.lower().strip() == med_name.lower().strip():
                return med
        return None

    def add_medicine(self, medicine: Medicine) -> bool:
        if self.find_by_name(medicine.name) is not None:
            return False  # Hore ayuu u jiray
        self.inventory.append(medicine)
        return True

    def sell_medicine(self, med_name: str, qty: int) -> bool:
        med = self.find_by_name(med_name)
        if med is None:
            return False  # Daawo lama helin
        if med.stock < qty:
            return False  # Stock ma filna
        med.stock -= qty
        total_price = qty * med.price
        print(f"Wadarta lacagta: ${total_price:.2f}")
        return True

    def show_inventory(self) -> None:
        if not self.inventory:
            print("Inventory waa madhan yahay.")
            return
        for med in self.inventory:
            expired = " [DHACDAY]" if med.is_expired() else ""
            low     = " [STOCK YAR]" if med.is_low_stock() else ""
            print(f"{med}{expired}{low}")

    def all(self) -> list[Medicine]:
        return list(self.inventory)

    def update(
        self,
        name: str | None = None,
        *,
        price: float | None = None,
        expiry_date: str | None = None,
        stock: int | None = None,
    ) -> bool:
        m = self.find_by_name(name)
        if m is None:
            return False
        if price is not None:
            m.price = price
        if expiry_date is not None:
            m.expiry_date = expiry_date
        if stock is not None:
            m.stock = stock
        return True

    def clear(self) -> None:
        self.inventory = []