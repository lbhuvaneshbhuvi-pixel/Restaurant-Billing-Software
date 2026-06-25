from tkinter import *
from tkinter import ttk
from tkinter import Tk, Label, Button, Frame, messagebox, StringVar, Toplevel
import random
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import tempfile
from time import strftime
import csv
import datetime
import mysql.connector
from mysql.connector import Error
import bcrypt
import mysql.connector

def setup_database():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bhuvi',
            database='billing_system'
        )
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Create bills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bill_number VARCHAR(50) NOT NULL,
                customer_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(50) NOT NULL,
                email VARCHAR(255) NOT NULL,
                sub_total DECIMAL(10, 2) NOT NULL,
                tax DECIMAL(10, 2) NOT NULL,
                total DECIMAL(10, 2) NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                status VARCHAR(50) NOT NULL
            );
        ''')
        
        # Create monthly reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                month_year VARCHAR(7) NOT NULL,
                total_bills DECIMAL(10, 2) NOT NULL,
                total_income DECIMAL(10, 2) NOT NULL,
                total_orders INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Create admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(60) NOT NULL
            );
        ''')

        # Create billing table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS billing (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Create executive table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS executive (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        # Create kitchen table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kitchen (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        print("Database setup completed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bhuvi',  # MySQL password
            database='billing_system'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print('MySQL connection is closed')

# ─────────────────────────────────────────────────────────────────────────────
# PREMIUM ADMIN LOGIN WINDOW  ─  Dark glassmorphism theme
# ─────────────────────────────────────────────────────────────────────────────
class AdminLoginWindow:
    # Colour palette
    BG          = "#0d0f1a"   # deep navy background
    CARD_BG     = "#1a1d2e"   # card surface
    CARD_BORDER = "#2a2d3e"   # card border
    ACCENT      = "#7c3aed"   # violet accent
    ACCENT_HOV  = "#6d28d9"   # hover shade
    ACCENT2     = "#06b6d4"   # cyan highlight
    FG_MAIN     = "#f1f5f9"   # primary text
    FG_MUTED    = "#94a3b8"   # secondary text
    INPUT_BG    = "#0f1120"   # input background
    SUCCESS     = "#10b981"   # green
    ERROR       = "#ef4444"   # red

    def __init__(self, root):
        self.root = root
        self.root.title("Malabar Family Restaurant – Admin Portal")
        self.root.geometry("1280x800")
        self.root.resizable(True, True)
        self.root.configure(bg=self.BG)

        self.username = StringVar()
        self.password = StringVar()
        self._build_ui()

    # ------------------------------------------------------------------
    def _build_ui(self):
        # ── Left decorative panel ──────────────────────────────────────
        left = Frame(self.root, bg="#12152b", width=560)
        left.pack(side=LEFT, fill=Y)
        left.pack_propagate(False)

        # Brand block inside left panel
        brand_wrap = Frame(left, bg="#12152b")
        brand_wrap.place(relx=0.5, rely=0.42, anchor=CENTER)

        # Coloured accent bar
        Frame(brand_wrap, bg=self.ACCENT, height=4, width=60).pack(anchor=W, pady=(0, 12))

        Label(brand_wrap, text="MALABAR",
              font=("Helvetica", 36, "bold"), bg="#12152b",
              fg=self.FG_MAIN).pack(anchor=W)
        Label(brand_wrap, text="Family Restaurant",
              font=("Helvetica", 18), bg="#12152b",
              fg=self.ACCENT2).pack(anchor=W)

        Frame(brand_wrap, bg=self.CARD_BORDER, height=1, width=280).pack(anchor=W, pady=18)

        Label(brand_wrap, text="Admin Control Panel",
              font=("Helvetica", 12), bg="#12152b",
              fg=self.FG_MUTED).pack(anchor=W)
        Label(brand_wrap,
              text="Manage roles, billing & kitchen operations",
              font=("Helvetica", 10), bg="#12152b",
              fg="#475569", wraplength=320, justify=LEFT).pack(anchor=W, pady=4)

        # Footer note
        Label(left, text="© 2025 Malabar Restaurant. All rights reserved.",
              font=("Helvetica", 8), bg="#12152b",
              fg="#334155").place(relx=0.5, rely=0.97, anchor=CENTER)

        # ── Right login card ───────────────────────────────────────────
        right = Frame(self.root, bg=self.BG)
        right.pack(side=RIGHT, fill=BOTH, expand=True)

        card = Frame(right, bg=self.CARD_BG,
                     highlightbackground=self.CARD_BORDER,
                     highlightthickness=1, padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Card header
        Label(card, text="Welcome back",
              font=("Helvetica", 22, "bold"),
              bg=self.CARD_BG, fg=self.FG_MAIN).pack(anchor=W)
        Label(card, text="Sign in to your admin account",
              font=("Helvetica", 11),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W, pady=(4, 24))

        # Username field
        Label(card, text="USERNAME",
              font=("Helvetica", 9, "bold"),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W)
        self._entry(card, self.username, False).pack(fill=X, pady=(4, 16))

        # Password field
        Label(card, text="PASSWORD",
              font=("Helvetica", 9, "bold"),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W)
        self._entry(card, self.password, True).pack(fill=X, pady=(4, 28))

        # Login button
        btn = Button(card, text="Sign In  →",
                     command=self.login,
                     bg=self.ACCENT, fg="white",
                     font=("Helvetica", 12, "bold"),
                     relief=FLAT, cursor="hand2",
                     padx=20, pady=10, width=26)
        btn.pack(fill=X)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.ACCENT_HOV))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.ACCENT))

        # Status label (shows errors inline)
        self.status_lbl = Label(card, text="",
                                font=("Helvetica", 10),
                                bg=self.CARD_BG, fg=self.ERROR)
        self.status_lbl.pack(pady=(12, 0))

        # Divider + hint
        Frame(card, bg=self.CARD_BORDER, height=1, width=320).pack(pady=20)
        Label(card,
              text="Default credentials: admin / admin123",
              font=("Helvetica", 9),
              bg=self.CARD_BG, fg="#334155").pack()

    # ------------------------------------------------------------------
    def _entry(self, parent, var, is_pass):
        """Create a styled dark entry widget."""
        e = Entry(parent, textvariable=var,
                  show="●" if is_pass else "",
                  font=("Helvetica", 13),
                  bg=self.INPUT_BG, fg=self.FG_MAIN,
                  insertbackground=self.ACCENT2,
                  relief=FLAT,
                  highlightbackground=self.CARD_BORDER,
                  highlightthickness=1,
                  width=30)
        if is_pass:
            e.bind("<Return>", lambda ev: self.login())
        return e

    # ------------------------------------------------------------------
    def load_image(self, path):
        try:
            img = Image.open(path)
            img = img.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = Label(self.root, image=photo, bg=self.BG)
            label.image = photo
            label.place(x=300, y=100)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        self.status_lbl.config(text="Authenticating…", fg=self.ACCENT2)
        self.root.update()

        if not username or not password:
            self.status_lbl.config(text="⚠  Username and password are required.", fg=self.ERROR)
            return

        conn = create_connection()
        if conn is None:
            self.status_lbl.config(text="⚠  Database connection failed.", fg=self.ERROR)
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM admins WHERE username=%s", (username,))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                self.status_lbl.config(text="✔  Login successful!", fg=self.SUCCESS)
                self.root.after(400, lambda: [
                    self.show_role_login_signup(),
                    self.root.withdraw()
                ])
            else:
                self.status_lbl.config(text="✘  Invalid username or password.", fg=self.ERROR)
        except mysql.connector.Error as err:
            self.status_lbl.config(text=f"DB Error: {err}", fg=self.ERROR)
        finally:
            cursor.close()
            close_connection(conn)

    # ------------------------------------------------------------------
    def show_role_login_signup(self):
        """Premium role selection / sign-up window."""
        win = Toplevel(self.root)
        win.title("Role Access – Malabar Restaurant")
        win.geometry("900x620")
        win.configure(bg=self.BG)
        win.resizable(False, False)
        self._staff_portal_win = win  # Keep reference for back_to_home navigation

        self.role     = StringVar(value="billing")
        self.username = StringVar()
        self.password = StringVar()

        # ── Header strip ──────────────────────────────────────────────
        hdr = Frame(win, bg="#12152b", height=70)
        hdr.pack(fill=X)
        Label(hdr, text="Malabar Restaurant  ›  Staff Portal",
              font=("Helvetica", 14, "bold"),
              bg="#12152b", fg=self.FG_MAIN).place(x=30, rely=0.5, anchor=W)

        # ── Role selector row ─────────────────────────────────────────
        role_strip = Frame(win, bg=self.BG, pady=18)
        role_strip.pack(fill=X)
        Label(role_strip, text="Select Your Role",
              font=("Helvetica", 11, "bold"),
              bg=self.BG, fg=self.FG_MUTED).pack(side=LEFT, padx=30)

        roles = ["billing", "kitchen", "executive"]
        role_colors = {"billing": "#7c3aed", "kitchen": "#f59e0b", "executive": "#06b6d4"}
        self._role_btns = {}
        for r in roles:
            b = Button(role_strip, text=r.upper(),
                       font=("Helvetica", 10, "bold"),
                       bg=role_colors[r] if r == "billing" else self.CARD_BG,
                       fg="white",
                       relief=FLAT, padx=18, pady=8, cursor="hand2",
                       command=lambda rv=r: self._select_role(rv, role_colors))
            b.pack(side=LEFT, padx=6)
            self._role_btns[r] = b
        self._role_colors = role_colors

        # ── Login card ────────────────────────────────────────────────
        card = Frame(win, bg=self.CARD_BG,
                     highlightbackground=self.CARD_BORDER,
                     highlightthickness=1, padx=60, pady=40)
        card.place(relx=0.5, rely=0.58, anchor=CENTER)

        Label(card, text="Staff Login / Sign Up",
              font=("Helvetica", 18, "bold"),
              bg=self.CARD_BG, fg=self.FG_MAIN).pack(anchor=W)
        Label(card, text="Enter your credentials for your assigned role",
              font=("Helvetica", 10),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W, pady=(4, 22))

        Label(card, text="USERNAME",
              font=("Helvetica", 9, "bold"),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W)
        self._entry(card, self.username, False).pack(fill=X, pady=(4, 14))

        Label(card, text="PASSWORD",
              font=("Helvetica", 9, "bold"),
              bg=self.CARD_BG, fg=self.FG_MUTED).pack(anchor=W)
        self._entry(card, self.password, True).pack(fill=X, pady=(4, 24))

        btn_row = Frame(card, bg=self.CARD_BG)
        btn_row.pack(fill=X)

        def _styled_btn(parent, text, cmd, color):
            b = Button(parent, text=text, command=cmd,
                       bg=color, fg="white",
                       font=("Helvetica", 11, "bold"),
                       relief=FLAT, padx=16, pady=9, cursor="hand2")
            b.pack(side=LEFT, expand=True, fill=X, padx=(0, 6))
            hov = self._darken(color)
            b.bind("<Enter>", lambda e: b.config(bg=hov))
            b.bind("<Leave>", lambda e: b.config(bg=color))
            return b

        _styled_btn(btn_row, "Login",   self.role_login,  self.ACCENT)
        _styled_btn(btn_row, "Sign Up", self.role_signup, self.SUCCESS)

        self.role_status = Label(card, text="",
                                 font=("Helvetica", 10),
                                 bg=self.CARD_BG, fg=self.ERROR)
        self.role_status.pack(pady=(12, 0))

        # Back button
        back = Button(win, text="← Back to Admin Login",
                      command=lambda: self.back_to_admin(win),
                      bg=self.BG, fg=self.FG_MUTED,
                      font=("Helvetica", 10),
                      relief=FLAT, cursor="hand2")
        back.place(x=20, y=580)
        back.bind("<Enter>", lambda e: back.config(fg=self.FG_MAIN))
        back.bind("<Leave>", lambda e: back.config(fg=self.FG_MUTED))

    # ------------------------------------------------------------------
    def _select_role(self, role, colors):
        self.role.set(role)
        for r, b in self._role_btns.items():
            b.config(bg=colors[r] if r == role else self.CARD_BG)

    @staticmethod
    def _darken(hex_color):
        """Return a slightly darker shade of the given hex colour."""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            factor = 0.80
            return "#{:02x}{:02x}{:02x}".format(
                int(r*factor), int(g*factor), int(b*factor))
        except Exception:
            return hex_color

    # ------------------------------------------------------------------
    def back_to_admin(self, role_selection_window):
        role_selection_window.destroy()
        self.root.deiconify()

    def role_login(self):
        role = self.role.get()
        username = self.username.get()
        password = self.password.get()

        conn = create_connection()
        if conn is None:
            messagebox.showerror("Error", "Could not connect to the database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT password FROM {role} WHERE username=%s", (username,))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                messagebox.showinfo("Success", f"Logged in as {role.capitalize()}")
                # Find the staff portal window (the Toplevel that called role_login)
                staff_portal_win = self._staff_portal_win
                # Open the respective application based on the role
                if role == "billing":
                    self.open_billing_app(staff_portal_win)
                elif role == "kitchen":
                    self.open_kitchen_app(staff_portal_win)
                elif role == "executive":
                    self.open_executive_app(staff_portal_win)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            cursor.close()
            close_connection(conn)

    def role_signup(self):
        role = self.role.get()
        username = self.username.get()
        password = self.password.get()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = create_connection()
        if conn is None:
            messagebox.showerror("Error", "Could not connect to the database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {role} (username, password) VALUES (%s, %s)", 
                           (username, hashed_password.decode('utf-8')))
            conn.commit()
            messagebox.showinfo("Success", f"{role.capitalize()} signed up successfully!")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", f"{role.capitalize()} username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sign up: {str(e)}")
        finally:
            cursor.close()
            close_connection(conn)

    def open_billing_app(self, staff_portal_win):
        staff_portal_win.withdraw()  # Hide the staff portal
        billing_window = Toplevel(self.root)
        Bill_App(billing_window, staff_portal_win)  # Pass staff portal reference

    def open_kitchen_app(self, staff_portal_win):
        staff_portal_win.withdraw()  # Hide the staff portal
        kitchen_window = Toplevel(self.root)
        KitchenApp(kitchen_window, staff_portal_win)  # Pass staff portal reference

    def open_executive_app(self, staff_portal_win):
        staff_portal_win.withdraw()  # Hide the staff portal
        executive_window = Toplevel(self.root)
        ExecutiveApp(executive_window, staff_portal_win)  # Pass staff portal reference


class AdminSignupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Sign Up")
        self.root.geometry("1980x1080")

        # Default credentials
        self.default_username = "admin"
        self.default_password = "admin123"  # Change this to a secure password

        Label(self.root, text="Default Admin Username:").pack(pady=10)
        Label(self.root, text=self.default_username).pack(pady=5)
        Label(self.root, text="Default Admin Password:").pack(pady=10)
        Label(self.root, text=self.default_password).pack(pady=5)

        Button(self.root, text="Set Default Admin", command=self.set_default_admin).pack(pady=20)

    def set_default_admin(self):
        hashed_password = bcrypt.hashpw(self.default_password.encode('utf-8'), bcrypt.gensalt())

        conn = create_connection()
        if conn is None:
            messagebox.showerror("Error", "Could not connect to the database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", 
                           (self.default_username, hashed_password.decode('utf-8')))
            conn.commit()
            messagebox.showinfo("Success", "Default admin set successfully!")
            self.root.destroy()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Admin username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set default admin: {str(e)}")
        finally:
            cursor.close()
            close_connection(conn)




class Bill_App:
    def __init__(self, root, staff_portal_win=None):
        self.root = root
        self.staff_portal_win = staff_portal_win  # Reference to staff portal window
        self.root.geometry("1980x1080")
        self.root.title("Malabar Family Restaurant")
        self.input_value = True
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize billing UI
        self.setup_ui()

    def setup_ui(self):
        # Variables
        self.c_name = StringVar()
        self.c_phon = StringVar()
        self.c_email = StringVar()
        self.search_bill = StringVar()
        self.product = StringVar()
        self.prices = IntVar()
        self.qty = IntVar()
        self.sub_total = StringVar()
        self.tax_input = StringVar()
        self.total = StringVar()
        
        self.l = []
        
        # Product Categories
        self.categories = {
            "Starter": {
                "Veg Starter": {
                    "Gobi 65": 80,
                    "Paneer Hot Pepper": 130,
                    "Paneer Maharani": 120
                },
                "Non-Veg Starter": {
                    "Chicken Pallipalayam": 160,
                    "Hyderabadi Chicken 65": 140,
                    "Chicken Chettinadu Dry": 170
                }
            },
            "Main Course": {
                "Veg": {
                    "Veg Fried Rice": 70,
                    "Paneer Fried Rice": 90,
                    "Gobi Rice": 90,
                    "Mushroom Fried Rice": 130
                },
                "Non-Veg": {
                    "Chicken Biryani": 120,
                    "Chicken Fried Rice": 90,
                    "Chicken Noodles": 90,
                    "Nallampatti Chicken Rice": 150
                }
            },
            "Dessert&Drinks": {
                "Ice Cream": {
                    "Chocolate": 50,
                    "Butterscotch": 55,
                    "Vennila": 45
                },
                "Mojitos": {
                    "Blue virgin": 80,
                    "Paan": 80,
                    "Bubblegum": 70
                },
                "Milk Shakes": {
                    "Tender Coconut": 110,
                    "Oreo": 100,
                    "Dry Fruits": 140
                }
            }
        }

        # ===============Images==================================
        self.load_image("img/girl1.jpg", (800, 200), 0, 0)  # Changed width to 600
        self.load_image("img/girl2.jpg", (800, 200), 500, 0)  # Changed width to 600
        self.load_image("img/girl3.jpg", (800, 200), 1000, 0)  # Changed width to 600

        
        
        # ==================== Project title ==================================================
        title = Label(self.root, text="Malabar Family Restaurant", font=("times new roman", 30, "bold"), bg="white", fg="red")
        title.place(x=0, y=0, width=1540, height=45)

        # Time Label
        lbl = Label(title, font=('times new roman', 16, 'bold'), background='white', foreground='blue') 
        lbl.place(x=0, y=(-15), width=120, height=50) 
        self.time(lbl)

        self.bg_color = "white"

        Main_Frame = Frame(self.root, bd=5, relief=GROOVE, bg=self.bg_color)
        Main_Frame.place(x=0, y=100, width=1535, height=620)

        # Customer LabelFrame
        CustFrame = LabelFrame(Main_Frame, text="Customer", bg=self.bg_color, fg="red", font=("arial", 16, "bold"))
        CustFrame.place(x=10, y=0, width=350, height=140)
        
        self.lblMobile = Label(CustFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Mobile No.", bd=4)
        self.lblMobile.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.txtMobile = ttk.Entry(CustFrame, font=('arial', 10, 'bold'), textvariable=self.c_phon, width=24)
        self.txtMobile.grid(row=0, column=1, sticky=W, padx=5, pady=2)
    
        self.lblCustName = Label(CustFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Customer Name", bd=4)
        self.lblCustName.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.txtCustName = ttk.Entry(CustFrame, font=('arial', 10, 'bold'), textvariable=self.c_name, width=24)
        self.txtCustName.grid(row=1, column=1, sticky=W, padx=5, pady=2)

        self.lblEmail = Label(CustFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Email", bd=4)
        self.lblEmail.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.txtEmail = ttk.Entry(CustFrame, font=('arial', 10, 'bold'), textvariable=self.c_email, width=24)
        self.txtEmail.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        # Product LabelFrame
        ProductFrame = LabelFrame(Main_Frame, text="Item", bg=self.bg_color, fg="red", font=("arial", 14, "bold"))
        ProductFrame.place(x=370, y=0, width=620, height=140)

        # Search LabelFrame
        SerachFrame = Frame(Main_Frame, bd=2, bg="white")
        SerachFrame.place(x=1000, y=10, width=350, height=40)

        cbill_label = Label(SerachFrame, text="Bill Number", bg="red", fg="white", font=("times new roman", 14, "bold")).grid(row=0, column=0)
        cbill_txt = ttk.Entry(SerachFrame, width=12, textvariable=self.search_bill, font="arial 14").grid(row=0, column=1, padx=2)

        bill_btn = Button(SerachFrame, text="Search", command=self.find_bill, width=14, font="arial 11 bold", bg="orangered", fg="white").grid(row=0, column=2, padx=2)

        # MiddleFrame
        MiddleFrame = Frame(Main_Frame, bd=10)
        MiddleFrame.place(x=10, y=150, width=800, height=250)
        
        # Adjust the width of the images as needed
        self.load_image("img/briyani.jpg", (600, 350), 0, 0, MiddleFrame)  # Changed width to 600
        self.load_image("img/restaurant.jpg", (600, 300), 490, 0, MiddleFrame)  # Changed width to 500

        # ── Premium Bill Receipt Area ────────────────────────────────
        RightFrame = Frame(Main_Frame, bg="#0d0f1a",
                           highlightbackground="#7c3aed",
                           highlightthickness=2)
        RightFrame.place(x=870, y=140, width=480, height=260)

        # Header bar
        bill_hdr = Frame(RightFrame, bg="#7c3aed", height=32)
        bill_hdr.pack(fill=X)
        bill_hdr.pack_propagate(False)
        Label(bill_hdr, text="  🧾  BILL RECEIPT",
              font=("Courier", 11, "bold"),
              bg="#7c3aed", fg="white").pack(side=LEFT, padx=6, pady=4)

        scroll_y = Scrollbar(RightFrame, orient=VERTICAL,
                             troughcolor="#1a1d2e", bg="#2a2d3e")
        self.textarea = Text(RightFrame,
                             yscrollcommand=scroll_y.set,
                             bg="#0d0f1a", fg="#06b6d4",
                             font=("Courier", 11),
                             insertbackground="#7c3aed",
                             selectbackground="#7c3aed",
                             relief=FLAT, padx=10, pady=6)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH, expand=1)
        # Tag styles for the receipt
        self.textarea.tag_config("header",  foreground="#f1f5f9", font=("Courier", 12, "bold"))
        self.textarea.tag_config("divider", foreground="#334155")
        self.textarea.tag_config("label",   foreground="#94a3b8")
        self.textarea.tag_config("value",   foreground="#06b6d4", font=("Courier", 11, "bold"))
        self.textarea.tag_config("total",   foreground="#7c3aed", font=("Courier", 12, "bold"))

        self.lblCategories = Label(ProductFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Select Item", bd=4)
        self.lblCategories.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.ComboCategories = ttk.Combobox(ProductFrame, value=list(self.categories.keys()), font=('arial', 10, 'bold'), width=24, state="readonly")
        self.ComboCategories.grid(row=0, column=1, sticky=W, padx=5, pady=2)
        self.ComboCategories.current(0)
        self.ComboCategories.bind("<<ComboboxSelected>>", self.Categories)

        self.lblSubCategory = Label(ProductFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Category", bd=4)
        self.lblSubCategory.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.ComboSubCategory = ttk.Combobox(ProductFrame, state="readonly", value=[""], font=('arial', 10, 'bold'), width=24)
        self.ComboSubCategory.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        self.ComboSubCategory.current(0)
        self.ComboSubCategory.bind("<<ComboboxSelected>>", self.Product_Add)
        
        self.lblproduct = Label(ProductFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Item Name", bd=4)
        self.lblproduct.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.ComboProduct = ttk.Combobox(ProductFrame, value=[""], textvariable=self.product, state="readonly", font=('arial', 10, 'bold'), width=24)
        self.ComboProduct.grid(row=2, column=1, sticky=W, padx=5, pady=2)
        self.ComboProduct.bind("<<ComboboxSelected>>", self.price)

        self.lblPrice = Label(ProductFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Price", bd=4)
        self.lblPrice.grid(row=0, column=2, sticky=W, padx=5, pady=2)

        self.ComboPrice = ttk.Combobox(ProductFrame, state="readonly", textvariable=self.prices, value=[""], font=('arial', 10, 'bold'), width=24)
        self.ComboPrice.grid(row=0, column=3, sticky=W, padx=5, pady=2)

        self.lblQty = Label(ProductFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Qty", bd=4)
        self.lblQty.grid(row=1, column=2, sticky=W, padx=5, pady=2)

        self.ComboQty = ttk.Entry(ProductFrame, textvariable=self.qty, font=('arial', 10, 'bold'), width=26)
        self.ComboQty.grid(row=1, column=3, sticky=W, padx=5, pady=2)
    
       
        # Assuming you have a footer defined somewhere above this section
        footer = Label(self.root, text="Footer Content Here", bg="gray", fg="white", font=("Arial", 14))
        footer.pack(side=BOTTOM, fill=X)

        # BottomLabelFrame
        BottomFrame = LabelFrame(Main_Frame, text="Bill Counter", bd=2, bg='white', font=('arial', 16, 'bold'), fg="red", height=200)  # Reduced height
        BottomFrame.pack(side=BOTTOM, fill=X, padx=7, pady=7, ipadx=4, ipady=10)  # Adjusted ipady for internal padding

        # Total Product Price tax
        self.lblTotal = Label(BottomFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Sub Total", bd=4)
        self.lblTotal.grid(row=0, column=0, sticky=W, padx=5, pady=2)  # Column 0

        self.txtTotal = ttk.Entry(BottomFrame, textvariable=self.sub_total, font=('arial', 10, 'bold'), width=24)
        self.txtTotal.grid(row=0, column=1, sticky=W, padx=5, pady=2)  # Column 1

        self.lbl_tax = Label(BottomFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Gov Tax", bd=4)
        self.lbl_tax.grid(row=1, column=0, sticky=W, padx=5, pady=2)  # Column 0

        self.txt_tax = ttk.Entry(BottomFrame, textvariable=self.tax_input, font=('arial', 10, 'bold'), width=24)
        self.txt_tax.grid(row=1, column=1, sticky=W, padx=5, pady=2)  # Column 1

        self.lblAmountTotal = Label(BottomFrame, font=('arial', 14, 'bold'), bg=self.bg_color, text="Total", bd=4)
        self.lblAmountTotal.grid(row=2, column=0, sticky=W, padx=5, pady=2)  # Column 0

        self.txtAmountTotal = ttk.Entry(BottomFrame, textvariable=self.total, font=('arial', 10, 'bold'), width=24)
        self.txtAmountTotal.grid(row=2, column=1, sticky=W, padx=5, pady=2)  # Column 1

        # Create a Frame for buttons without a border
        btnFrame = Frame(BottomFrame, bg=self.bg_color)
        btnFrame.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

        # Button configuration
        button_config = {
            'bg': "orangered",
            'fg': "white",
            'font': ('arial', 14, 'bold'),
            'bd': 0,
            'relief': FLAT,
        }

        # Manage Catalog button
        self.btn_ManageCatalog = Button(btnFrame, height=1, text="Manage Catalog", command=self.manage_catalog, width=14, **button_config)
        self.btn_ManageCatalog.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Other buttons
        self.btn_AddToCart = Button(btnFrame, height=1, text="Add To Cart", command=self.iaddItem, width=14, **button_config)
        self.btn_AddToCart.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.btn_generate_bill = Button(btnFrame, height=1, text="Generate Bill", command=self.gen_bill, width=14, **button_config)
        self.btn_generate_bill.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.btn_save = Button(btnFrame, height=1, text="Save Bill", command=self.save_bill, width=14, **button_config)
        self.btn_save.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        self.btn_print = Button(btnFrame, height=1, text="Print", command=self.iPrint, width=14, **button_config)
        self.btn_print.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

        self.btn_Clear = Button(btnFrame, height=1, text="Clear", command=self.clear, width=14, **button_config)
        self.btn_Clear.grid(row=0, column=5, padx=5, pady=5, sticky='ew')

        self.btn_ViewReport = Button(btnFrame, height=1, text="Report", command=self.display_report, width=14, **button_config)
        self.btn_ViewReport.grid(row=0, column=6, padx=5, pady=5, sticky='ew')

        # Back to Home button in the same frame, after the Report button
        self.btn_BackToHome2 = Button(btnFrame, height=1, text="Back to Home", command=self.back_to_home, width=14, **button_config)
        self.btn_BackToHome2.grid(row=0, column=7, padx=5, pady=5, sticky='ew')

        # Move the View Monthly Sales button to a new row below the Back to Home button
        btn_ViewMonthlySales = Button(btnFrame, height=2, text="View Monthly Sales", command=self.view_monthly_sales, bg="orangered", fg="white", width=14)
        btn_ViewMonthlySales.grid(row=1, column=4, padx=5, pady=5, sticky='ew')  # Span across all columns for better alignment

        self.welcome()     

    def load_image(self, path, max_size, x, y, parent=None):
        if not os.path.exists(path):
            print(f"Image file not found: {path}")  # Debugging line
            return
        try:
            img = Image.open(path)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)  # Resize while maintaining aspect ratio
            photoImg = ImageTk.PhotoImage(img)
            bg_lbl = Label(parent if parent else self.root, image=photoImg)
            bg_lbl.image = photoImg  # Keep a reference to avoid garbage collection
            bg_lbl.place(x=x, y=y)
        except Exception as e:
            print(f"Error loading image: {e}")
            
    def time(self, lbl): 
        string = strftime('%H:%M:%S %p') 
        lbl.config(text=string) 
        lbl.after(1000, lambda: self.time(lbl))  # Use lambda to pass lbl

    def clear(self):
        self.textarea.delete(1.0, END)
        self.c_name.set("")
        self.c_phon.set("")
        self.c_email.set("")
        self.search_bill.set(str(random.randint(1000, 9999)))  # Reset to a new random bill number
        self.product.set("")
        self.prices.set(0)
        self.qty.set(0)
        self.l = [0]
        self.total.set("")
        self.sub_total.set("")
        self.tax_input.set('')
        self.welcome()
        
    def price(self, event):
        selected_product = self.ComboProduct.get()
        if selected_product:
            # Find the price of the selected product
            for category in self.categories.values():
                for subcategory in category.values():
                    if selected_product in subcategory:
                        self.prices.set(subcategory[selected_product])
                        break

        # In the setup_ui method, ensure you bind the price method correctly
        self.ComboProduct.bind("<<ComboboxSelected>>", self.price)

    def display_report(self):
        # Get today's date for the CSV file name
        today = datetime.date.today().strftime("%Y-%m-%d")
        csv_file_name = f"bills/daily_bills_{today}.csv"

        # Check if the file exists
        if not os.path.exists(csv_file_name):
            messagebox.showerror("Error", f"No report found for {today}.")
            return

        # Read the CSV content
        with open(csv_file_name, "r") as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

        # Display the content in a Treeview
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()  # Clear previous frame if exists

        self.report_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.report_frame.place(x=50, y=400, width=1450, height=300)

        tree = ttk.Treeview(self.report_frame, columns=rows[0], show="headings")
        tree.pack(fill=BOTH, expand=True)

        # Set column headings
        for col in rows[0]:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Insert rows into the Treeview
        for row in rows[1:]:
            tree.insert("", END, values=row)

        # Add a scrollbar
        scrollbar = Scrollbar(self.report_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        close_btn = Button(self.report_frame, text="Close Report", command=self.close_report, font=("Arial", 14, "bold"), bg="red", fg="white")
        close_btn.pack(side=BOTTOM, pady=5)

        messagebox.showinfo("Report", f"Displaying report for {today}.")
        
    def close_report(self):
        if hasattr(self, 'report_frame'):
            self.report_frame.destroy()

    def iPrint(self):
        q = self.textarea.get("1.0", "end-1c")
        filename = tempfile.mktemp(".txt")
        open(filename, "w").write(q)
        os.startfile(filename, "print")

    def welcome(self):
        self.textarea.delete(1.0, END)
        self.textarea.insert(END, " ╔══════════════════════════════════════╗\n", "divider")
        self.textarea.insert(END, "   MALABAR FAMILY RESTAURANT\n", "header")
        self.textarea.insert(END, "   Erode, Tamil Nadu\n", "label")
        self.textarea.insert(END, " ╚══════════════════════════════════════╝\n", "divider")
        self.textarea.insert(END, " Bill No : ", "label")
        self.textarea.insert(END, f"{self.search_bill.get()}\n", "value")
        self.textarea.insert(END, " Name    : ", "label")
        self.textarea.insert(END, f"{self.c_name.get()}\n", "value")
        self.textarea.insert(END, " Phone   : ", "label")
        self.textarea.insert(END, f"{self.c_phon.get()}\n", "value")
        self.textarea.insert(END, " Email   : ", "label")
        self.textarea.insert(END, f"{self.c_email.get()}\n", "value")
        self.textarea.insert(END, " ──────────────────────────────────────\n", "divider")
        self.textarea.insert(END, " Item                    QTY    Price\n", "header")
        self.textarea.insert(END, " ──────────────────────────────────────\n", "divider")

    def iaddItem(self):
        Tax = 2
        self.n = self.prices.get()
        self.m = self.qty.get() * self.n
        self.l.append(self.m)
        if self.product.get() == "":
            messagebox.showerror('Error', "Please Enter Mobile No. & Select The Product") 
        else:
            self.textarea.insert(END, f'\n {self.product.get()}\t\t\t{self.qty.get()} \t\t{self.m}')
            self.sub_total.set(str('Rs.%.2f' % (sum(self.l))))
            self.tax_input.set(str('Rs.%.2f' % ((((sum(self.l)) - (self.prices.get())) * Tax) / 100)))
            self.total.set(str('Rs.%.2f' % (((sum(self.l)) + ((((sum(self.l)) - (self.prices.get())) * Tax) / 100)))))

    def gen_bill(self):
        if self.product.get() == "":
            messagebox.showerror('Error', "Please Add To Cart Product")
        else:
            text = self.textarea.get(10.0, (10.0 + float(len(self.l))))
            self.welcome()  # This will include the bill number
            self.textarea.insert(END, text)
            self.textarea.insert(END, " ──────────────────────────────────────\n", "divider")
            self.textarea.insert(END, " Sub Total : ", "label")
            self.textarea.insert(END, f"{self.sub_total.get()}\n", "value")
            self.textarea.insert(END, " Tax (Govt): ", "label")
            self.textarea.insert(END, f"{self.tax_input.get()}\n", "value")
            self.textarea.insert(END, " ══════════════════════════════════════\n", "divider")
            self.textarea.insert(END, " TOTAL     : ", "label")
            self.textarea.insert(END, f"{self.total.get()}\n", "total")
            self.textarea.insert(END, " ══════════════════════════════════════\n", "divider")
            self.textarea.insert(END, "  Thank you! Visit again 🙏\n", "header")

    def get_bill_data(self):
        return f"Bill Number: {self.search_bill.get()}\n" \
            f"Customer Name: {self.c_name.get()}\n" \
            f"Phone: {self.c_phon.get()}\n" \
            f"Email: {self.c_email.get()}\n" \
            f"Sub Total: {self.sub_total.get()}\n" \
            f"Tax: {self.tax_input.get()}\n" \
            f"Total: {self.total.get()}\n"    
      
    def save_bill(self):
        # Ensure the 'bills' directory exists
        if not os.path.exists("bills"):
            os.makedirs("bills")

        # Save the bill to an individual text file
        bill_data = self.get_bill_data()
        with open(f"bills/{str(self.search_bill.get())}.txt", "w") as bill_file:
            bill_file.write(bill_data)

        # Append the bill data to a daily CSV file
        today = datetime.date.today().strftime("%Y-%m-%d")
        csv_file_name = f"bills/daily_bills_{today}.csv"

        # Extract bill data for CSV
        bill_data_list = [
            self.search_bill.get(),
            self.c_name.get(),
            self.c_phon.get(),
            self.c_email.get(),
            self.sub_total.get(),
            self.tax_input.get(),
            self.total.get(),
        ]

        # Check if the CSV file already exists
        file_exists = os.path.isfile(csv_file_name)

        # Write to CSV file
        with open(csv_file_name, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(["Bill Number", "Customer Name", "Phone Number", "Email", "Sub Total", "Tax", "Total"])
            writer.writerow(bill_data_list)

        # Show confirmation message
        messagebox.showinfo("Saved", f"Bill No: {self.search_bill.get()} saved successfully.\n"
                                    f"Data also stored in {csv_file_name}.")

    def find_bill(self):
        present = "no"
        for i in os.listdir("bills/"):
            if i.split(".")[0] == self.search_bill.get():
                f1 = open(f"bills/{i}", "r")
                self.textarea.delete("1.0", END)
                for d in f1:
                    self.textarea.insert(END, d)
                f1.close()
                present = "yes"
        if present == "no":
            messagebox.showerror("Error", "Invalid Bill No.")

    def Categories(self, event=""):
        selected_category = self.ComboCategories.get()
        if selected_category in self.categories:
            subcategories = list(self.categories[selected_category].keys())
            self.ComboSubCategory.config(value=subcategories)
            self.ComboSubCategory.current(0)

    def Product_Add(self, event=""):
        selected_subcategory = self.ComboSubCategory.get()
        if selected_subcategory in self.categories[self.ComboCategories.get()]:
            products = list(self.categories[self.ComboCategories.get()][selected_subcategory].keys())
            self.ComboProduct.config(value=products)
            self.ComboProduct.current(0)
    
    def view_monthly_sales(self):
        # Create a new window for the monthly sales report
        report_window = Toplevel(self.root)
        report_window.title("Monthly Sales Report")
        report_window.geometry("800x600")

        # Create a Treeview to display the monthly sales report
        columns = ("Month-Year", "Total Bills", "Total Income", "Total Orders")
        self.tree = ttk.Treeview(report_window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=BOTH, expand=True)

        # Load monthly sales data
        self.load_monthly_sales()

    def load_monthly_sales(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT month_year, total_bills, total_income, total_orders FROM monthly_reports")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load monthly sales: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    
    def update_monthly_sales(self):
        today = datetime.date.today()
        month_year = today.strftime("%Y-%m")  # Format: YYYY-MM

        # Calculate total sales for the current month
        total_bills = 1  # This should be the count of bills for the month
        total_income = float(self.total.get().replace("Rs.", "").replace(",", "").strip())  # Get the total income from the bill
        total_orders = len(self.l)  # Assuming self.l contains the list of products sold

        conn = create_connection()
        if conn is None:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monthly_reports WHERE month_year=%s", (month_year,))
            result = cursor.fetchone()

            if result:
                # Update existing record
                cursor.execute("""
                    UPDATE monthly_reports 
                    SET total_bills = total_bills + %s, 
                        total_income = total_income + %s, 
                        total_orders = total_orders + %s 
                    WHERE month_year = %s
                """, (total_bills, total_income, total_orders, month_year))
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO monthly_reports (month_year, total_bills, total_income, total_orders) 
                    VALUES (%s, %s, %s, %s)
                """, (month_year, total_bills, total_income, total_orders))

            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update monthly sales: {str(e)}")
        finally:
            cursor.close()
            close_connection(conn)



    def manage_catalog(self):
        catalog_window = Toplevel(self.root)
        catalog_window.title("Manage Catalog")
        catalog_window.geometry("400x400")

        new_category = StringVar()
        new_subcategory = StringVar()
        new_product = StringVar()
        new_price = StringVar()  # Use StringVar for price to handle input as string

        Label(catalog_window, text="Select Item", font=("Arial", 14)).pack(pady=5)
        category_combobox = ttk.Combobox(catalog_window, textvariable=new_category, state="readonly", font=("Arial", 12),
                                          values=list(self.categories.keys()))
        category_combobox.pack(pady=5)

        Label(catalog_window, text="Subcategory", font=("Arial", 14)).pack(pady=5)
        subcategory_combobox = ttk.Combobox(catalog_window, textvariable=new_subcategory, state="readonly", font=("Arial", 12))
        subcategory_combobox.pack(pady=5)

        # Bind the event to load subcategories
        category_combobox.bind("<<ComboboxSelected>>", lambda event: self.load_subcategories(new_category, subcategory_combobox))

        Label(catalog_window, text="Item Name", font=("Arial", 14)).pack(pady=5)
        ttk.Entry(catalog_window, textvariable=new_product, font=("Arial", 12)).pack(pady=5)

        Label(catalog_window, text="Price", font=("Arial", 14)).pack(pady=5)
        ttk.Entry(catalog_window, textvariable=new_price, font=("Arial", 12)).pack(pady=5)

        Button(catalog_window, text="Add Product", command=lambda: self.add_product(new_category, new_subcategory, new_product, new_price, catalog_window), font=("Arial", 12), bg="orangered", fg="white").pack(pady=20)

        Label(catalog_window, text="Remove Product", font=("Arial", 14)).pack(pady=10)
        Button(catalog_window, text="Remove Product", command=lambda: self.remove_product(new_category, new_subcategory, new_product, catalog_window), font=("Arial", 12), bg="orangered", fg="white").pack(pady=20)

    def load_subcategories(self, new_category, subcategory_combobox):
        selected_item = new_category.get()
        if selected_item in self.categories:
            subcategory_combobox["values"] = list(self.categories[selected_item].keys())
        else:
            subcategory_combobox["values"] = []
        subcategory_combobox.set("")  # Clear previous selection

    def add_product(self, new_category, new_subcategory, new_product, new_price, catalog_window):
        item = new_category.get()
        category = new_subcategory.get()
        product_name = new_product.get()
        price = new_price.get()

        # Validate inputs
        if item and category and product_name and price:
            try:
                price = float(price)  # Convert price to float
                if item not in self.categories:
                    self.categories[item] = {}
                if category not in self.categories[item]:
                    self.categories[item][category] = {}
                self.categories[item][category][product_name] = price
                messagebox.showinfo("Success", "Product added successfully!")
                catalog_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Price must be a number.")
        else:
            messagebox.showerror("Error", "Please fill all fields correctly.")

    def remove_product(self, new_category, new_subcategory, new_product, catalog_window):
        item = new_category.get()
        category = new_subcategory.get()
        product_name = new_product.get()

        if item in self.categories and category in self.categories[item] and product_name in self.categories[item][category]:
            del self.categories[item][category][product_name]
            messagebox.showinfo("Success", "Product removed successfully!")
            catalog_window.destroy()
        else:
            messagebox.showerror("Error", "Product not found.")

    def back_to_home(self):
        self.root.destroy()  # Close the billing window
        if self.staff_portal_win and self.staff_portal_win.winfo_exists():
            self.staff_portal_win.deiconify()  # Show the staff portal again
        else:
            # Fallback: open a new admin login if staff portal is gone
            main_window = Tk()
            AdminLoginWindow(main_window)
            main_window.mainloop()





class KitchenApp:
    def __init__(self, root, staff_portal_win=None):
        self.root = root
        self.staff_portal_win = staff_portal_win  # Reference to staff portal window
        self.root.geometry("1980x1080")
        self.root.title("Kitchen Application")
        self.create_ui()

    def create_ui(self):
        # Create UI components for the kitchen application
        title = Label(self.root, text="Kitchen Dashboard", font=("times new roman", 30, "bold"), bg="white", fg="green")
        title.pack(pady=20)

        # Add buttons for managing orders
        Button(self.root, text="Accept Order", command=self.accept_order, bg="orangered", fg="white", font=("Arial", 14, 'bold')).pack(pady=10)
        Button(self.root, text="Refresh Orders", command=self.refresh_orders, bg="orangered", fg="white", font=("Arial", 14, 'bold')).pack(pady=10)
        Button(self.root, text="Manage Stock", command=self.open_stock_management, bg="orangered", fg="white", font=("Arial", 14, 'bold')).pack(pady=10)
        Button(self.root, text="Back to Home", command=self.back_to_home, bg="orangered", fg="white", font=("Arial", 14, 'bold')).pack(pady=10)

        # Create a Treeview to display orders
        self.tree = ttk.Treeview(self.root, columns=("Table Number", "Product Name", "Quantity"), show="headings")
        self.tree.heading("Table Number", text="Table Number")
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.pack(fill=BOTH, expand=True)

        # Load orders from the database
        self.load_orders()

    def load_orders(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT table_number, product, quantity FROM orders WHERE status='pending'")
            orders = cursor.fetchall()

            for order in orders:
                self.tree.insert("", "end", values=order)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def accept_order(self):
        selected_order = self.tree.selection()
        if selected_order:
            order_details = self.tree.item(selected_order)["values"]
            table_number = order_details[0]  # Get the table number instead of order ID
            product_name = order_details[1]
            quantity = order_details[2]

            # Check stock availability
            if not self.check_stock_availability(product_name, quantity):
                messagebox.showwarning("Insufficient Stock", f"Not enough stock for {product_name}.")
                return

            self.update_order_status(table_number)
            self.update_stock(product_name, quantity)  # Update stock after accepting the order
            messagebox.showinfo("Success", f"Order for Table {table_number} accepted.")
            self.load_orders()  # Refresh the order list
        else:
            messagebox.showwarning("Warning", "Please select an order to accept.")

    def check_stock_availability(self, product_name, quantity):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM stock WHERE item_name = %s", (product_name,))
            stock_quantity = cursor.fetchone()
            if stock_quantity and stock_quantity[0] >= quantity:
                return True
            else:
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check stock availability: {str(e)}")
            return False
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def update_order_status(self, table_number):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE orders SET status='accepted' WHERE table_number=%s", (table_number,))
            conn.commit()
            self.send_order_to_billing(table_number)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order status: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def send_order_to_billing(self, table_number):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT product, quantity FROM orders WHERE table_number=%s", (table_number,))
            order_details = cursor.fetchall()
            if order_details:
                for product_name, quantity in order_details:
                    print(f"Sending Order for Table {table_number} with {product_name} (Quantity: {quantity}) to billing app.")
                self.load_orders()  # Refresh the order list after sending
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send order to billing: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def update_stock(self, product_name, quantity):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE stock SET quantity = quantity - %s WHERE item_name = %s", (quantity, product_name))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update stock: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def refresh_orders(self):
        self.tree.delete(*self.tree.get_children())  # Clear the current order list
        self.load_orders()  # Reload orders from the database

    def back_to_home(self):
        self.root.destroy()  # Close the kitchen window
        if self.staff_portal_win and self.staff_portal_win.winfo_exists():
            self.staff_portal_win.deiconify()  # Show the staff portal again
        else:
            # Fallback: open a new admin login if staff portal is gone
            main_window = Tk()
            AdminLoginWindow(main_window)
            main_window.mainloop()

    def open_stock_management(self):
        stock_window = Toplevel(self.root)
        stock_window.title("Stock Management")
        stock_window.geometry("600x400")

        # Create UI components for stock management
        Label(stock_window, text="Stock Management", font=("times new roman", 20, "bold")).pack(pady=10)

        # Create a Treeview to display stock items
        self.stock_tree = ttk.Treeview(stock_window, columns=("Item Name", "Quantity"), show="headings")
        self.stock_tree.heading("Item Name", text="Item Name")
        self.stock_tree.heading("Quantity", text="Quantity")
        self.stock_tree.pack(fill=BOTH, expand=True)

        # Load stock items from the database
        self.load_stock()

        # Add buttons for stock management
        Button(stock_window, text="Add Stock", command=self.add_stock, bg="orangered", fg="white").pack(pady=10)
        Button(stock_window, text="Refresh Stock", command=self.load_stock, bg="orangered", fg="white").pack(pady=10)

    def load_stock(self):
        self.stock_tree.delete(*self.stock_tree.get_children())  # Clear the current stock list
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, quantity FROM stock")
            stock_items = cursor.fetchall()

            for item in stock_items:
                self.stock_tree.insert("", "end", values=item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load stock: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def add_stock(self):
        def submit_stock():
            item_name = item_name_entry.get()
            quantity = quantity_entry.get()
            if item_name and quantity.isdigit():
                try:
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO stock (item_name, quantity) VALUES (%s, %s)", (item_name, int(quantity)))
                    conn.commit()
                    messagebox.showinfo("Success", "Stock added successfully.")
                    stock_window.destroy()
                    self.load_stock()  # Refresh the stock list
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add stock: {str(e)}")
                finally:
                    if 'conn' in locals() and conn.is_connected():
                        cursor.close()
                        close_connection(conn)
            else:
                messagebox.showwarning("Warning", "Please enter valid item name and quantity.")

        stock_window = Toplevel(self.root)
        stock_window.title("Add Stock")
        stock_window.geometry("300x200")

        Label(stock_window, text="Item Name").pack(pady=5)
        item_name_entry = Entry(stock_window)
        item_name_entry.pack(pady=5)

        Label(stock_window, text="Quantity").pack(pady=5)
        quantity_entry = Entry(stock_window)
        quantity_entry.pack(pady=5)

        Button(stock_window, text="Submit", command=submit_stock, bg="orangered", fg="white").pack(pady=10)





class ExecutiveApp:
    def __init__(self, root, staff_portal_win=None):
        self.root = root
        self.staff_portal_win = staff_portal_win  # Reference to staff portal window
        self.root.geometry("1980x1080")
        self.root.title("Executive Application")
        self.cart = []  # To hold items added to the cart
        self.categories = {
            "Starter": {
                "Veg Starter": {
                    "Gobi 65": 80,
                    "Paneer Hot Pepper": 130,
                    "Paneer Maharani": 120
                },
                "Non-Veg Starter": {
                    "Chicken Pallipalayam": 160,
                    "Hyderabadi Chicken 65": 140,
                    "Chicken Chettinadu Dry": 170
                }
            },
            "Main Course": {
                "Veg": {
                    "Veg Fried Rice": 70,
                    "Paneer Fried Rice": 90,
                    "Gobi Rice": 90,
                    "Mushroom Fried Rice": 130
                },
                "Non-Veg": {
                    "Chicken Biryani": 120,
                    "Chicken Fried Rice": 90,
                    "Chicken Noodles": 90,
                    "Nallampatti Chicken Rice": 150
                }
            },
            "Dessert&Drinks": {
                "Ice Cream": {
                    "Chocolate": 50,
                    "Butterscotch": 55,
                    "Vennila": 45
                },
                "Mojitos": {
                    "Blue virgin": 80,
                    "Paan": 80,
                    "Bubblegum": 70
                },
                "Milk Shakes": {
                    "Tender Coconut": 110,
                    "Oreo": 100,
                    "Dry Fruits": 140
                }
            }
        }
        self.create_ui()

    def create_ui(self):
        # Title with shadow effect
        title_bg_color = "#f8f9fa"  # Light background color
        title_fg_color = "#dc3545"   # Bootstrap red color

        # Create a shadow effect for the title
        shadow_title = Label(self.root, text="Executive Dashboard", font=("Arial", 32, "bold"), bg=title_bg_color, fg="lightgray")
        shadow_title.grid(row=0, column=0, columnspan=3, pady=20, padx=2)  # Slightly offset

        # Main title
        title = Label(self.root, text="Executive Dashboard", font=("Arial", 32, "bold"), bg=title_bg_color, fg=title_fg_color)
        title.grid(row=0, column=0, columnspan=3, pady=20)



        # Buttons with shadow effect
        button_bg_color = "orangered"
        button_fg_color = "white"
        button_font = ("Arial", 16, 'bold')

        # Create shadow buttons
        shadow_button1 = Button(self.root, text="Manage Catalog", command=self.open_manage_catalog, width=15, bg="lightgray", fg="lightgray", font=button_font)
        shadow_button1.grid(row=1, column=0, pady=10, padx=10)
        
        shadow_button2 = Button(self.root, text="Add to Cart", command=self.add_to_cart, width=15, bg="lightgray", fg="lightgray", font=button_font)
        shadow_button2.grid(row=1, column=1, pady=10, padx=10)
        
        shadow_button3 = Button(self.root, text="Send to Kitchen", command=self.send_to_kitchen, width=15, bg="lightgray", fg="lightgray", font=button_font)
        shadow_button3.grid(row=1, column=2, pady=10, padx=10)

        # Main buttons
        Button(self.root, text="Manage Catalog", command=self.open_manage_catalog, width=20, bg=button_bg_color, fg=button_fg_color, font=button_font).grid(row=1, column=0, pady=10, padx=10)
        Button(self.root, text="Add to Cart", command=self.add_to_cart, width=20, bg=button_bg_color, fg=button_fg_color, font=button_font).grid(row=1, column=1, pady=10, padx=10)
        Button(self.root, text="Send to Kitchen", command=self.send_to_kitchen, width=20, bg=button_bg_color, fg=button_fg_color, font=button_font).grid(row=1, column=2, pady=10, padx=10)
        Button(self.root, text="Back to Home", command=self.back_to_home, width=20, bg=button_bg_color, fg=button_fg_color, font=button_font).grid(row=2, column=1, pady=10, padx=10)

        # Continue with the rest of your UI setup...
        # Create a style for the Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))  # Set the font for the Treeview
        style.configure("Treeview.Heading", font=("Arial", 14, 'bold'))  # Set the font for the headings
        
        # Create a smaller Treeview for the cart
        self.cart_tree = ttk.Treeview(self.root, columns=("Product Name", "Price", "Quantity"), show="headings", height=2)  # Set height to 2 rows
        self.cart_tree.heading("Product Name", text="Product Name")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Quantity", text="Quantity")

        # Set column widths
        self.cart_tree.column("Product Name", width=150)  # Set width for Product Name column
        self.cart_tree.column("Price", width=80)          # Set width for Price column
        self.cart_tree.column("Quantity", width=80)       # Set width for Quantity column

        self.cart_tree.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # Add a scrollbar to the cart Treeview
        cart_scrollbar = Scrollbar(self.root, orient="vertical", command=self.cart_tree.yview)
        cart_scrollbar.grid(row=3, column=3, sticky='ns')
        self.cart_tree.configure(yscroll=cart_scrollbar.set)

        self.load_items()
        self.create_product_selection_frame()

        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(3, weight=1)  # Allow the cart Treeview to expand
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        

    def create_product_selection_frame(self):
        self.ProductFrame = LabelFrame(self.root, text="Item Selection", bg="white", fg="red", font=("arial", 18, "bold"))
        self.ProductFrame.grid(row=4, column=0, columnspan=3, pady=20, padx=10, sticky="ew")

        self.lblCategories = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Select Item", bd=4)
        self.lblCategories.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.ComboCategories = ttk.Combobox(self.ProductFrame, value=['Starter', 'Main Course', 'Dessert & Drinks'], font=('arial', 13, 'bold'), width=24, state="readonly")
        self.ComboCategories.grid(row=0, column=1, sticky=W, padx=5, pady=2)
        self.ComboCategories.current(0)
        self.ComboCategories.bind("<<ComboboxSelected>>", self.update_category_options)

        self.lblSubCategory = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Subcategory", bd=4)
        self.lblSubCategory.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.ComboSubCategory = ttk.Combobox(self.ProductFrame, state="readonly", value=[""], font=('arial', 10, 'bold'), width=24)
        self.ComboSubCategory.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        self.ComboSubCategory.current(0)
        self.ComboSubCategory.bind("<<ComboboxSelected>>", self.update_product_options)

        self.lblProduct = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Product Name", bd=4)
        self.lblProduct.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.ComboProduct = ttk.Combobox(self.ProductFrame, value=[""], state="readonly", font=('arial', 10, 'bold'), width=24)
        self.ComboProduct.grid(row=2, column=1, sticky=W, padx=5, pady=2)
        self.ComboProduct.bind("<<ComboboxSelected>>", self.update_price)

        self.lblPrice = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Price", bd=4)
        self.lblPrice.grid(row=0, column=2, sticky=W, padx=5, pady=2)

        self.ComboPrice = ttk.Combobox(self.ProductFrame, state="readonly", value=[""], font=('arial', 10, 'bold'), width=24)
        self.ComboPrice.grid(row=0, column=3, sticky=W, padx=5, pady=2)

        self.lblQty = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Qty", bd=4)
        self.lblQty.grid(row=1, column=2, sticky=W, padx=5, pady=2)

        self.ComboQty = Entry(self.ProductFrame, font=('arial', 10, 'bold'), width=26)
        self.ComboQty.grid(row=1, column=3, sticky=W, padx=5, pady=2)

        # Add Table Number Field
        self.lblTableNumber = Label(self.ProductFrame, font=('arial', 14, 'bold'), bg="white", text="Table Number", bd=4)
        self.lblTableNumber.grid(row=3, column=0, sticky=W, padx=5, pady=2)

        self.entryTableNumber = Entry(self.ProductFrame, font=('arial', 10, 'bold'), width=26)
        self.entryTableNumber.grid(row=3, column=1, sticky=W, padx=5, pady=2)

    def update_category_options(self, event):
        selected_category = self.ComboCategories.get()
        if selected_category == 'Starter':
            subcategories = ['Veg Starter', 'Non-Veg Starter']
        elif selected_category == 'Main Course':
            subcategories = ['Veg', 'Non-Veg']
        elif selected_category == 'Dessert & Drinks':
            subcategories = ['Ice Cream', 'Mojitos', 'Milk Shakes']
        else:
            subcategories = []

        self.ComboSubCategory['values'] = subcategories
        self.ComboSubCategory.set('')  # Clear previous selection
        self.ComboProduct.set('')  # Clear product selection
        self.ComboPrice.set('')  # Clear price selection

    def update_product_options(self, event):
        selected_subcategory = self.ComboSubCategory.get()
        products = []
        if selected_subcategory:
            for category in self.categories.values():
                if selected_subcategory in category:
                    products = list(category[selected_subcategory].keys())
                    break
        self.ComboProduct['values'] = products
        self.ComboProduct.set('')  # Clear previous selection
        self.ComboPrice.set('')  # Clear price selection

    def update_price(self, event):
        selected_product = self.ComboProduct.get()
        if selected_product:
            for category in self.categories.values():
                for subcategory in category.values():
                    if selected_product in subcategory:
                        self.ComboPrice.set(subcategory[selected_product])
                        break

    def load_items(self):
        # This method is no longer needed since we removed the product table
        pass

    def add_to_cart(self):
        selected_product = self.ComboProduct.get()  # Get the selected product from the combobox
        selected_price = self.ComboPrice.get()  # Get the selected price
        selected_qty = self.ComboQty.get()  # Get the quantity entered

        if selected_product and selected_price and selected_qty:
            item_details = (selected_product, selected_price, selected_qty)  # Create a tuple of item details
            self.cart.append(item_details)  # Add the item to the cart
            
            # Insert the item into the cart Treeview
            self.cart_tree.insert("", "end", values=item_details)
            messagebox.showinfo("Success", f"Added {selected_product} to cart.")
        else:
            messagebox.showwarning("Warning", "Please select an item and enter quantity to add to cart.")

    def send_to_kitchen(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Your cart is empty.")
            return

        table_number = self.entryTableNumber.get()  # Get the table number from the entry field
        if not table_number:
            messagebox.showwarning("Warning", "Please enter a table number.")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            for item in self.cart:
                product_name, price, quantity = item
                print(f"Sending to kitchen: {product_name}, Quantity: {quantity}, Table Number: {table_number}")  # Debugging line
                cursor.execute("INSERT INTO orders (product, quantity, table_number, status) VALUES (%s, %s, %s, %s)",
                            (product_name, quantity, table_number, 'pending'))
            
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Orders sent to kitchen successfully!")
            self.cart.clear()  # Clear the cart after sending
            self.cart_tree.delete(*self.cart_tree.get_children())  # Clear the cart Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send orders to kitchen: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)
        
    def refresh_orders(self):
        messagebox.showinfo("Info", "Orders refreshed!")  # Placeholder for actual logic

    def back_to_home(self):
        self.root.destroy()  # Close the executive window
        if self.staff_portal_win and self.staff_portal_win.winfo_exists():
            self.staff_portal_win.deiconify()  # Show the staff portal again
        else:
            # Fallback: open a new admin login if staff portal is gone
            main_window = Tk()
            AdminLoginWindow(main_window)
            main_window.mainloop()

    def open_manage_catalog(self):
        self.catalog_window = Toplevel(self.root)
        self.catalog_window.title("Manage Catalog")
        self.catalog_window.geometry("400x400")
        self.product_name = StringVar()
        self.product_price = StringVar()
        self.product_category = StringVar()
        self.quantity = IntVar()

        # Create a frame for the category selection and scrollbar
        category_frame = Frame(self.catalog_window)
        category_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Create a Treeview for category selection
        self.category_tree = ttk.Treeview(category_frame, height=5, show="tree")
        self.category_tree.pack(side=LEFT, fill=BOTH)

        # Add a scrollbar to the Treeview
        scrollbar = Scrollbar(category_frame, orient="vertical", command=self.category_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.category_tree.configure(yscroll=scrollbar.set)

        # Populate the Treeview with categories
        for category in ['Starter', 'Main Course', 'Dessert & Drinks']:
            self.category_tree.insert("", "end", text=category)

        # Bind the selection event
        self.category_tree.bind("<<TreeviewSelect>>", self.on_category_select)

        self.selected_category_label = Label(self.catalog_window, text="Selected item", font=("Arial", 14))
        self.selected_category_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Create a label and combobox for subcategory selection
        self.subcategory_label = Label(self.catalog_window, text="Select Subcategory", font=("Arial", 14))
        self.subcategory_label.grid(row=2, column=0, pady=10, padx=10)

        self.subcategory_combobox = ttk.Combobox(self.catalog_window, state="readonly", width=27)
        self.subcategory_combobox.grid(row=2, column=1, pady=10, padx=10)

        Label(self.catalog_window, text="Item Name").grid(row=3, column=0, pady=10, padx=10)
        Entry(self.catalog_window, textvariable=self.product_name).grid(row=3, column=1, pady=10, padx=10)

        Label(self.catalog_window, text="Price").grid(row=4, column=0, pady=10, padx=10)
        Entry(self.catalog_window, textvariable=self.product_price).grid(row=4, column=1, pady=10, padx=10)

        Label(self.catalog_window, text="Quantity").grid(row=5, column=0, pady=10, padx=10)
        Entry(self.catalog_window, textvariable=self.quantity).grid(row=5, column=1, pady=10, padx=10)

        Button(self.catalog_window, text="Add Product", command=self.add_product, font=("Arial", 14, 'bold')).grid(row=6, column=0, pady=20, padx=10)
        Button(self.catalog_window, text="Delete Product", command=self.delete_product, font=("Arial", 14, 'bold')).grid(row=6, column=1, pady=20, padx=10)

    def on_category_select(self, event):
        selected_item = self.category_tree.selection()
        if selected_item:
            category = self.category_tree.item(selected_item, "text")
            self.selected_category_label.config(text=f"Selected Category: {category}")

            # Update subcategory options based on the selected category
            if category == 'Starter':
                subcategories = ['Veg Starter', 'Non-Veg Starter']
            elif category == 'Main Course':
                subcategories = ['Veg', 'Non-Veg']
            elif category == 'Dessert & Drinks':
                subcategories = ['Ice Cream', 'Mojitos', 'Milk Shakes']
            else:
                subcategories = []

            self.subcategory_combobox['values'] = subcategories
            self.subcategory_combobox.set('')  # Clear previous selection

    def add_product(self):
        product_name = self.product_name.get()  # Get the product name from the entry
        product_price = self.product_price.get()  # Get the product price from the entry
        quantity = self.quantity.get()  # Get the quantity from the entry
        selected_category = self.selected_category_label.cget("text").replace("Selected Category: ", "")
        selected_subcategory = self.subcategory_combobox.get()  # Get the selected subcategory

        # Check if all fields are filled
        if not product_name or not product_price or not quantity or not selected_category or not selected_subcategory:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

        try:
            # Convert price and quantity to appropriate types
            product_price = float(product_price)  # Ensure price is a float
            quantity = int(quantity)  # Ensure quantity is an integer

            # Add product to the database
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items_detail (product_name, price, category, subcategory) VALUES (%s, %s, %s, %s)",
                        (product_name, product_price, selected_category, selected_subcategory))
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")

            # Clear the fields after adding
            self.product_name.set('')
            self.product_price.set('')
            self.quantity.set(0)
            self.subcategory_combobox.set('')
            self.selected_category_label.config(text="Selected Category")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                close_connection(conn)

    def delete_product(self):
        product_name = self.product_name.get()

        if product_name:
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM items_detail WHERE product_name=%s", (product_name,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    # self.load_items()  # No longer needed
                else:
                    messagebox.showerror("Error", "Product not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    close_connection(conn)
        else:
            messagebox.showerror("Error", "Please enter a product name.")

if __name__ == "__main__":
    setup_database()          # Ensure all tables exist before UI starts
    root = Tk()
    app = AdminLoginWindow(root)  # Start with Admin Login
    root.mainloop()