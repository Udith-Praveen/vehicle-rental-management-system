import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#718096"))

        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "Vehicle Rental Management System")
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "RDBMS Lab Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, footer_text)
        self.drawString(54, 34, "Udith Praveen (2502052183) | B.tech / O4 | Sem 3")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.restoreState()

def build_pdf(filename="Vehicle_Rental_Management_System_Report.pdf"):
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        alignment=1,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    story = []

    # ==========================================
    # PAGE 1: COVER & STUDENT INFORMATION
    # ==========================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("VEHICLE RENTAL MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("RDBMS Lab Project Report", subtitle_style))
    story.append(Spacer(1, 12))

    student_data = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("Udith Praveen", body_style)],
        [Paragraph("<b>Registration Number</b>", body_style), Paragraph("2502052183", body_style)],
        [Paragraph("<b>Branch / Section</b>", body_style), Paragraph("B.tech / O4", body_style)],
        [Paragraph("<b>Semester</b>", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>Course</b>", body_style), Paragraph("Relational Database Management Systems (RDBMS) Lab", body_style)],
        [Paragraph("<b>Project Type</b>", body_style), Paragraph("Database & Front-End Application Integration", body_style)],
        [Paragraph("<b>Technologies</b>", body_style), Paragraph("Python 3.x, MySQL, Terminal Interface", body_style)],
        [Paragraph("<b>GitHub Link</b>", body_style), Paragraph("github.com/Udith-Praveen/vehicle-rental-management-system", body_style)]
    ]
    t_student = Table(student_data, colWidths=[2.1 * 72, 4.9 * 72])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#2B6CB0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 16))

    summary_text = (
        "<b>Project Summary:</b> This project is a simple vehicle rental management system "
        "built using MySQL and Python. It manages car inventory, customer information, rental bookings, "
        "returns with billing calculation, and vehicle maintenance logs through an interactive terminal interface. "
        "The database uses Primary Keys and Foreign Keys to keep all records connected and accurate, and uses "
        "SQL JOIN queries to display human-readable rental details."
    )
    t_box = Table([[Paragraph(summary_text, body_style)]], colWidths=[7.0 * 72])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_box)

    story.append(Spacer(1, 16))
    outline_data = [
        [Paragraph("<b>Section</b>", body_style), Paragraph("<b>Topic</b>", body_style)],
        [Paragraph("Section 1", body_style), Paragraph("Introduction and Problem Statement", body_style)],
        [Paragraph("Section 2", body_style), Paragraph("Database Design and Schema", body_style)],
        [Paragraph("Section 3", body_style), Paragraph("SQL Queries and Operations", body_style)],
        [Paragraph("Section 4", body_style), Paragraph("Python Front-End Application", body_style)],
        [Paragraph("Section 5", body_style), Paragraph("Project Demonstration Walkthrough", body_style)],
        [Paragraph("Section 6", body_style), Paragraph("Project Contribution", body_style)],
        [Paragraph("Section 7", body_style), Paragraph("References", body_style)]
    ]
    t_outline = Table(outline_data, colWidths=[1.5 * 72, 5.5 * 72])
    t_outline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_outline)
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: INTRODUCTION & DATABASE DESIGN
    # ==========================================
    story.append(Paragraph("1. Introduction and Problem Statement", h1_style))
    story.append(Paragraph(
        "Car rental companies deal with daily operations like tracking available vehicles, registering customer licenses, "
        "recording rental dates, and calculating payments upon return. Managing this on paper or spreadsheets easily leads to "
        "mistakes such as double booking a vehicle or losing track of customer records.",
        body_style
    ))
    story.append(Paragraph(
        "The goal of this project is to create a clean, working database in MySQL connected to a simple Python terminal interface. "
        "It allows an operator to add vehicles, register customers, rent out cars, return cars with automatic billing, and view all records.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Database Design and Schema", h1_style))
    story.append(Paragraph(
        "The database consists of 5 tables. Each table has a Primary Key to identify rows uniquely, and Foreign Keys are used to "
        "connect related information between tables.",
        body_style
    ))

    schema_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Primary Key</b>", body_style), Paragraph("<b>Foreign Key</b>", body_style), Paragraph("<b>Columns & Purpose</b>", body_style)],
        [Paragraph("<b>Customer</b>", body_style), Paragraph("CustomerID", code_style), Paragraph("None", body_style), Paragraph("FirstName, LastName, LicenseNumber (Unique), PhoneNumber. Stores customer details.", body_style)],
        [Paragraph("<b>Vehicle</b>", body_style), Paragraph("VehicleID", code_style), Paragraph("None", body_style), Paragraph("Make, Model, LicensePlate (Unique), DailyRate, Status. Stores vehicle inventory.", body_style)],
        [Paragraph("<b>Rental</b>", body_style), Paragraph("RentalID", code_style), Paragraph("CustomerID, VehicleID", body_style), Paragraph("RentalDate, ReturnDate, TotalCost. Links customer to rented car.", body_style)],
        [Paragraph("<b>Payment</b>", body_style), Paragraph("PaymentID", code_style), Paragraph("RentalID", body_style), Paragraph("PaymentDate, Amount, PaymentMethod. Records payment transactions.", body_style)],
        [Paragraph("<b>Maintenance</b>", body_style), Paragraph("MaintenanceID", code_style), Paragraph("VehicleID", body_style), Paragraph("ServiceDate, Description, Cost. Logs vehicle repairs and servicing.", body_style)]
    ]
    t_schema = Table(schema_data, colWidths=[1.1 * 72, 1.2 * 72, 1.7 * 72, 3.0 * 72])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_schema)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Table Relationships (1 : M):</b>", body_style))
    story.append(Paragraph("• <b>Customer to Rental (1 : M):</b> One customer can rent vehicles multiple times.", bullet_style))
    story.append(Paragraph("• <b>Vehicle to Rental (1 : M):</b> One vehicle can be rented repeatedly on different dates.", bullet_style))
    story.append(Paragraph("• <b>Rental to Payment (1 : M):</b> A rental can have one or more payments recorded.", bullet_style))
    story.append(Paragraph("• <b>Vehicle to Maintenance (1 : M):</b> A vehicle can have multiple service entries over time.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Referential Integrity:</b>", body_style))
    story.append(Paragraph(
        "Foreign Keys ensure that a rental cannot be created for a CustomerID or VehicleID that does not exist in the database. "
        "This prevents invalid or orphaned records.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: SQL QUERIES & OPERATIONS
    # ==========================================
    story.append(Paragraph("3. SQL Queries and Operations", h1_style))
    story.append(Paragraph(
        "The project uses standard SQL commands to create the database structure, insert records, update status, and query data.",
        body_style
    ))

    story.append(Paragraph("A. Table Creation (DDL)", h2_style))
    ddl_sql = (
        "CREATE TABLE Customer (\n"
        "    CustomerID INT PRIMARY KEY,\n"
        "    FirstName VARCHAR(50) NOT NULL,\n"
        "    LastName VARCHAR(50) NOT NULL,\n"
        "    LicenseNumber VARCHAR(30) UNIQUE NOT NULL,\n"
        "    PhoneNumber VARCHAR(15) NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Vehicle (\n"
        "    VehicleID INT PRIMARY KEY,\n"
        "    Make VARCHAR(50) NOT NULL, Model VARCHAR(50) NOT NULL,\n"
        "    LicensePlate VARCHAR(20) UNIQUE NOT NULL,\n"
        "    DailyRate DECIMAL(8,2) NOT NULL, Status VARCHAR(20) DEFAULT 'Available'\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Rental (\n"
        "    RentalID INT PRIMARY KEY,\n"
        "    CustomerID INT NOT NULL, VehicleID INT NOT NULL,\n"
        "    RentalDate DATE NOT NULL, ReturnDate DATE,\n"
        "    TotalCost DECIMAL(10,2) DEFAULT 0.00,\n"
        "    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;"
    )
    t_ddl = Table([[Preformatted(ddl_sql, code_style)]], colWidths=[7.0 * 72])
    t_ddl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ddl)

    story.append(Paragraph("B. Inserting and Updating Records (DML)", h2_style))
    dml_sql = (
        "-- Renting a vehicle (Insert rental record and change car status to 'Rented')\n"
        "INSERT INTO Rental (RentalID, CustomerID, VehicleID, RentalDate, TotalCost)\n"
        "VALUES (501, 1, 101, '2026-10-25', 0.00);\n"
        "UPDATE Vehicle SET Status = 'Rented' WHERE VehicleID = 101;\n\n"
        "-- Returning a vehicle (Set return date, total cost, and mark car 'Available')\n"
        "UPDATE Rental SET ReturnDate = '2026-10-28', TotalCost = 135.00 WHERE RentalID = 501;\n"
        "UPDATE Vehicle SET Status = 'Available' WHERE VehicleID = 101;"
    )
    t_dml = Table([[Preformatted(dml_sql, code_style)]], colWidths=[7.0 * 72])
    t_dml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_dml)

    story.append(Paragraph("C. Querying Data with SQL INNER JOIN (DQL)", h2_style))
    story.append(Paragraph(
        "Instead of showing raw numeric IDs, an INNER JOIN combines rows from Rental, Customer, and Vehicle tables to display "
        "the customer's name, car make, and model together:",
        body_style
    ))
    join_sql = (
        "SELECT \n"
        "    r.RentalID,\n"
        "    CONCAT(c.FirstName, ' ', c.LastName) AS Customer,\n"
        "    CONCAT(v.Make, ' ', v.Model) AS Vehicle,\n"
        "    v.LicensePlate,\n"
        "    r.RentalDate,\n"
        "    IFNULL(r.ReturnDate, 'Pending') AS ReturnDate,\n"
        "    r.TotalCost\n"
        "FROM Rental r\n"
        "JOIN Customer c ON r.CustomerID = c.CustomerID\n"
        "JOIN Vehicle v ON r.VehicleID = v.VehicleID\n"
        "ORDER BY r.RentalID DESC;"
    )
    t_join = Table([[Preformatted(join_sql, code_style)]], colWidths=[7.0 * 72])
    t_join.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_join)
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: FRONT-END, DEMO, CONTRIBUTION, REFS
    # ==========================================
    story.append(Paragraph("4. Python Front-End Application", h1_style))
    story.append(Paragraph(
        "The user interface is built in Python using <code>mysql.connector</code>. "
        "It provides a clear terminal menu where the user selects options to interact with the database. "
        "When an option is selected, Python executes the SQL query on MySQL and displays results neatly in ASCII tables.",
        body_style
    ))

    cli_sample = (
        "------------------------------------------- | Formatted Query Output (Show Available Vehicles):\n"
        "      VEHICLE RENTAL MANAGEMENT SYSTEM     | +------------+---------+---------+---------------+------------+-----------+\n"
        "------------------------------------------- | | Vehicle ID | Make    | Model   | License Plate | Daily Rate | Status    |\n"
        " 1. Add Vehicle        8. Rent a Vehicle    | +------------+---------+---------+---------------+------------+-----------+\n"
        " 2. Show All Vehicles  9. Return a Vehicle  | | 102        | Honda   | City    | KA-05-AB-5678 | 50.00      | Available |\n"
        " 3. Available Vehicles 10. Show All Rentals | | 103        | Hyundai | Creta   | MH-02-CD-9999 | 65.00      | Available |\n"
        " 4. Remove Vehicle     11. Log Payment      | +------------+---------+---------+---------------+------------+-----------+\n"
        " 15. Setup DB Tables   0. Exit Application  |"
    )
    t_cli = Table([[Preformatted(cli_sample, code_style)]], colWidths=[7.0 * 72])
    t_cli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2D3748")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1A202C")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cli)

    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Project Demonstration Walkthrough", h1_style))
    story.append(Paragraph("• <b>Database Setup:</b> Option 15 creates the database and all 5 tables with Primary and Foreign Keys.", bullet_style))
    story.append(Paragraph("• <b>Adding Records:</b> Options 1 and 5 insert new vehicles and register customer details.", bullet_style))
    story.append(Paragraph("• <b>Renting a Vehicle:</b> Option 8 records the rental and automatically updates the vehicle status to 'Rented'.", bullet_style))
    story.append(Paragraph("• <b>Viewing Rentals:</b> Option 10 runs the INNER JOIN query to show active and completed rentals with full customer and car details.", bullet_style))
    story.append(Paragraph("• <b>Returning a Vehicle:</b> Option 9 calculates the total rental fee, records the return date, and sets the car status back to 'Available'.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Project Contribution", h1_style))
    contrib_data = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("<b>Registration Number</b>", body_style), Paragraph("<b>Contribution</b>", body_style)],
        [
            Paragraph("<b>Udith Praveen</b>", body_style),
            Paragraph("<b>2502052183</b>", code_style),
            Paragraph(
                "• Designed the relational database schema, tables, and key constraints.<br/>"
                "• Wrote the complete SQL script in <code>schema.sql</code>.<br/>"
                "• Implemented database connection handling in <code>db_config.py</code>.<br/>"
                "• Built the terminal menu, ASCII table formatting, and CRUD functions in <code>main.py</code>.<br/>"
                "• Implemented the multi-table INNER JOIN query and prepared the documentation.",
                body_style
            )
        ]
    ]
    t_contrib = Table(contrib_data, colWidths=[1.4 * 72, 1.4 * 72, 4.2 * 72])
    t_contrib.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_contrib)

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. References", h1_style))
    story.append(Paragraph("1. R. Elmasri and S. B. Navathe, <i>Fundamentals of Database Systems</i>, 7th ed., Pearson, 2016.", bullet_style))
    story.append(Paragraph("2. A. Silberschatz, H. F. Korth, and S. Sudarshan, <i>Database System Concepts</i>, 7th ed., McGraw-Hill, 2019.", bullet_style))
    story.append(Paragraph("3. MySQL 8.0 Reference Manual, Oracle Corporation. URL: https://dev.mysql.com/doc/refman/8.0/en/", bullet_style))
    story.append(Paragraph("4. Python MySQL Connector Documentation. URL: https://dev.mysql.com/doc/connector-python/en/", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    build_pdf()
