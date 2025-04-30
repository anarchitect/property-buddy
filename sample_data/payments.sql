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
('apartment-906', 500.00, '2025-04-20', 'Insurance Company', 'Insurance', 'Overdue'),
('apartment-906', 1200.00, '2025-05-01', 'John Smith', 'Rent', 'Paid'),
('apartment-906', 85.50, '2025-05-03', 'Water Utility Co.', 'Utilities', 'Pending'),
('apartment-906', 60.75, '2025-05-04', 'Internet Provider', 'Utilities', 'Pending'),
('apartment-906', 150.00, '2025-05-12', 'Electric Company', 'Utilities', 'Pending'),
('apartment-906', 75.00, '2025-05-18', 'Garbage Collection', 'Services', 'Pending'),

INSERT INTO payment (customer_id, amount, due_date, payee, payment_type, status)
VALUES
('unit-1', 1250.00, '2025-05-01', 'Michael Green', 'Rent', 'Paid'),
('unit-1', 88.20, '2025-05-06', 'Water Utility Co.', 'Utilities', 'Paid'),
('unit-1', 142.30, '2025-05-15', 'Gas Provider', 'Utilities', 'Pending'),
('unit-1', 60.00, '2025-05-20', 'Internet Provider', 'Utilities', 'Pending'),
('unit-1', 500.00, '2025-06-01', 'Insurance Company', 'Insurance', 'Overdue'),
('unit-1', 1190.00, '2025-06-01', 'Michael Green', 'Rent', 'Due'),
('unit-1', 78.50, '2025-06-03', 'Garbage Collection', 'Services', 'Overdue');
