# Malabar Family Restaurant — Billing System

A simple desktop billing and order management application for a restaurant using Python and Tkinter.

**Project**: `MyBillingSoftware`

**Short description**: A role-based POS-style application (Admin, Billing, Kitchen, Executive) that generates receipts, saves daily CSV reports, manages products and basic stock, and uses MySQL for persistence.

**Features**
- Admin login and role signup/login (admin can create roles).
- Create and manage bills: add items, calculate tax, generate, save, and print receipts.
- Save individual bills to `bills/<bill_number>.txt` and append to `bills/daily_bills_<YYYY-MM-DD>.csv`.
- Manage product catalog and stock, send orders to kitchen, and view monthly sales reports.

**Prerequisites**
- Python 3.8+ installed and available on `PATH`.
- MySQL server running and accessible.
- Recommended Python packages: `Pillow`, `mysql-connector-python`, `bcrypt`.

**Quick install (Windows PowerShell)**

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install pillow mysql-connector-python bcrypt
```

**Database setup**
1. Update DB credentials if you do not use `root` / `root` in `MyBillingSoftware/billing_software.py` (see `create_connection()` and `setup_database()`).
2. Run the included table-creation helper from the project root:

```powershell
python -c "import sys; sys.path.append('MyBillingSoftware'); from billing_software import setup_database; setup_database()"
```

This creates the `billing_system` tables used by the app.

**Run the app**
From the project root (where `MyBillingSoftware` and `bills/` are located):

```powershell
python MyBillingSoftware\billing_software.py
```

When the GUI opens:
- Use the Admin Sign Up to create the default admin (or use the provided `set_default_admin` flow).
- Use role selection to sign up or log in as `billing`, `kitchen`, or `executive` users.

**File structure (relevant files)**
- `MyBillingSoftware/billing_software.py` — main application code and GUI.
- `MyBillingSoftware/img/` — images used by the GUI (logo, banners).
- `bills/` — stored bills and daily CSV reports (app creates this folder automatically).

**Notes & tips**
- Change the MySQL credentials in `create_connection()` before using in production.
- If the app cannot connect to MySQL, ensure the server is running and the DB `billing_system` exists or run `setup_database()`.
- The app writes CSVs named `bills/daily_bills_YYYY-MM-DD.csv` which you can open in Excel.

If you want, I can also:
- Add a `requirements.txt` or `pyproject.toml`.
- Add a small CLI wrapper to run `setup_database()` more easily.
- Create a minimal `start.bat` or PowerShell script to set up the venv and run the app.

---
Written to help you get started quickly. Let me know which optional items you'd like me to add.
