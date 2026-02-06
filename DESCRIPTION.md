Malabar Family Restaurant — Billing System

A desktop billing application for restaurants built with Python and Tkinter.

Purpose
- Provide a simple point-of-sale and billing interface for a small restaurant.
- Allow multiple roles (admin, billing, kitchen, executive) with separate interfaces.
- Save individual bills as text files and append daily records to CSV reports.

Key features
- Admin login/signup and role-based access (billing, kitchen, executive).
- Add products to a bill, calculate tax, generate and print receipts.
- Save bills to `bills/<bill_number>.txt` and append daily summaries to `bills/daily_bills_<YYYY-MM-DD>.csv`.
- Manage product catalog, stock, and orders for kitchen staff.
- View daily CSV reports in a GUI treeview and monthly aggregated reports stored in a MySQL table.

Implementation notes
- UI: Tkinter (desktop GUI)
- Images: `MyBillingSoftware/img/` (logo and decorative images)
- Database: MySQL (default connection uses `host=localhost user=root password=root database=billing_system`)
- Password hashing: `bcrypt`
- Image handling: `Pillow` (PIL)

Where files are stored
- Bills and daily CSVs: `bills/` (created automatically by the app)
- Application code: `MyBillingSoftware/billing_software.py`

Short troubleshooting
- If images do not load, check `MyBillingSoftware/img/` paths.
- Ensure MySQL server is running and credentials in `create_connection()` are updated.
- Use the included `setup_database()` function to create required tables in the `billing_system` database.

Contact
- For help or to request features, edit and extend the code in `MyBillingSoftware/` or open an issue in your local issue tracker.