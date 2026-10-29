# Vehicle Rental Management System
Coursework: Relational Database Management Systems (RDBMS)  
Technologies: Python 3, MySQL

---

## 1. Project Overview

The Vehicle Rental Management System is a simple console-based application built to manage car rentals. It uses Python to connect to a MySQL database and allows users to manage vehicles, customers, rentals, payments, and maintenance records through a terminal menu.

The project demonstrates core database concepts:
- Creating relational tables with Primary Keys and Foreign Keys.
- Inserting, updating, deleting, and querying data (CRUD operations).
- Combining data from multiple tables using SQL INNER JOIN.

---

## 2. Project Structure

```text
Mini project for rdbms/
├── schema.sql           # Database schema and sample data queries
├── db_config.py         # MySQL connection and table setup
├── main.py              # Main terminal menu and operations
├── connection.py        # Entry file
├── requirements.txt     # Python dependency (mysql-connector-python)
└── README.md            # Project documentation and viva notes
```

- **`schema.sql`**: Contains the SQL code to create the database, tables, keys, and insert sample data.
- **`db_config.py`**: Handles connecting to MySQL and running table creation queries.
- **`main.py`**: Runs the terminal interface with formatted tables and menus.
- **`connection.py`**: Simple starter file to run the program.
- **`requirements.txt`**: Specifies the MySQL connector module.

---

## 3. Entity-Relationship (ER) Model

In standard database design, the system has 5 Entities:
1. **Customer** (Holds customer personal information)
2. **Vehicle** (Holds details of cars in the fleet)
3. **Rental** (Records which customer rented which car and when)
4. **Payment** (Records payment transactions for a rental)
5. **Maintenance** (Records servicing details of a vehicle)

### Cardinality / Relationships (1:M)
- **Customer to Rental (1 : M)**: One customer can have multiple rentals over time.
- **Vehicle to Rental (1 : M)**: One vehicle can be rented multiple times across different dates.
- **Rental to Payment (1 : M)**: One rental can have one or more payments.
- **Vehicle to Maintenance (1 : M)**: One vehicle can undergo maintenance multiple times.

### ER Diagram (Text / College Exam Representation)

```text
  +------------+                 +------------+
  |  CUSTOMER  |                 |  VEHICLE   |
  +------------+                 +------------+
        | 1                            | 1
        |                              |
        | [Places]                     | [Assigned To]
        |                              |
        v M                            v M
  +-------------------------------------------+
  |                  RENTAL                   |
  +-------------------------------------------+
        | 1                            |
        |                              |
        | [Paid Via]                   | (Vehicle undergo service)
        |                              v
        v M                      +-------------+
  +-------------+                | MAINTENANCE |
  |   PAYMENT   |                +-------------+
  +-------------+
```

### Table Definitions & Keys

1. **Customer**
   - `CustomerID` (Primary Key)
   - `FirstName`, `LastName`
   - `LicenseNumber` (Unique)
   - `PhoneNumber`

2. **Vehicle**
   - `VehicleID` (Primary Key)
   - `Make`, `Model`
   - `LicensePlate` (Unique)
   - `DailyRate`
   - `Status` (Available / Rented / Maintenance)

3. **Rental**
   - `RentalID` (Primary Key)
   - `CustomerID` (Foreign Key referencing Customer)
   - `VehicleID` (Foreign Key referencing Vehicle)
   - `RentalDate`
   - `ReturnDate`
   - `TotalCost`

4. **Payment**
   - `PaymentID` (Primary Key)
   - `RentalID` (Foreign Key referencing Rental)
   - `PaymentDate`
   - `Amount`
   - `PaymentMethod` (Cash / Card / UPI)

5. **Maintenance**
   - `MaintenanceID` (Primary Key)
   - `VehicleID` (Foreign Key referencing Vehicle)
   - `ServiceDate`
   - `Description`
   - `Cost`

---

## 4. Key Database Concepts Used

1. **Primary Key (PK)**:
   Uniquely identifies each row in a table (e.g., `CustomerID`, `VehicleID`, `RentalID`). A Primary Key cannot contain NULL values and must be unique.

2. **Foreign Key (FK)**:
   A field in one table that links to the Primary Key of another table (e.g., `Rental.CustomerID` links to `Customer.CustomerID`). This ensures **Referential Integrity**, meaning you cannot create a rental for a customer that does not exist.

3. **SQL Commands Used**:
   - **DDL (Data Definition Language)**: `CREATE DATABASE`, `CREATE TABLE`, `DROP TABLE`.
   - **DML (Data Manipulation Language)**: `INSERT` (add vehicle/customer), `UPDATE` (return car, change status), `DELETE` (remove record).
   - **DQL (Data Query Language)**: `SELECT`, `WHERE`, `ORDER BY`.

4. **SQL INNER JOIN**:
   When displaying rentals, the program combines rows from `Rental`, `Customer`, and `Vehicle` so it shows the customer's real name and the car's model instead of just numeric IDs:
   ```sql
   SELECT 
       r.RentalID,
       CONCAT(c.FirstName, ' ', c.LastName) AS Customer,
       CONCAT(v.Make, ' ', v.Model) AS Vehicle,
       v.LicensePlate,
       r.RentalDate,
       r.ReturnDate,
       r.TotalCost
   FROM Rental r
   JOIN Customer c ON r.CustomerID = c.CustomerID
   JOIN Vehicle v ON r.VehicleID = v.VehicleID;
   ```

---

## 5. How to Run the Project

### Step 1: Install Python connector
Open your terminal and run:
```bash
pip install mysql-connector-python
```

### Step 2: Configure MySQL credentials
Open `db_config.py` and set your MySQL password:
```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "rental_db"
```

### Step 3: Start the program
Run either:
```bash
python main.py
```
or
```bash
python connection.py
```

### Step 4: First time database setup
From the main menu, select **Option 15** (`Reset / Setup Database Tables`). When it asks `Include sample data? (y/n):`, enter `y`.

---

## 6. Terminal Menu Preview

```text
-------------------------------------------
      VEHICLE RENTAL MANAGEMENT SYSTEM     
-------------------------------------------
 1. Add Vehicle
 2. Show All Vehicles
 3. Show Available Vehicles
 4. Remove Vehicle
 5. Add Customer
 6. Show All Customers
 7. Remove Customer
 8. Rent a Vehicle
 9. Return a Vehicle
10. Show All Rentals
11. Log Payment
12. Show Payment History
13. Log Maintenance
14. Show Maintenance Records
15. Reset / Setup Database Tables
 0. Exit
-------------------------------------------
```

Sample output when viewing vehicles:
```text
+------------+---------+---------+---------------+------------+-----------+
| Vehicle ID | Make    | Model   | License Plate | Daily Rate | Status    |
+------------+---------+---------+---------------+------------+-----------+
| 101        | Toyota  | Corolla | KA-01-MG-1234 | 45.00      | Rented    |
| 102        | Honda   | City    | KA-05-AB-5678 | 50.00      | Available |
| 103        | Hyundai | Creta   | MH-02-CD-9999 | 65.00      | Available |
+------------+---------+---------+---------------+------------+-----------+
```

---

## 7. Viva Voce / Exam Q&A (Simple & Direct)

**Q1: What is an RDBMS?**  
*Answer:* A Relational Database Management System organizes data into tables consisting of rows (tuples) and columns (attributes), where relationships between tables are maintained using Primary and Foreign Keys.

**Q2: What is a Primary Key and a Foreign Key in your project?**  
*Answer:* 
- A Primary Key uniquely identifies a record in a table, like `CustomerID` in the `Customer` table or `VehicleID` in the `Vehicle` table.
- A Foreign Key is a field that references the Primary Key of another table. In the `Rental` table, `CustomerID` and `VehicleID` are Foreign Keys linking back to `Customer` and `Vehicle`.

**Q3: What type of relationship exists between Customer and Rental?**  
*Answer:* A One-to-Many (1:M) relationship. One customer can make multiple rentals over time, but each rental belongs to one customer.

**Q4: Why did you use an INNER JOIN query?**  
*Answer:* The `Rental` table only stores IDs (`CustomerID`, `VehicleID`). To display meaningful output on screen (customer's name and car name), we use `INNER JOIN` to match records across the `Rental`, `Customer`, and `Vehicle` tables.

**Q5: How does Python interact with MySQL in your project?**  
*Answer:* We use `mysql.connector`. It creates a connection object to MySQL. Then we use a `cursor` to execute SQL queries (`cur.execute()`), read results (`cur.fetchall()`), and save changes using `conn.commit()`.

**Q6: What happens when a vehicle is rented?**  
*Answer:* The system creates a new row in the `Rental` table and automatically updates the vehicle's `Status` in the `Vehicle` table from `'Available'` to `'Rented'`.
