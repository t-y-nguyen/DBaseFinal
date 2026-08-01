-- Clean up existing tables (orders matter due to foreign keys)
DROP TABLE IF EXISTS Purchase CASCADE;
DROP TABLE IF EXISTS CreditCard CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS Staff CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;

-- 1. Customer Table
CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passwords VARCHAR(100) NOT NULL,
    phone VARCHAR(20)
);

-- 2. Staff Table
CREATE TABLE Staff (
    staff_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passwords VARCHAR(100) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'Inventory Manager'
);

-- 3. CreditCard Table
CREATE TABLE CreditCard (
    card_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    expiration_date VARCHAR(7) NOT NULL, -- Format: MM/YY
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
);

-- 4. Product Table
CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0),
    managed_by_staff_id INT,
    FOREIGN KEY (managed_by_staff_id) REFERENCES Staff(staff_id) ON DELETE SET NULL
);

-- 5. Purchase Table
CREATE TABLE Purchase (
    purchase_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    card_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_amount NUMERIC(10, 2) NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES CreditCard(card_id) ON DELETE CASCADE
);

-- ==========================================
-- SEED INITIAL STAFF ACCOUNTS ONLY
-- ==========================================

INSERT INTO Staff (username, passwords, first_name, last_name, email, role) VALUES
('admin', 'adminpassword', 'Alice', 'Smith', 'alice.staff@store.com', 'Store Manager'),
('bob_manager', 'password123', 'Bob', 'Jones', 'bob.staff@store.com', 'Inventory Specialist');