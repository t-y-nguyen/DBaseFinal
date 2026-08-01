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
-- DATA INSERTION
-- ==========================================

-- 1. Insert Staff Members
INSERT INTO Staff (username, passwords, first_name, last_name, email, role) VALUES
('admin', 'adminpassword', 'Alice', 'Smith', 'alice.staff@store.com', 'Store Manager'),
('bob_manager', 'password123', 'Bob', 'Jones', 'bob.staff@store.com', 'Inventory Specialist');

-- 2. Insert Customers
INSERT INTO Customer (first_name, last_name, email, passwords, phone) VALUES
('Alex', 'Mercer', 'alex.m@gmail.com', 'customerpass1', '5135550199'),
('Sarah', 'Connor', 'sconnor@yahoo.com', 'customerpass2', '5135550288'),
('Bruce', 'Wayne', 'bwayne@gotham.com', 'batpass123', '5135550377');

-- 3. Insert Credit Cards
INSERT INTO CreditCard (customer_id, card_number, cardholder_name, expiration_date) VALUES
(1, '4111111111111111', 'Alex Mercer', '12/28'),
(1, '4222222222222222', 'Alex Mercer', '05/29'), -- Multiple cards for testing Query 2
(2, '5500000000000004', 'Sarah Connor', '08/27');

-- 4. Insert Products (Some over $100 for Query 1)
INSERT INTO Product (name, price, stock_quantity, managed_by_staff_id) VALUES
('Wireless Mechanical Keyboard', 89.99, 15, 1),   -- Under $100
('27-Inch 4K Monitor', 329.99, 8, 1),            -- Over $100
('Noise-Canceling Headphones', 199.50, 12, 2),    -- Over $100
('USB-C Desk Hub', 24.50, 50, 2);                -- Under $100

-- 5. Insert Purchases
INSERT INTO Purchase (customer_id, product_id, card_id, quantity, total_amount) VALUES
(1, 1, 1, 1, 89.99),   -- Alex bought Keyboard (< $100)
(1, 2, 2, 1, 329.99),  -- Alex bought Monitor (> $100) -> Triggers Query 1
(2, 3, 3, 2, 399.00);  -- Sarah bought Headphones (> $100) -> Triggers Query 1
