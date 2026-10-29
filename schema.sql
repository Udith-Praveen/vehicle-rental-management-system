CREATE DATABASE IF NOT EXISTS rental_db;
USE rental_db;

DROP TABLE IF EXISTS Maintenance;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Rental;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS Customer;

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    LicenseNumber VARCHAR(30) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Vehicle (
    VehicleID INT PRIMARY KEY,
    Make VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    LicensePlate VARCHAR(20) UNIQUE NOT NULL,
    DailyRate DECIMAL(8,2) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Available'
) ENGINE=InnoDB;

CREATE TABLE Rental (
    RentalID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    VehicleID INT NOT NULL,
    RentalDate DATE NOT NULL,
    ReturnDate DATE,
    TotalCost DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY,
    RentalID INT NOT NULL,
    PaymentDate DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentMethod VARCHAR(20) NOT NULL,
    FOREIGN KEY (RentalID) REFERENCES Rental(RentalID) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Maintenance (
    MaintenanceID INT PRIMARY KEY,
    VehicleID INT NOT NULL,
    ServiceDate DATE NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Cost DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Customer (CustomerID, FirstName, LastName, LicenseNumber, PhoneNumber) VALUES
(1, 'Rahul', 'Sharma', 'DL-01-2021001', '9876543210'),
(2, 'Priya', 'Verma', 'MH-02-2020045', '9812345678'),
(3, 'Amit', 'Patel', 'KA-03-2019888', '9900112233');

INSERT INTO Vehicle (VehicleID, Make, Model, LicensePlate, DailyRate, Status) VALUES
(101, 'Toyota', 'Corolla', 'KA-01-MG-1234', 45.00, 'Rented'),
(102, 'Honda', 'City', 'KA-05-AB-5678', 50.00, 'Available'),
(103, 'Hyundai', 'Creta', 'MH-02-CD-9999', 65.00, 'Available');

INSERT INTO Rental (RentalID, CustomerID, VehicleID, RentalDate, ReturnDate, TotalCost) VALUES
(501, 1, 101, '2026-10-25', NULL, 0.00);
