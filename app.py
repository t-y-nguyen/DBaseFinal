import psycopg2
from psycopg2 import extras

# ==========================================
# DATABASE CONFIGURATION
# ==========================================
DB_HOST = "localhost"
DB_NAME = "ecommerceDB"
DB_USER = "postgres"
DB_PASS = "password"
DB_PORT = "5432"

def get_db_connection():
    """Establishes connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS, 
            port=DB_PORT
        )
    except Exception as e:
        print(f"\n[Error] Database connection failed: {e}")
        return None

# ==========================================
# AUTHENTICATION & REGISTRATION
# ==========================================

def register_customer():
    """Registers a new customer in the database."""
    print("\n--- CREATE NEW CUSTOMER ACCOUNT ---")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email Address: ").strip().lower()
    phone = input("Phone Number: ").strip()
    password = input("Password: ").strip()
    confirm_pass = input("Confirm Password: ").strip()

    if password != confirm_pass:
        print("\n[!] Passwords do not match!")
        return

    conn = get_db_connection()
    if not conn: 
        return
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO Customer (first_name, last_name, email, passwords, phone) 
               VALUES (%s, %s, %s, %s, %s) RETURNING customer_id;""",
            (first_name, last_name, email, password, phone)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        print(f"\n[Success] Account created successfully! Your Customer ID is {new_id}.")
    except psycopg2.IntegrityError:
        conn.rollback()
        print("\n[!] An account with that email already exists.")
    except Exception as e:
        conn.rollback()
        print(f"\n[Error] Registration failed: {e}")
    finally:
        cur.close()
        conn.close()

def login_customer():
    """Authenticates a customer account."""
    print("\n--- CUSTOMER LOGIN ---")
    email = input("Email: ").strip().lower()
    password = input("Password: ").strip()

    conn = get_db_connection()
    if not conn: 
        return None
    try:
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(
            "SELECT customer_id, first_name, last_name FROM Customer WHERE email = %s AND passwords = %s;",
            (email, password)
        )
        customer = cur.fetchone()
        if customer:
            print(f"\n[Success] Welcome back, {customer['first_name']}!")
            return customer
        else:
            print("\n[!] Invalid email or password.")
            return None
    finally:
        cur.close()
        conn.close()

def login_staff():
    """Authenticates a staff member account."""
    print("\n--- STAFF LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    conn = get_db_connection()
    if not conn: 
        return None
    try:
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(
            "SELECT staff_id, first_name, role FROM Staff WHERE username = %s AND passwords = %s;",
            (username, password)
        )
        staff = cur.fetchone()
        if staff:
            print(f"\n[Success] Welcome, {staff['first_name']} ({staff['role']})!")
            return staff
        else:
            print("\n[!] Invalid username or password.")
            return None
    finally:
        cur.close()
        conn.close()

# ==========================================
# BUSINESS LOGIC & DATABASE FEATURES
# ==========================================

def view_products():
    """Fetches and displays all available products in inventory."""
    conn = get_db_connection()
    if not conn: 
        return
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT product_id, name, price, stock_quantity FROM Product ORDER BY product_id;")
    products = cur.fetchall()
    
    print("\n--- AVAILABLE PRODUCTS ---")
    print(f"{'ID':<5} | {'Product Name':<30} | {'Price':<10} | {'Stock':<5}")
    print("-" * 60)
    for p in products:
        print(f"{p['product_id']:<5} | {p['name']:<30} | ${p['price']:<9.2f} | {p['stock_quantity']:<5}")
    
    cur.close()
    conn.close()

def add_product_staff(staff_id):
    """Allows staff members to insert new items into inventory."""
    print("\n--- ADD NEW PRODUCT ---")
    name = input("Enter product name: ").strip()
    try:
        price = float(input("Enter price ($): "))
        stock = int(input("Enter initial stock quantity: "))
    except ValueError:
        print("\n[!] Invalid numerical input.")
        return

    conn = get_db_connection()
    if not conn: 
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Product (name, price, stock_quantity, managed_by_staff_id) VALUES (%s, %s, %s, %s);",
            (name, price, stock, staff_id)
        )
        conn.commit()
        print(f"\n[Success] '{name}' successfully added to inventory!")
    except Exception as e:
        conn.rollback()
        print(f"\n[Error] Could not add product: {e}")
    finally:
        cur.close()
        conn.close()

def add_credit_card(customer_id):
    """Allows customers to attach payment methods to their account."""
    print("\n--- ADD PAYMENT METHOD ---")
    card_num = input("16-digit Card Number: ").strip()
    holder = input("Cardholder Name: ").strip()
    exp = input("Expiration Date (MM/YY): ").strip()

    conn = get_db_connection()
    if not conn: 
        return
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO CreditCard (customer_id, card_number, cardholder_name, expiration_date) VALUES (%s, %s, %s, %s);",
            (customer_id, card_num, holder, exp)
        )
        conn.commit()
        print("\n[Success] Credit card added to your account!")
    except Exception as e:
        conn.rollback()
        print(f"\n[Error] Could not add card: {e}")
    finally:
        cur.close()
        conn.close()

def make_purchase_customer(customer_id):
    """Handles product purchase transactions for customers."""
    print("\n--- PLACE AN ORDER ---")
    view_products()
    try:
        product_id = int(input("\nEnter Product ID to purchase: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("\n[!] Invalid numerical input.")
        return

    conn = get_db_connection()
    if not conn: 
        return
    try:
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        
        # Verify Product Existence & Stock
        cur.execute("SELECT price, stock_quantity FROM Product WHERE product_id = %s;", (product_id,))
        prod = cur.fetchone()
        if not prod:
            print("\n[!] Product not found.")
            return
        if prod['stock_quantity'] < quantity:
            print(f"\n[!] Insufficient stock! Only {prod['stock_quantity']} remaining.")
            return

        # Verify Credit Card on File
        cur.execute("SELECT card_id FROM CreditCard WHERE customer_id = %s LIMIT 1;", (customer_id,))
        card = cur.fetchone()
        if not card:
            print("\n[!] No payment method on file. Please add a credit card first!")
            return

        total_amount = float(prod['price']) * quantity
        
        # Execute Transaction: Insert Purchase + Update Product Stock
        cur.execute(
            "INSERT INTO Purchase (customer_id, product_id, card_id, quantity, total_amount) VALUES (%s, %s, %s, %s, %s);",
            (customer_id, product_id, card['card_id'], quantity, total_amount)
        )
        cur.execute(
            "UPDATE Product SET stock_quantity = stock_quantity - %s WHERE product_id = %s;",
            (quantity, product_id)
        )
        conn.commit()
        print(f"\n[Success] Order complete! Total charged: ${total_amount:.2f}")

    except Exception as e:
        conn.rollback()
        print(f"\n[Error] Transaction failed: {e}")
    finally:
        cur.close()
        conn.close()

# ==========================================
# SUB-MENUS & MAIN DASHBOARDS
# ==========================================

def customer_menu(customer):
    """Customer Dashboard Navigation."""
    while True:
        print(f"\n=== CUSTOMER DASHBOARD ({customer['first_name'].upper()}) ===")
        print("1. View Products")
        print("2. Add Credit Card")
        print("3. Purchase Product")
        print("4. Logout")
        choice = input("Select option (1-4): ").strip()

        if choice == '1':
            view_products()
        elif choice == '2':
            add_credit_card(customer['customer_id'])
        elif choice == '3':
            make_purchase_customer(customer['customer_id'])
        elif choice == '4':
            print(f"\nLogging out {customer['first_name']}...")
            break
        else:
            print("\n[!] Invalid choice.")

def staff_menu(staff):
    """Staff Dashboard Navigation."""
    while True:
        print(f"\n=== STAFF DASHBOARD ({staff['first_name'].upper()}) ===")
        print("1. View Inventory")
        print("2. Add New Product")
        print("3. Logout")
        choice = input("Select option (1-3): ").strip()

        if choice == '1':
            view_products()
        elif choice == '2':
            add_product_staff(staff['staff_id'])
        elif choice == '3':
            print(f"\nLogging out {staff['first_name']}...")
            break
        else:
            print("\n[!] Invalid choice.")

def main():
    """Main System Loop."""
    while True:
        print("\n==========================================")
        print("       E-COMMERCE SYSTEM MAIN MENU        ")
        print("==========================================")
        print("1. Customer Login")
        print("2. Customer Registration (Create Account)")
        print("3. Staff Login")
        print("4. Exit")
        choice = input("Select option (1-4): ").strip()

        if choice == '1':
            user = login_customer()
            if user:
                customer_menu(user)
        elif choice == '2':
            register_customer()
        elif choice == '3':
            user = login_staff()
            if user:
                staff_menu(user)
        elif choice == '4':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("\n[!] Invalid selection, please try again.")

if __name__ == "__main__":
    main()