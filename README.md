# Overview
This database system is to be used to support an online E-commerce system. It offers a dual-interface design:
* **Customer Operations:** Viewing available products, handling saved payment methods and completing purchases.
* **Staff Operations:** Updates product listings, maintains current inventory and conducts an inventory audit.

## Requirements
* **Customers:** Must keep unique identity information (first name, last name, unique e-mail, contact phone number) and plain text account passwords.
* **Staff:** Must record their staff login credentials (username, email, password), full name and role in operation (e.g., Manager, Inventory Specialist).
* **Products:** Must record product name, unit price (must be >= 0), current inventory quantity and which staff member(s) oversees this product.
* **Credit Cards:** Store card information (16-digit number, name, expiry date) that is tied to a specific customer account.
* **Purchases:** Should have records of the products purchased, buyer, credit card, quantity purchased, total amount calculated and time of purchase.

## Use Cases
* **UC-01 Customer Checkout:** is used to describe when a customer checks out a product and payment card. This system verifies stock, totals the amount amount = quantity * price, writes the record in Purchase and updates the product stock.
* **UC-02 (Staff Inventory Management):** Staff can add new products or change stock_quantity of existing products.
* **UC-03 (Reporting & Analytics):** Get high-value purchases (where order amount > \$100). Staff member groups inventory. Display all payment methods the customer has registered.
