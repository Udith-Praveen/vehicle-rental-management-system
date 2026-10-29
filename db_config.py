import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Kanna@6782"
DB_NAME = "rental_db"
DB_PORT = 3306

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cur.execute(f"USE {DB_NAME}")
        cur.close()
        return conn
    except Exception as e:
        print("Database connection error:", e)
        print("Check MySQL server status and password in db_config.py")
        return None

def setup_tables(cur, conn, seed_sample_data=False, verbose=True):
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID INT PRIMARY KEY,
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            LicenseNumber VARCHAR(30) UNIQUE NOT NULL,
            PhoneNumber VARCHAR(15) NOT NULL
        ) ENGINE=InnoDB;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Vehicle (
            VehicleID INT PRIMARY KEY,
            Make VARCHAR(50) NOT NULL,
            Model VARCHAR(50) NOT NULL,
            LicensePlate VARCHAR(20) UNIQUE NOT NULL,
            DailyRate DECIMAL(8,2) NOT NULL,
            Status VARCHAR(20) DEFAULT 'Available'
        ) ENGINE=InnoDB;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Rental (
            RentalID INT PRIMARY KEY,
            CustomerID INT NOT NULL,
            VehicleID INT NOT NULL,
            RentalDate DATE NOT NULL,
            ReturnDate DATE,
            TotalCost DECIMAL(10,2) DEFAULT 0.00,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
            FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Payment (
            PaymentID INT PRIMARY KEY,
            RentalID INT NOT NULL,
            PaymentDate DATE NOT NULL,
            Amount DECIMAL(10,2) NOT NULL,
            PaymentMethod VARCHAR(20) NOT NULL,
            FOREIGN KEY (RentalID) REFERENCES Rental(RentalID) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Maintenance (
            MaintenanceID INT PRIMARY KEY,
            VehicleID INT NOT NULL,
            ServiceDate DATE NOT NULL,
            Description VARCHAR(255) NOT NULL,
            Cost DECIMAL(8,2) NOT NULL,
            FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """)

        conn.commit()
        if verbose:
            print("Tables setup completed successfully.")

        if seed_sample_data:
            cur.execute("SELECT COUNT(*) FROM Customer")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                INSERT INTO Customer (CustomerID, FirstName, LastName, LicenseNumber, PhoneNumber) VALUES
                (1, 'Rahul', 'Sharma', 'DL-01-2021001', '9876543210'),
                (2, 'Priya', 'Verma', 'MH-02-2020045', '9812345678'),
                (3, 'Amit', 'Patel', 'KA-03-2019888', '9900112233');
                """)

                cur.execute("""
                INSERT INTO Vehicle (VehicleID, Make, Model, LicensePlate, DailyRate, Status) VALUES
                (101, 'Toyota', 'Corolla', 'KA-01-MG-1234', 45.00, 'Rented'),
                (102, 'Honda', 'City', 'KA-05-AB-5678', 50.00, 'Available'),
                (103, 'Hyundai', 'Creta', 'MH-02-CD-9999', 65.00, 'Available');
                """)

                cur.execute("""
                INSERT INTO Rental (RentalID, CustomerID, VehicleID, RentalDate, ReturnDate, TotalCost) VALUES
                (501, 1, 101, '2026-10-25', NULL, 0.00);
                """)

                conn.commit()
                if verbose:
                    print("Sample seed data added.")

    except Exception as e:
        print("Error during setup:", e)
