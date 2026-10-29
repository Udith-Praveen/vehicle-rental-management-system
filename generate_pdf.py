import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, Image
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

        # Header on pages 2+
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "Manipal University Jaipur | DBMS Lab (CSC2131)")
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Vehicle Rental Management System")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer on pages 2+
        if self._pageNumber > 1:
            footer_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * 72 - 54, 34, footer_text)
            self.drawString(54, 34, "Udith Praveen (2502052183) | B.Tech CSE 3rd Sem | Section: B.tech/O4")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 46, 8.5 * 72 - 54, 46)

        self.restoreState()

def build_pdf(filename="Vehicle_Rental_Management_System_Report.pdf"):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(curr_dir, filename)
    logo_path = os.path.join(curr_dir, "muj_logo.jpeg")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    cover_main_title = ParagraphStyle(
        'CoverMainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1A202C"),
        alignment=1,
        spaceAfter=4
    )

    cover_course_code = ParagraphStyle(
        'CoverCourseCode',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#2B6CB0"),
        alignment=1,
        spaceAfter=4
    )

    cover_report_type = ParagraphStyle(
        'CoverReportType',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A202C"),
        alignment=1,
        spaceAfter=6
    )

    cover_session = ParagraphStyle(
        'CoverSession',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=25
    )

    cover_proj_title = ParagraphStyle(
        'CoverProjTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=30
    )

    cover_student_info = ParagraphStyle(
        'CoverStudentInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#2D3748"),
        alignment=1,
        spaceAfter=30
    )

    cover_dept_info = ParagraphStyle(
        'CoverDeptInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        alignment=1,
        spaceAfter=4
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
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
        spaceAfter=5
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

    center_bold = ParagraphStyle(
        'CenterBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=15
    )

    story = []

    # ==========================================
    # PAGE 1: OFFICIAL COVER PAGE (MANIPAL FORMAT)
    # ==========================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("DATABASE MANAGEMENT SYSTEMS LAB", cover_main_title))
    story.append(Paragraph("(CSC2131)", cover_course_code))
    story.append(Paragraph("PROJECT REPORT", cover_report_type))
    story.append(Paragraph("Academic Session: 2026-2027", cover_session))

    story.append(Paragraph("VEHICLE RENTAL MANAGEMENT SYSTEM", cover_proj_title))

    student_block = (
        "<b>By:</b><br/>"
        "<b>Name of Student:</b> Udith Praveen<br/>"
        "<b>Registration Number:</b> 2502052183<br/>"
        "<b>Section:</b> B.tech/O4"
    )
    story.append(Paragraph(student_block, cover_student_info))
    story.append(Spacer(1, 15))

    # University Logo
    if os.path.exists(logo_path):
        # 696 x 130 aspect ratio (approx 5.35 : 1)
        # width = 4.0 inches = 288 pt, height = 288 / 5.35 = 53.8 pt
        story.append(Image(logo_path, width=4.0 * 72, height=54))
    else:
        story.append(Paragraph("<b>MANIPAL UNIVERSITY JAIPUR</b>", cover_main_title))

    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>November 2026</b>", cover_dept_info))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Department of Computer Science and Engineering</b><br/>"
                           "<b>Manipal University Jaipur</b><br/>"
                           "VPO. Dehmi Kalan, Jaipur, Rajasthan, India – 303007", cover_dept_info))
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: DECLARATION BY THE STUDENT
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("DECLARATION BY THE STUDENT", center_bold))
    story.append(Spacer(1, 15))

    declaration_text = (
        "I hereby declare that this project <b>Vehicle Rental Management System</b> is my own work "
        "and that, to the best of my knowledge and belief, it contains no material previously published or written "
        "by another person nor material which has been accepted for the award of any other degree or diploma of the "
        "University or other Institute, except where due acknowledgements has been made in the text."
    )
    story.append(Paragraph(declaration_text, ParagraphStyle('DecText', parent=body_style, fontSize=10, leading=16)))
    story.append(Spacer(1, 60))

    sig_data = [
        [Paragraph("(Signature)", body_style), Paragraph("", body_style)],
        [Paragraph("<b>Place:</b> Jaipur", body_style), Paragraph("<b>Name of Student:</b> Udith Praveen", body_style)],
        [Paragraph("<b>Date:</b>", body_style), Paragraph("<b>Registration Number:</b> 2502052183", body_style)],
        [Paragraph("", body_style), Paragraph("B.Tech CSE 3rd Semester", body_style)],
        [Paragraph("", body_style), Paragraph("Section: B.tech/O4", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[3.2 * 72, 3.8 * 72])
    t_sig.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sig)
    story.append(PageBreak())

    # ==========================================
    # PAGE 3: TABLE OF CONTENTS (MANIPAL FORMAT)
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("TABLE OF CONTENTS", center_bold))
    story.append(Spacer(1, 10))

    toc_rows = [
        [Paragraph("<b>S. No</b>", body_style), Paragraph("<b>Contents</b>", body_style), Paragraph("<b>Page No.</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("Abstract", body_style), Paragraph("4", body_style)],
        [Paragraph("2", body_style), Paragraph("Introduction", body_style), Paragraph("4", body_style)],
        [Paragraph("3", body_style), Paragraph("Problem Statement", body_style), Paragraph("4", body_style)],
        [Paragraph("4", body_style), Paragraph("Objectives of the Project", body_style), Paragraph("4", body_style)],
        [Paragraph("5", body_style), Paragraph("System Requirements (Hardware and Software)", body_style), Paragraph("5", body_style)],
        [Paragraph("6", body_style), Paragraph("System Design and Database Schema", body_style), Paragraph("5", body_style)],
        [Paragraph("7", body_style), Paragraph("ER Diagram", body_style), Paragraph("5", body_style)],
        [Paragraph("8", body_style), Paragraph("Database and Table Creation", body_style), Paragraph("6", body_style)],
        [Paragraph("9", body_style), Paragraph("SQL Queries for Data Insertion, Updation, Deletion, and Retrieval", body_style), Paragraph("6", body_style)],
        [Paragraph("10", body_style), Paragraph("Front-End Design and Implementation (Case 1 only)", body_style), Paragraph("7", body_style)],
        [Paragraph("11", body_style), Paragraph("Results and Screenshots", body_style), Paragraph("7", body_style)],
        [Paragraph("12", body_style), Paragraph("Conclusion", body_style), Paragraph("8", body_style)],
        [Paragraph("13", body_style), Paragraph("Contributions by Team Members", body_style), Paragraph("8", body_style)],
        [Paragraph("14", body_style), Paragraph("References", body_style), Paragraph("8", body_style)],
    ]
    t_toc = Table(toc_rows, colWidths=[0.8 * 72, 5.2 * 72, 1.0 * 72])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================
    # PAGE 4: ABSTRACT, INTRODUCTION, PROBLEM, OBJECTIVES
    # ==========================================
    story.append(Paragraph("1. Abstract", h1_style))
    story.append(Paragraph(
        "The Vehicle Rental Management System is a database-driven application developed for managing car rental operations. "
        "The system replaces manual paper logs by connecting a relational MySQL database with a clean Python terminal interface. "
        "It maintains information on fleet vehicles, registered customers, rental transactions, billing payments, and maintenance logs. "
        "By enforcing Primary and Foreign Key constraints, the database ensures referential integrity across all entities, while "
        "multi-table SQL INNER JOIN queries combine related records into readable rental summaries.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Introduction", h1_style))
    story.append(Paragraph(
        "Vehicle rental services operate in a fast-paced environment where cars are rented, returned, and serviced continuously. "
        "A reliable database system is necessary to keep track of which cars are available, who is currently renting a car, "
        "and whether maintenance has been completed. This project implements a relational database solution in MySQL integrated "
        "with a Python console front-end to streamline day-to-day rental tasks.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Problem Statement", h1_style))
    story.append(Paragraph(
        "When vehicle rental records are managed using paper logs or basic spreadsheets, businesses frequently run into "
        "common issues: duplicate vehicle bookings, misplaced customer driving license numbers, unrecorded return dates, "
        "and incorrect billing calculations. Without referential constraints, records become disconnected and difficult to audit.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Objectives of the Project", h1_style))
    story.append(Paragraph("• <b>Database Design:</b> Create a normalized relational schema with 5 dedicated tables in MySQL.", bullet_style))
    story.append(Paragraph("• <b>Referential Integrity:</b> Link tables using Primary and Foreign Keys with cascading actions.", bullet_style))
    story.append(Paragraph("• <b>CRUD Operations:</b> Support adding vehicles/customers, updating car statuses, recording rentals, and billing.", bullet_style))
    story.append(Paragraph("• <b>Data Retrieval:</b> Use SQL INNER JOIN queries to display comprehensive rental contracts in the terminal.", bullet_style))
    story.append(Paragraph("• <b>Front-End Integration:</b> Provide an easy-to-use Python menu interface for database administration.", bullet_style))
    story.append(PageBreak())

    # ==========================================
    # PAGE 5: SYSTEM REQS, SCHEMA, ER DIAGRAM
    # ==========================================
    story.append(Paragraph("5. System Requirements (Hardware and Software)", h1_style))
    req_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Specification</b>", body_style)],
        [Paragraph("Operating System", body_style), Paragraph("Windows 10 / 11, Linux, or macOS", body_style)],
        [Paragraph("Database Management System", body_style), Paragraph("MySQL Server 8.0+ (InnoDB Storage Engine)", body_style)],
        [Paragraph("Programming Language", body_style), Paragraph("Python 3.8 or higher", body_style)],
        [Paragraph("Python Database Driver", body_style), Paragraph("mysql-connector-python (v8.0+)", body_style)],
        [Paragraph("Hardware Requirements", body_style), Paragraph("Standard PC / Laptop (Intel Core i3 / AMD Ryzen 3+, 4 GB RAM, 500 MB Free Disk)", body_style)]
    ]
    t_req = Table(req_data, colWidths=[2.2 * 72, 4.8 * 72])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_req)

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. System Design and Database Schema", h1_style))
    story.append(Paragraph(
        "The system is organized into 5 relational tables:",
        body_style
    ))

    schema_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Primary Key</b>", body_style), Paragraph("<b>Foreign Key</b>", body_style), Paragraph("<b>Description & Attributes</b>", body_style)],
        [Paragraph("<b>Customer</b>", body_style), Paragraph("CustomerID", code_style), Paragraph("None", body_style), Paragraph("FirstName, LastName, LicenseNumber (Unique), PhoneNumber", body_style)],
        [Paragraph("<b>Vehicle</b>", body_style), Paragraph("VehicleID", code_style), Paragraph("None", body_style), Paragraph("Make, Model, LicensePlate (Unique), DailyRate, Status", body_style)],
        [Paragraph("<b>Rental</b>", body_style), Paragraph("RentalID", code_style), Paragraph("CustomerID, VehicleID", body_style), Paragraph("RentalDate, ReturnDate, TotalCost. Connects customer to vehicle.", body_style)],
        [Paragraph("<b>Payment</b>", body_style), Paragraph("PaymentID", code_style), Paragraph("RentalID", body_style), Paragraph("PaymentDate, Amount, PaymentMethod (Cash/Card/UPI)", body_style)],
        [Paragraph("<b>Maintenance</b>", body_style), Paragraph("MaintenanceID", code_style), Paragraph("VehicleID", body_style), Paragraph("ServiceDate, Description, Cost. Logs vehicle servicing.", body_style)]
    ]
    t_schema = Table(schema_data, colWidths=[1.1 * 72, 1.2 * 72, 1.6 * 72, 3.1 * 72])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_schema)

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. ER Diagram (Entity-Relationship Representation)", h1_style))
    er_text = (
        "  +------------+                                   +------------+\n"
        "  |  CUSTOMER  |                                   |  VEHICLE   |\n"
        "  +------------+                                   +------------+\n"
        "        | 1                                              | 1\n"
        "        |                                                |\n"
        "        | [Places Rental]                                | [Assigned To]\n"
        "        v M                                              v M\n"
        "  +-------------------------------------------------------------+\n"
        "  |                           RENTAL                            |\n"
        "  +-------------------------------------------------------------+\n"
        "        | 1                                              |\n"
        "        | [Settled via]                                  | 1 [Undergoes]\n"
        "        v M                                              v M\n"
        "  +-------------+                                  +-------------+\n"
        "  |   PAYMENT   |                                  | MAINTENANCE |\n"
        "  +-------------+                                  +-------------+"
    )
    t_er = Table([[Preformatted(er_text, code_style)]], colWidths=[7.0 * 72])
    t_er.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_er)
    story.append(PageBreak())

    # ==========================================
    # PAGE 6: DATABASE CREATION & SQL QUERIES
    # ==========================================
    story.append(Paragraph("8. Database and Table Creation (DDL)", h1_style))
    ddl_sql = (
        "CREATE DATABASE IF NOT EXISTS rental_db;\n"
        "USE rental_db;\n\n"
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
        "    RentalDate DATE NOT NULL, ReturnDate DATE, TotalCost DECIMAL(10,2) DEFAULT 0.00,\n"
        "    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;"
    )
    t_ddl = Table([[Preformatted(ddl_sql, code_style)]], colWidths=[7.0 * 72])
    t_ddl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ddl)

    story.append(Spacer(1, 4))
    story.append(Paragraph("9. SQL Queries for Data Insertion, Updation, Deletion, and Retrieval", h1_style))
    story.append(Paragraph("<b>A. Data Insertion & Status Synchronization (DML):</b>", body_style))
    dml_sql = (
        "-- Renting out a vehicle (adds rental row and updates vehicle status)\n"
        "INSERT INTO Rental (RentalID, CustomerID, VehicleID, RentalDate, TotalCost)\n"
        "VALUES (501, 1, 101, '2026-10-25', 0.00);\n"
        "UPDATE Vehicle SET Status = 'Rented' WHERE VehicleID = 101;\n\n"
        "-- Returning a vehicle (updates return date, total cost, and restores status)\n"
        "UPDATE Rental SET ReturnDate = '2026-10-28', TotalCost = 135.00 WHERE RentalID = 501;\n"
        "UPDATE Vehicle SET Status = 'Available' WHERE VehicleID = 101;"
    )
    t_dml = Table([[Preformatted(dml_sql, code_style)]], colWidths=[7.0 * 72])
    t_dml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_dml)

    story.append(Paragraph("<b>B. Multi-Table Relational Data Retrieval (DQL - INNER JOIN):</b>", body_style))
    join_sql = (
        "SELECT \n"
        "    r.RentalID,\n"
        "    CONCAT(c.FirstName, ' ', c.LastName) AS Customer,\n"
        "    CONCAT(v.Make, ' ', v.Model) AS Vehicle,\n"
        "    v.LicensePlate, r.RentalDate,\n"
        "    IFNULL(r.ReturnDate, 'Pending') AS ReturnDate, r.TotalCost\n"
        "FROM Rental r\n"
        "JOIN Customer c ON r.CustomerID = c.CustomerID\n"
        "JOIN Vehicle v ON r.VehicleID = v.VehicleID\n"
        "ORDER BY r.RentalID DESC;"
    )
    t_join = Table([[Preformatted(join_sql, code_style)]], colWidths=[7.0 * 72])
    t_join.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_join)
    story.append(PageBreak())

    # ==========================================
    # PAGE 7: FRONT-END IMPLEMENTATION & RESULTS
    # ==========================================
    story.append(Paragraph("10. Front-End Design and Implementation (Case 1 only)", h1_style))
    story.append(Paragraph(
        "The front-end is written in Python and connects directly to MySQL using <code>mysql.connector</code>. "
        "The project is structured into modular scripts:",
        body_style
    ))
    story.append(Paragraph("• <b>db_config.py:</b> Manages database host, port, user, and password credentials. Automatically creates <code>rental_db</code> on startup and runs table creation queries.", bullet_style))
    story.append(Paragraph("• <b>main.py:</b> Implements the console menu loop, user input prompts, business validation (e.g. checking if a car is available before renting), and formatted table printing.", bullet_style))
    story.append(Paragraph("• <b>connection.py:</b> Entry point delegating directly to <code>main.py</code>.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("11. Results and Screenshots", h1_style))
    story.append(Paragraph(
        "The following console outputs demonstrate the interactive menu and formatted tabular data displayed to the user:",
        body_style
    ))

    cli_sample = (
        "------------------------------------------- | Formatted Query Output (Available Vehicles):\n"
        "      VEHICLE RENTAL MANAGEMENT SYSTEM     | +------------+---------+---------+---------------+------------+-----------+\n"
        "------------------------------------------- | | Vehicle ID | Make    | Model   | License Plate | Daily Rate | Status    |\n"
        " 1. Add Vehicle        8. Rent a Vehicle    | +------------+---------+---------+---------------+------------+-----------+\n"
        " 2. Show All Vehicles  9. Return a Vehicle  | | 102        | Honda   | City    | KA-05-AB-5678 | 50.00      | Available |\n"
        " 3. Available Vehicles 10. Show All Rentals | | 103        | Hyundai | Creta   | MH-02-CD-9999 | 65.00      | Available |\n"
        " 4. Remove Vehicle     11. Log Payment      | +------------+---------+---------+---------------+------------+-----------+\n"
        " 5. Add Customer       12. Show Payments    |\n"
        " 6. Show All Customers 13. Log Maintenance  | Sample Multi-Table JOIN Output (Option 10):\n"
        " 7. Remove Customer    14. Show Maintenance | +-----------+--------------+---------------+---------------+-------------+\n"
        " 15. Setup DB Tables   0. Exit Application  | | Rental ID | Customer     | Vehicle       | Rental Date   | Total Cost  |\n"
        "------------------------------------------- | +-----------+--------------+---------------+---------------+-------------+\n"
        "                                            | | 501       | Rahul Sharma | Toyota Corolla| 2026-10-25    | $0.00       |\n"
        "                                            | +-----------+--------------+---------------+---------------+-------------+"
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
    story.append(PageBreak())

    # ==========================================
    # PAGE 8: CONCLUSION, CONTRIBUTIONS, REFS
    # ==========================================
    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(Paragraph(
        "The Vehicle Rental Management System successfully demonstrates the integration of a Python terminal front-end "
        "with a MySQL relational database. The project fulfills all core requirements: database and table creation, "
        "referential integrity enforcement through Primary and Foreign Keys, CRUD data management, and data retrieval "
        "using multi-table SQL INNER JOIN queries. The modular codebase allows easy extension, such as adding a graphical "
        "user interface or online booking capabilities in the future.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("13. Contributions by Team Members", h1_style))
    story.append(Paragraph(
        "This project was developed individually by <b>Udith Praveen</b> (Registration Number: <b>2502052183</b>). "
        "Key contributions include:",
        body_style
    ))
    story.append(Paragraph("• Designed the 5-table relational schema and foreign key constraints in MySQL.", bullet_style))
    story.append(Paragraph("• Wrote the complete DDL and DML scripts in <code>schema.sql</code>.", bullet_style))
    story.append(Paragraph("• Implemented database connection handling and auto-setup in <code>db_config.py</code>.", bullet_style))
    story.append(Paragraph("• Developed the terminal menu, ASCII table renderer, and CRUD operations in <code>main.py</code>.", bullet_style))
    story.append(Paragraph("• Authored multi-table SQL INNER JOIN queries and prepared the formal documentation.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("14. References", h1_style))
    story.append(Paragraph("1. R. Elmasri and S. B. Navathe, <i>Fundamentals of Database Systems</i>, 7th ed., Pearson, 2016.", bullet_style))
    story.append(Paragraph("2. A. Silberschatz, H. F. Korth, and S. Sudarshan, <i>Database System Concepts</i>, 7th ed., McGraw-Hill, 2019.", bullet_style))
    story.append(Paragraph("3. MySQL 8.0 Reference Manual, Oracle Corporation. URL: https://dev.mysql.com/doc/refman/8.0/en/", bullet_style))
    story.append(Paragraph("4. Python MySQL Connector Documentation. URL: https://dev.mysql.com/doc/connector-python/en/", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    build_pdf()
