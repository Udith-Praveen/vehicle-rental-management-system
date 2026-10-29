import sys
from db_config import get_connection, setup_tables

def print_table(headers, rows):
    if not rows:
        print("\nNo records found.\n")
        return

    col_widths = []
    for i in range(len(headers)):
        max_w = len(headers[i])
        for r in rows:
            val = str(r[i]) if r[i] is not None else "NULL"
            if len(val) > max_w:
                max_w = len(val)
        col_widths.append(max_w)

    border = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers))) + " |"

    print("\n" + border)
    print(header_line)
    print(border)
    for r in rows:
        row_str = "| " + " | ".join((str(r[i]) if r[i] is not None else "NULL").ljust(col_widths[i]) for i in range(len(headers))) + " |"
        print(row_str)
    print(border + "\n")

def add_vehicle(cur, conn):
    print("\n--- Add Vehicle ---")
    try:
        vid = int(input("Enter vehicle id: ").strip())
        make = input("Enter make: ").strip()
        model = input("Enter model: ").strip()
        plate = input("Enter license plate: ").strip()
        rate = float(input("Enter daily rate: ").strip())

        query = "INSERT INTO Vehicle (VehicleID, Make, Model, LicensePlate, DailyRate, Status) VALUES (%s, %s, %s, %s, %s, 'Available')"
        cur.execute(query, (vid, make, model, plate, rate))
        conn.commit()
        print(f"Vehicle {make} {model} added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def show_vehicles(cur, available_only=False):
    try:
        if available_only:
            print("\n--- Available Vehicles ---")
            cur.execute("SELECT VehicleID, Make, Model, LicensePlate, DailyRate, Status FROM Vehicle WHERE Status = 'Available' ORDER BY VehicleID")
        else:
            print("\n--- All Vehicles ---")
            cur.execute("SELECT VehicleID, Make, Model, LicensePlate, DailyRate, Status FROM Vehicle ORDER BY VehicleID")
        
        rows = cur.fetchall()
        headers = ["Vehicle ID", "Make", "Model", "License Plate", "Daily Rate", "Status"]
        print_table(headers, rows)
    except Exception as e:
        print("Error fetching vehicles:", e)

def remove_vehicle(cur, conn):
    print("\n--- Remove Vehicle ---")
    show_vehicles(cur)
    try:
        vid = int(input("Enter vehicle id to remove: ").strip())
        cur.execute("SELECT Make, Model FROM Vehicle WHERE VehicleID = %s", (vid,))
        v = cur.fetchone()
        if not v:
            print("Vehicle not found.")
            return

        conf = input(f"Delete {v[0]} {v[1]} (id {vid})? (y/n): ").strip().lower()
        if conf == 'y':
            cur.execute("DELETE FROM Vehicle WHERE VehicleID = %s", (vid,))
            conn.commit()
            print("Vehicle deleted.")
        else:
            print("Cancelled.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def add_customer(cur, conn):
    print("\n--- Add Customer ---")
    try:
        cid = int(input("Enter customer id: ").strip())
        fname = input("Enter first name: ").strip()
        lname = input("Enter last name: ").strip()
        lic = input("Enter license number: ").strip()
        ph = input("Enter phone number: ").strip()

        cur.execute("INSERT INTO Customer (CustomerID, FirstName, LastName, LicenseNumber, PhoneNumber) VALUES (%s, %s, %s, %s, %s)", (cid, fname, lname, lic, ph))
        conn.commit()
        print(f"Customer {fname} {lname} added successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def show_customers(cur):
    print("\n--- Customer List ---")
    try:
        cur.execute("SELECT CustomerID, FirstName, LastName, LicenseNumber, PhoneNumber FROM Customer ORDER BY CustomerID")
        rows = cur.fetchall()
        headers = ["Customer ID", "First Name", "Last Name", "License", "Phone"]
        print_table(headers, rows)
    except Exception as e:
        print("Error fetching customers:", e)

def remove_customer(cur, conn):
    print("\n--- Remove Customer ---")
    show_customers(cur)
    try:
        cid = int(input("Enter customer id to remove: ").strip())
        cur.execute("DELETE FROM Customer WHERE CustomerID = %s", (cid,))
        conn.commit()
        print("Customer deleted.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def rent_vehicle(cur, conn):
    print("\n--- Rent Out Vehicle ---")
    show_vehicles(cur, available_only=True)
    try:
        rid = int(input("Enter rental id: ").strip())
        cid = int(input("Enter customer id: ").strip())
        vid = int(input("Enter vehicle id to rent: ").strip())
        rdate = input("Enter rental date (YYYY-MM-DD): ").strip()

        cur.execute("SELECT Status FROM Vehicle WHERE VehicleID = %s", (vid,))
        res = cur.fetchone()
        if not res:
            print("Vehicle does not exist.")
            return
        if res[0] != 'Available':
            print(f"Vehicle is not available (current status: {res[0]}).")
            return

        cur.execute("INSERT INTO Rental (RentalID, CustomerID, VehicleID, RentalDate, TotalCost) VALUES (%s, %s, %s, %s, 0.00)", (rid, cid, vid, rdate))
        cur.execute("UPDATE Vehicle SET Status = 'Rented' WHERE VehicleID = %s", (vid,))
        conn.commit()
        print("Vehicle rented out successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def return_vehicle(cur, conn):
    print("\n--- Return Vehicle ---")
    try:
        rid = int(input("Enter rental id: ").strip())
        
        cur.execute("""
            SELECT r.VehicleID, v.Make, v.Model, v.DailyRate, r.RentalDate
            FROM Rental r
            JOIN Vehicle v ON r.VehicleID = v.VehicleID
            WHERE r.RentalID = %s
        """, (rid,))
        data = cur.fetchone()

        if not data:
            print("Rental record not found.")
            return

        vid, make, model, rate, rent_date = data
        print(f"Vehicle: {make} {model} | Rate: {rate}/day | Rented on: {rent_date}")

        retdate = input("Enter return date (YYYY-MM-DD): ").strip()
        days_str = input("Enter days rented (press enter to enter total manually): ").strip()

        if days_str:
            total_cost = float(days_str) * float(rate)
            print(f"Total calculated cost: {total_cost:.2f}")
        else:
            total_cost = float(input("Enter total cost: ").strip())

        cur.execute("UPDATE Rental SET ReturnDate = %s, TotalCost = %s WHERE RentalID = %s", (retdate, total_cost, rid))
        cur.execute("UPDATE Vehicle SET Status = 'Available' WHERE VehicleID = %s", (vid,))
        conn.commit()
        print("Vehicle returned and marked as available.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def show_rentals(cur):
    print("\n--- Rentals List ---")
    try:
        query = """
        SELECT 
            r.RentalID,
            CONCAT(c.FirstName, ' ', c.LastName) AS Customer,
            CONCAT(v.Make, ' ', v.Model) AS Vehicle,
            v.LicensePlate,
            r.RentalDate,
            IFNULL(r.ReturnDate, 'Pending') AS ReturnDate,
            r.TotalCost
        FROM Rental r
        JOIN Customer c ON r.CustomerID = c.CustomerID
        JOIN Vehicle v ON r.VehicleID = v.VehicleID
        ORDER BY r.RentalID DESC
        """
        cur.execute(query)
        rows = cur.fetchall()
        headers = ["Rental ID", "Customer", "Vehicle", "Plate", "Rental Date", "Return Date", "Total Cost"]
        print_table(headers, rows)
    except Exception as e:
        print("Error fetching rentals:", e)

def log_payment(cur, conn):
    print("\n--- Log Payment ---")
    try:
        pid = int(input("Enter payment id: ").strip())
        rid = int(input("Enter rental id: ").strip())
        pdate = input("Enter payment date (YYYY-MM-DD): ").strip()
        amt = float(input("Enter amount: ").strip())
        method = input("Enter payment method (Cash/Card/UPI): ").strip()

        cur.execute("INSERT INTO Payment (PaymentID, RentalID, PaymentDate, Amount, PaymentMethod) VALUES (%s, %s, %s, %s, %s)", (pid, rid, pdate, amt, method))
        conn.commit()
        print("Payment logged successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def show_payments(cur):
    print("\n--- Payments History ---")
    try:
        cur.execute("SELECT PaymentID, RentalID, PaymentDate, Amount, PaymentMethod FROM Payment ORDER BY PaymentID DESC")
        rows = cur.fetchall()
        headers = ["Payment ID", "Rental ID", "Date", "Amount", "Method"]
        print_table(headers, rows)
    except Exception as e:
        print("Error fetching payments:", e)

def log_maintenance(cur, conn):
    print("\n--- Log Vehicle Maintenance ---")
    show_vehicles(cur)
    try:
        mid = int(input("Enter maintenance id: ").strip())
        vid = int(input("Enter vehicle id: ").strip())
        sdate = input("Enter service date (YYYY-MM-DD): ").strip()
        desc = input("Enter description: ").strip()
        cost = float(input("Enter cost: ").strip())

        cur.execute("INSERT INTO Maintenance (MaintenanceID, VehicleID, ServiceDate, Description, Cost) VALUES (%s, %s, %s, %s, %s)", (mid, vid, sdate, desc, cost))
        
        status_ch = input("Change vehicle status to 'Maintenance'? (y/n): ").strip().lower()
        if status_ch == 'y':
            cur.execute("UPDATE Vehicle SET Status = 'Maintenance' WHERE VehicleID = %s", (vid,))

        conn.commit()
        print("Maintenance logged.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def show_maintenance(cur):
    print("\n--- Maintenance Logs ---")
    try:
        query = """
        SELECT m.MaintenanceID, CONCAT(v.Make, ' ', v.Model), m.ServiceDate, m.Description, m.Cost
        FROM Maintenance m
        JOIN Vehicle v ON m.VehicleID = v.VehicleID
        ORDER BY m.MaintenanceID DESC
        """
        cur.execute(query)
        rows = cur.fetchall()
        headers = ["ID", "Vehicle", "Date", "Description", "Cost"]
        print_table(headers, rows)
    except Exception as e:
        print("Error fetching maintenance:", e)

def main():
    conn = get_connection()
    if not conn:
        print("Unable to connect to database.")
        sys.exit(1)

    cur = conn.cursor()
    setup_tables(cur, conn, seed_sample_data=True, verbose=False)

    while True:
        print("\n-------------------------------------------")
        print("      VEHICLE RENTAL MANAGEMENT SYSTEM     ")
        print("-------------------------------------------")
        print(" 1. Add Vehicle")
        print(" 2. Show All Vehicles")
        print(" 3. Show Available Vehicles")
        print(" 4. Remove Vehicle")
        print(" 5. Add Customer")
        print(" 6. Show All Customers")
        print(" 7. Remove Customer")
        print(" 8. Rent a Vehicle")
        print(" 9. Return a Vehicle")
        print("10. Show All Rentals")
        print("11. Log Payment")
        print("12. Show Payment History")
        print("13. Log Maintenance")
        print("14. Show Maintenance Records")
        print("15. Reset / Setup Database Tables")
        print(" 0. Exit")
        print("-------------------------------------------")

        choice = input("Enter option (0-15): ").strip()

        if choice == '1':
            add_vehicle(cur, conn)
        elif choice == '2':
            show_vehicles(cur, available_only=False)
        elif choice == '3':
            show_vehicles(cur, available_only=True)
        elif choice == '4':
            remove_vehicle(cur, conn)
        elif choice == '5':
            add_customer(cur, conn)
        elif choice == '6':
            show_customers(cur)
        elif choice == '7':
            remove_customer(cur, conn)
        elif choice == '8':
            rent_vehicle(cur, conn)
        elif choice == '9':
            return_vehicle(cur, conn)
        elif choice == '10':
            show_rentals(cur)
        elif choice == '11':
            log_payment(cur, conn)
        elif choice == '12':
            show_payments(cur)
        elif choice == '13':
            log_maintenance(cur, conn)
        elif choice == '14':
            show_maintenance(cur)
        elif choice == '15':
            ans = input("Setup tables now? (y/n): ").strip().lower()
            if ans == 'y':
                with_sample = input("Include sample data? (y/n): ").strip().lower() == 'y'
                setup_tables(cur, conn, seed_sample_data=with_sample)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid option, try again.")

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
