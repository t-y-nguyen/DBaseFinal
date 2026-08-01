-- Query 1 (Multi-Table Join): Customer names and products purchased over $100
SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    p.name AS product_name,
    p.price,
    pur.purchase_date
FROM Purchase pur
JOIN Customer c ON pur.customer_id = c.customer_id
JOIN Product p ON pur.product_id = p.product_id
WHERE p.price > 100.00;

-- Query 2: List all credit cards registered to each customer
SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    cc.card_number,
    cc.expiration_date
FROM Customer c
JOIN CreditCard cc ON c.customer_id = cc.customer_id
ORDER BY customer_name;

-- Query 3: Inventory summary managed by staff members
SELECT 
    s.first_name || ' ' || s.last_name AS staff_member,
    COUNT(p.product_id) AS total_products_managed,
    SUM(p.stock_quantity) AS total_stock_count
FROM Staff s
LEFT JOIN Product p ON s.staff_id = p.managed_by_staff_id
GROUP BY s.staff_id, staff_member;