import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from models.Medicine import Pharmacy, Medicine
from utils.storage import load_medicine, save_medicine, DATA_PATH


def print_header():
    print("=" * 45)
    print("    E-PHARMACY MANAGEMENT SYSTEM")
    print("=" * 45)


def main():
    pharmacy = Pharmacy()
    load_medicine(DATA_PATH, pharmacy)

    while True:
        print_header()
        print("  1. Daawo Cusub Ku Dar")
        print("  2. Daawo Iib")
        print("  3. Inventory Fiiri")
        print("  4. Daawo Update")
        print("  5. Inventory Nadiifi")
        print("  6. Ka Bax")
        print("-" * 45)
      
        choice = input("Xulo [1-6]: ").strip()
        if not choice.isdigit():
            print("Kalad waye! fadlan gali number [1/6]\n")
            continue
        if choice == "1":
            add_medicine(pharmacy)
        elif choice == "2":
            sell_medicine(pharmacy)
        elif choice == "3":
            show_inventory(pharmacy)
        elif choice == "4":
            update_medicine(pharmacy)
        elif choice == "5":
            clear_inventory(pharmacy)
        elif choice == "6":
            save_medicine(DATA_PATH, pharmacy)
            print("\nXogta waa la kaydiyay. Nabad gelyo!\n")
            break
        else:
            print("Xulasho khaldan. fadlan markale ku celi.\n")
            continue  # ✨ ADDED: save_medicine ha u socdon haddii choice khaldan yahay

        save_medicine(DATA_PATH, pharmacy)


# 1. ADD
def add_medicine(pharmacy: Pharmacy) -> None:
    print("\nDAAWO CUSUB KU DAR")
    print("-" * 35)
    name        = input("  Magaca               : ").strip()
    price_str   = input("  Qiimaha ($)          : ").strip()
    stock_str   = input("  Tirada               : ").strip()
    expiry_date = input("  Taariikhda (YYYY-MM-DD): ").strip()

    if not name:
        print("Magaca ma noqon karo madhan!\n")
        return

    try:
        price = float(price_str)
        stock = int(stock_str)
    except ValueError:
        print("Qiimaha ama tirada khaldan!\n")
        return

    if price <= 0 or stock < 0:
        print("Qiimaha waa in uu ka weyn yahay eber, tiraduna ma noqon karto tiro taban!\n")
        return  # ✨ ADDED: qiime iyo stock xaq ah hubi

    med = Medicine(name=name, price=price, stock=stock, expiry_date=expiry_date)

    if pharmacy.add_medicine(med):
        print(f"'{name}' si guul leh ayaa loo daray!\n")
    else:
        print(f"'{name}' hore ayuu u jiray — lama darin.\n")


# 2. SELL
def sell_medicine(pharmacy: Pharmacy) -> None:
    print("\nDAAWO IIB")
    print("-" * 35)
    name    = input("  Magaca Daawooyinka : ").strip()
    qty_str = input("  Tirada             : ").strip()

    try:
        qty = int(qty_str)
    except ValueError:
        print("Tirada khaldan!\n")
        return

    if pharmacy.sell_medicine(name, qty):
        print(f"{qty} '{name}' si guul leh ayaa loo iibiyay!\n")
    else:
        print("Iibku fashilmay — daawooyinku ma jiraan ama stock ma filna.\n")


# 3. SHOW
def show_inventory(pharmacy: Pharmacy) -> None:
    print("\nINVENTORY")
    print("-" * 55)
    medicines = pharmacy.all()
    if not medicines:
        print("  Inventory waa madhan yahay.\n")
        return
    print(f"  {'Magac':<20} {'Qiimo':>8} {'Tiro':>6}  {'Taariikhda'}")
    print("  " + "-" * 50)
    for med in medicines:
        print(f"  {med.name:<20} ${med.price:>7.2f} {med.stock:>6}  {med.expiry_date}")
    print(f"\n  Wadarta: {len(medicines)} daawo\n")


# 4. UPDATE
def update_medicine(pharmacy: Pharmacy) -> None:
    print("\nDAAWO UPDATE")
    print("-" * 35)
    name       = input("  Magaca Daawooyinka              : ").strip()
    price_str  = input("  Qiime Cusub  (Enter u dhaaf)    : ").strip()
    expiry_str = input("  Taariikhda Cusub (Enter u dhaaf): ").strip()

    price  = float(price_str) if price_str  else None
    expiry = expiry_str        if expiry_str else None

    if pharmacy.update(name, price=price, expiry_date=expiry):
        print(f"'{name}' si guul leh ayaa loo cusbooneysiiyay!\n")
    else:
        print(f"'{name}' lama helin.\n")


# 5. CLEAR
def clear_inventory(pharmacy: Pharmacy) -> None:
    confirm = input("\nInventory dhamaan nadiifin? (y/n): ").strip().lower()
    if confirm == "y":
        pharmacy.clear()
        print("Inventory waa la nadiifiyay.\n")
    else:
        print("La joojiyay.\n")


if __name__ == "__main__":
    main()