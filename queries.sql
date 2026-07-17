   (DDL)
-- this creates the customer table
 CREATE TABLE customer (
    ->     Customer_Id INT PRIMARY KEY AUTO_INCREMENT,
    ->     First_Name VARCHAR(50),
    ->     Middle_Name VARCHAR(50),
    ->     Last_Name VARCHAR(50),
    ->     Phone VARCHAR(15)
    -> ); 

 CREATE TABLE supplier (
    ->     Supplier_Id INT PRIMARY KEY AUTO_INCREMENT,
    ->     First_Name VARCHAR(50),
    ->     Middle_Name VARCHAR(50),
    ->     Last_Name VARCHAR(50),
    ->     Contact_No VARCHAR(15)
    -> );

CREATE TABLE sales (
    ->     Sale_Id INT PRIMARY KEY AUTO_INCREMENT,
    ->     Customer_Id INT,
    ->     Sale_Date DATE DEFAULT (CURDATE()),
    ->     Total_Amount DECIMAL(10,2),
    ->     FOREIGN KEY (Customer_Id) REFERENCES customer(Customer_Id)
    -> );

-- this adds supplier foreign key to medicines
ALTER TABLE medicines
    -> ADD COLUMN Supplier_Id INT,
    -> ADD FOREIGN KEY (Supplier_Id) REFERENCES supplier(Supplier_Id);
 
    (DML)
-- this inserts supplier data
 INSERT INTO supplier VALUES
    -> (1, 'Raj', 'Kumar', 'Sharma', '9876543210'),
    -> (2, 'Priya', 'Devi', 'Singh', '8765432109'),
    -> (3, 'Amit', 'Lal', 'Verma', '7654321098');

 INSERT INTO customer VALUES
    -> (1, 'Anjali', 'Rani', 'Gupta', '9123456780'),
    -> (2, 'Rohit', 'Kumar', 'Mehta', '8234567891'),
    -> (3, 'Sneha', 'Priya', 'Joshi', '7345678902');

INSERT INTO medicines (name, company, price, stock, expiry_date, Supplier_Id) VALUES
    -> ('Paracetamol', 'ABC Pharma', 50.00, 100, '2026-12-31', 1),
    -> ('Aspirin', 'XYZ Labs', 30.00, 5, '2025-06-30', 2),
    -> ('Amoxicillin', 'MediCo', 120.00, 25, '2027-01-15', 3);

INSERT INTO sales VALUES
    -> (1, 1, '2026-05-24', 50.00),
    -> (2, 2, '2026-05-24', 120.00),
    -> (3, 3, '2026-05-24', 30.00);
 
    (SELECT QUERIES)

 SELECT * FROM customer;
+-------------+------------+-------------+-----------+------------+
| Customer_Id | First_Name | Middle_Name | Last_Name | Phone      |
+-------------+------------+-------------+-----------+------------+
|           1 | Anjali     | Rani        | Gupta     | 9123456780 |
|           2 | Rohit      | Kumar       | Mehta     | 8234567891 |
|           3 | Sneha      | Priya       | Joshi     | 7345678902 |
+-------------+------------+-------------+-----------+------------+

 SELECT * FROM medicines;
+----+-------------+------------+-------+-------+-------------+-------------+
| id | name        | company    | price | stock | expiry_date | Supplier_Id |
+----+-------------+------------+-------+-------+-------------+-------------+
|  1 | Metformin   | xyz        |   200 |    35 | 2028-05-14  |        NULL |
|  2 | Paracetamol | ABC Pharma |    50 |   100 | 2026-12-31  |           1 |
|  3 | Aspirin     | XYZ Labs   |    30 |     5 | 2025-06-30  |           2 |
|  4 | Amoxicillin | MediCo     |   120 |    25 | 2027-01-15  |           3 |
+----+-------------+------------+-------+-------+-------------+-------------+

 SELECT * FROM supplier;
+-------------+------------+-------------+-----------+------------+
| Supplier_Id | First_Name | Middle_Name | Last_Name | Contact_No |
+-------------+------------+-------------+-----------+------------+
|           1 | Raj        | Kumar       | Sharma    | 9876543210 |
|           2 | Priya      | Devi        | Singh     | 8765432109 |
|           3 | Amit       | Lal         | Verma     | 7654321098 |
+-------------+------------+-------------+-----------+------------+

    (JOIN QUERY)
--this shows medicines with their suppliers using JOIN
SELECT m.name, m.price, m.stock,
    -> s.First_Name, s.Contact_No
    -> FROM medicines m
    -> JOIN supplier s ON m.Supplier_Id = s.Supplier_Id;
+-------------+-------+-------+------------+------------+
| name        | price | stock | First_Name | Contact_No |
+-------------+-------+-------+------------+------------+
| Paracetamol |    50 |   100 | Raj        | 9876543210 |
| Aspirin     |    30 |     5 | Priya      | 8765432109 |
| Amoxicillin |   120 |    25 | Amit       | 7654321098 |
+-------------+-------+-------+------------+------------+

  (low stock query)
SELECT name, stock FROM medicines WHERE stock < 10;
+---------+-------+
| name    | stock |
+---------+-------+
| Aspirin |     5 |
+---------+-------+