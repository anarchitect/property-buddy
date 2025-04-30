CREATE TABLE payment (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50),
    amount DECIMAL(10, 2),
    due_date DATE,
    payee VARCHAR(100),
    payment_type VARCHAR(50),
    status VARCHAR(20)
);
INSERT INTO payment (customer_id, amount, due_date, payee, payment_type, status)
VALUES
('apartment-901', 500.00, '2025-04-20', 'Insurance Company', 'Insurance', 'Overdue'),
('apartment-901', 1200.00, '2025-05-01', 'John Smith', 'Rent', 'Paid'),
('apartment-901', 85.50, '2025-05-03', 'Water Utility Co.', 'Utilities', 'Pending'),
('apartment-901', 60.75, '2025-05-04', 'Internet Provider', 'Utilities', 'Pending'),
('apartment-901', 150.00, '2025-05-12', 'Electric Company', 'Utilities', 'Pending'),
('apartment-901', 75.00, '2025-05-18', 'Garbage Collection', 'Services', 'Pending');
