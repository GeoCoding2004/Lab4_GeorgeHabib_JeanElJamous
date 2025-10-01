import sys
import csv
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFormLayout,
                             QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QDialog, QDialogButtonBox,
                             QTabWidget, QComboBox)

from school_system_backend import Student, Instructor, Course
from database_manager import DatabaseManager


# --- Edit Dialogs ---
# A separate dialog class for each record type keeps the code cleaner.

class EditStudentDialog(QDialog):
    """A dialog window for editing the details of an existing student.

    This dialog is pre-populated with the student's current data and provides
    input fields for the user to modify the name, age, and email.

    :param student_data: A tuple containing the current data of the student (id, name, age, email).
    :type student_data: tuple
    :param parent: The parent widget for this dialog, defaults to None.
    :type parent: QWidget, optional
    """
    def __init__(self, student_data, parent=None):
        """Constructor method. Initializes the dialog's UI elements."""
        super().__init__(parent)
        self.setWindowTitle("Edit Student")
        # student_data is a tuple from the database: (id, name, age, email)
        self.student_id = student_data[0]
        layout = QFormLayout(self)
        self.name_edit = QLineEdit(student_data[1])
        self.age_edit = QLineEdit(str(student_data[2]))
        self.email_edit = QLineEdit(student_data[3])
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Age:", self.age_edit)
        layout.addRow("Email:", self.email_edit)
        # Using the standard OK/Cancel buttons.
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Retrieves the edited data from the dialog's input fields.

        :return: The student's ID and the updated name, age, and email.
        :rtype: tuple
        """
        # Helper to pass the edited data back to the main window.
        return (self.student_id, self.name_edit.text(), self.age_edit.text(), self.email_edit.text())

class EditInstructorDialog(QDialog):
    """A dialog window for editing the details of an existing instructor.

    This dialog is pre-populated with the instructor's current data and provides
    input fields for the user to modify the name, age, and email.

    :param instructor_data: A tuple containing the current data of the instructor (id, name, age, email).
    :type instructor_data: tuple
    :param parent: The parent widget for this dialog, defaults to None.
    :type parent: QWidget, optional
    """
    # Same as the student dialog, just for instructors.
    def __init__(self, instructor_data, parent=None):
        """Constructor method. Initializes the dialog's UI elements."""
        super().__init__(parent)
        self.setWindowTitle("Edit Instructor")
        self.instructor_id = instructor_data[0]
        layout = QFormLayout(self)
        self.name_edit = QLineEdit(instructor_data[1])
        self.age_edit = QLineEdit(str(instructor_data[2]))
        self.email_edit = QLineEdit(instructor_data[3])
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Age:", self.age_edit)
        layout.addRow("Email:", self.email_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Retrieves the edited data from the dialog's input fields.

        :return: The instructor's ID and the updated name, age, and email.
        :rtype: tuple
        """
        return (self.instructor_id, self.name_edit.text(), self.age_edit.text(), self.email_edit.text())

class EditCourseDialog(QDialog):
    """A dialog window for editing the details of an existing course.

    This dialog is pre-populated with the course's current data and provides
    an input field for the user to modify the course name.

    :param course_data: A tuple containing the current data of the course (id, name, instructor_id).
    :type course_data: tuple
    :param parent: The parent widget for this dialog, defaults to None.
    :type parent: QWidget, optional
    """
    # Simpler dialog for courses, since I'm only editing the name for now.
    def __init__(self, course_data, parent=None):
        """Constructor method. Initializes the dialog's UI elements."""
        super().__init__(parent)
        self.setWindowTitle("Edit Course")
        self.course_id = course_data[0]
        layout = QFormLayout(self)
        self.name_edit = QLineEdit(course_data[1])
        layout.addRow("Course Name:", self.name_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Retrieves the edited data from the dialog's input fields.

        :return: The course's ID and the updated name.
        :rtype: tuple
        """
        return (self.course_id, self.name_edit.text())


# Main application class for the PyQt5 GUI.
class SchoolManagementApp(QWidget):
    """This class represents the main PyQt5 application for managing the school system.
    It provides a GUI to add, edit, delete, and view students, instructors, and courses.
    It also allows registering students for courses and provides data export and backup functionalities.
    """
    def __init__(self):
        """Constructor method to set up the main application window and initialize the database manager."""
        super().__init__()
        self.db_manager = DatabaseManager("school.db")
        self.db_manager.setup_database()
        self.init_ui()

    def init_ui(self):
        """Creates and arranges all the main widgets in the application window.

        This includes setting up the tabbed interface for adding records, the main table
        for displaying all data, and the action buttons for editing, deleting, and other utilities.

        :return: None
        :rtype: None
        """
        self.setWindowTitle("School Management System (PyQt5)")
        self.setGeometry(100, 100, 800, 700)
        main_layout = QVBoxLayout()

        # Using tabs for the forms so the window doesn't get ridiculously long.
        tab_widget = QTabWidget()

        # Student Tab
        student_tab = QWidget()
        student_layout = QFormLayout(student_tab)
        self.name_entry = QLineEdit()
        self.age_entry = QLineEdit()
        self.email_entry = QLineEdit()
        self.id_entry = QLineEdit()
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        student_layout.addRow(QLabel("Name:"), self.name_entry)
        student_layout.addRow(QLabel("Age:"), self.age_entry)
        student_layout.addRow(QLabel("Email:"), self.email_entry)
        student_layout.addRow(QLabel("Student ID:"), self.id_entry)
        student_layout.addRow(self.add_student_button)
        tab_widget.addTab(student_tab, "Add Student")

        # Instructor Tab
        instructor_tab = QWidget()
        instructor_layout = QFormLayout(instructor_tab)
        self.inst_name_entry = QLineEdit()
        self.inst_age_entry = QLineEdit()
        self.inst_email_entry = QLineEdit()
        self.inst_id_entry = QLineEdit()
        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        instructor_layout.addRow(QLabel("Name:"), self.inst_name_entry)
        instructor_layout.addRow(QLabel("Age:"), self.inst_age_entry)
        instructor_layout.addRow(QLabel("Email:"), self.inst_email_entry)
        instructor_layout.addRow(QLabel("Instructor ID:"), self.inst_id_entry)
        instructor_layout.addRow(self.add_instructor_button)
        tab_widget.addTab(instructor_tab, "Add Instructor")

        # Course Tab
        course_tab = QWidget()
        course_layout = QFormLayout(course_tab)
        self.course_name_entry = QLineEdit()
        self.course_id_entry = QLineEdit()
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        course_layout.addRow(QLabel("Course Name:"), self.course_name_entry)
        course_layout.addRow(QLabel("Course ID:"), self.course_id_entry)
        course_layout.addRow(self.add_course_button)
        tab_widget.addTab(course_tab, "Add Course")

        # Registration Tab
        registration_tab = QWidget()
        reg_layout = QVBoxLayout(registration_tab)
        reg_form_group = QGroupBox("Register Student for Course")
        reg_form_layout = QFormLayout()
        self.reg_student_combo = QComboBox()
        self.reg_course_combo = QComboBox()
        self.register_button = QPushButton("Register Student")
        self.register_button.clicked.connect(self.register_student)
        reg_form_layout.addRow(QLabel("Select Student:"), self.reg_student_combo)
        reg_form_layout.addRow(QLabel("Select Course:"), self.reg_course_combo)
        reg_form_layout.addRow(self.register_button)
        reg_form_group.setLayout(reg_form_layout)

        self.registrations_table = QTableWidget()
        self.registrations_table.setColumnCount(4)
        self.registrations_table.setHorizontalHeaderLabels(["Student ID", "Student Name", "Course ID", "Course Name"])
        self.registrations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.registrations_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        reg_layout.addWidget(reg_form_group)
        reg_layout.addWidget(self.registrations_table)
        tab_widget.addTab(registration_tab, "Registrations")

        main_layout.addWidget(tab_widget)

        # Main table for showing all records.
        records_group = QGroupBox("All Records")
        records_layout = QVBoxLayout()
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(4)
        self.records_table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Details"])
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.records_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.records_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        records_layout.addWidget(self.records_table)
        records_group.setLayout(records_layout)
        main_layout.addWidget(records_group, 1)

        # Action buttons at the bottom.
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        self.edit_button = QPushButton("Edit Selected"); self.edit_button.clicked.connect(self.edit_record)
        self.delete_button = QPushButton("Delete Selected"); self.delete_button.clicked.connect(self.delete_record)
        self.export_csv_button = QPushButton("Export Students to CSV"); self.export_csv_button.clicked.connect(self.export_to_csv)
        self.backup_db_button = QPushButton("Backup Database"); self.backup_db_button.clicked.connect(self.backup_database)
        actions_layout.addWidget(self.edit_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addStretch()
        actions_layout.addWidget(self.export_csv_button)
        actions_layout.addWidget(self.backup_db_button)
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        self.setLayout(main_layout)
        self.refresh_all_data()

    def refresh_all_data(self):
        """Refreshes all data views in the UI to ensure they are synchronized with the database.

        This method is a convenient wrapper that calls all individual refresh methods for the
        main records table, the registration dropdowns, and the registrations table.

        :return: None
        :rtype: None
        """
        # Central function to refresh all the UI bits after a data change.
        self.refresh_records_table()
        self.update_registration_comboboxes()
        self.refresh_registrations_table()

    def refresh_records_table(self):
        """Fetches all records from the database and repopulates the main records table.

        Shows a critical error message if the records cannot be loaded from the database.

        :return: None
        :rtype: None
        """
        # Fetches all records from the DB and populates the main table.
        try:
            self.records_table.setRowCount(0)
            current_row = 0
            for s in self.db_manager.get_all_students():
                self.records_table.insertRow(current_row); self.records_table.setItem(current_row,0,QTableWidgetItem(s[0])); self.records_table.setItem(current_row,1,QTableWidgetItem(s[1])); self.records_table.setItem(current_row,2,QTableWidgetItem("Student")); self.records_table.setItem(current_row,3,QTableWidgetItem(f"Age: {s[2]}, Email: {s[3]}")); current_row += 1
            for i in self.db_manager.get_all_instructors():
                self.records_table.insertRow(current_row); self.records_table.setItem(current_row,0,QTableWidgetItem(i[0])); self.records_table.setItem(current_row,1,QTableWidgetItem(i[1])); self.records_table.setItem(current_row,2,QTableWidgetItem("Instructor")); self.records_table.setItem(current_row,3,QTableWidgetItem(f"Age: {i[2]}, Email: {i[3]}")); current_row += 1
            for c in self.db_manager.get_all_courses():
                self.records_table.insertRow(current_row); self.records_table.setItem(current_row,0,QTableWidgetItem(c[0])); self.records_table.setItem(current_row,1,QTableWidgetItem(c[1])); self.records_table.setItem(current_row,2,QTableWidgetItem("Course")); self.records_table.setItem(current_row,3,QTableWidgetItem(f"Instructor ID: {c[2] if c[2] else 'N/A'}")); current_row += 1
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not load records: {e}")

    def update_registration_comboboxes(self):
        """Updates the registration dropdowns with the current list of students and courses.

        Shows a critical error message if the data cannot be loaded from the database.

        :return: None
        :rtype: None
        """
        # Populates dropdowns with current students and courses.
        try:
            self.reg_student_combo.clear()
            for s in self.db_manager.get_all_students(): self.reg_student_combo.addItem(f"{s[1]} ({s[0]})", s[0])
            self.reg_course_combo.clear()
            for c in self.db_manager.get_all_courses(): self.reg_course_combo.addItem(f"{c[1]} ({c[0]})", c[0])
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not load data for dropdowns: {e}")

    def refresh_registrations_table(self):
        """Fetches and displays all current student-course registrations in the "Registrations" tab.

        Shows a critical error message if the registration data cannot be loaded.

        :return: None
        :rtype: None
        """
        # Updates the table in the "Registrations" tab.
        try:
            self.registrations_table.setRowCount(0)
            for row_num, reg_data in enumerate(self.db_manager.get_registrations_for_display()):
                self.registrations_table.insertRow(row_num)
                for col_num, data in enumerate(reg_data): self.registrations_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not refresh registrations table: {e}")

    # --- Add/Register Methods ---
    def add_student(self):
        """Adds a new student to the database after validating the input fields.

        It provides appropriate error messages for validation errors (e.g., negative age)
        or database issues (e.g., duplicate student ID).

        :return: None
        :rtype: None
        """
        name, age, email, student_id = self.name_entry.text(), self.age_entry.text(), self.email_entry.text(), self.id_entry.text()
        if not all([name, age, email, student_id]): return QMessageBox.warning(self, "Input Error", "All fields are required.")
        try:
            student_obj = Student(name, int(age), email, student_id)
            self.db_manager.add_student(student_obj)
            QMessageBox.information(self, "Success", f"Student {name} added successfully!")
            self.refresh_all_data()
            self.name_entry.clear(); self.age_entry.clear(); self.email_entry.clear(); self.id_entry.clear()
        except ValueError as e: QMessageBox.warning(self, "Validation Error", str(e))
        except sqlite3.IntegrityError: QMessageBox.warning(self, "Database Error", f"A student with ID '{student_id}' already exists.")
        except Exception as e: QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def add_instructor(self):
        """Adds a new instructor to the database after validating the input fields.

        It provides appropriate error messages for validation errors or database issues
        like a duplicate instructor ID.

        :return: None
        :rtype: None
        """
        name, age, email, instructor_id = self.inst_name_entry.text(), self.inst_age_entry.text(), self.inst_email_entry.text(), self.inst_id_entry.text()
        if not all([name, age, email, instructor_id]): return QMessageBox.warning(self, "Input Error", "All fields are required.")
        try:
            inst_obj = Instructor(name, int(age), email, instructor_id)
            self.db_manager.add_instructor(inst_obj)
            QMessageBox.information(self, "Success", f"Instructor {name} added successfully!")
            self.refresh_all_data()
            self.inst_name_entry.clear(); self.inst_age_entry.clear(); self.inst_email_entry.clear(); self.inst_id_entry.clear()
        except ValueError as e: QMessageBox.warning(self, "Validation Error", str(e))
        except sqlite3.IntegrityError: QMessageBox.warning(self, "Database Error", f"An instructor with ID '{instructor_id}' already exists.")
        except Exception as e: QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def add_course(self):
        """Adds a new course to the database after validating the input fields.

        It provides an error message if the course ID already exists.

        :return: None
        :rtype: None
        """
        name, course_id = self.course_name_entry.text(), self.course_id_entry.text()
        if not all([name, course_id]): return QMessageBox.warning(self, "Input Error", "All fields are required.")
        try:
            course_obj = Course(course_id, name)
            self.db_manager.add_course(course_obj)
            QMessageBox.information(self, "Success", f"Course '{name}' added successfully!")
            self.refresh_all_data()
            self.course_name_entry.clear(); self.course_id_entry.clear()
        except sqlite3.IntegrityError: QMessageBox.warning(self, "Database Error", f"A course with ID '{course_id}' already exists.")
        except Exception as e: QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def register_student(self):
        """Registers a selected student for a selected course.

        It provides a warning if a student or course is not selected, or if the
        student is already registered for that course.

        :return: None
        :rtype: None
        """
        # .currentData() gets the ID I stored with the dropdown item, which is safer than parsing the string.
        student_id = self.reg_student_combo.currentData()
        course_id = self.reg_course_combo.currentData()
        if not student_id or not course_id: return QMessageBox.warning(self, "Selection Error", "Please select both a student and a course.")
        try:
            self.db_manager.register_student_in_course(student_id, course_id)
            QMessageBox.information(self, "Success", f"Student '{student_id}' registered for course '{course_id}'.")
            self.refresh_registrations_table()
        except sqlite3.IntegrityError: QMessageBox.warning(self, "Registration Error", "This student is already registered for this course.")
        except Exception as e: QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    # --- Edit/Delete Methods ---
    def edit_record(self):
        """Handles the 'Edit Selected' button click.

        It identifies which record is selected in the main table, determines its type
        (Student, Instructor, or Course), and opens the corresponding edit dialog.
        Upon successful dialog completion, it updates the database.

        :return: None
        :rtype: None
        """
        # This figures out which record is selected and opens the correct dialog.
        selected_row = self.records_table.currentRow()
        if selected_row < 0: return QMessageBox.warning(self, "Selection Error", "Please select a record to edit.")
        record_type = self.records_table.item(selected_row, 2).text()
        record_id = self.records_table.item(selected_row, 0).text()
        try:
            if record_type == "Student":
                data = self.db_manager.get_student_by_id(record_id)
                dialog = EditStudentDialog(data, self)
                if dialog.exec_() == QDialog.Accepted:
                    _, name, age, email = dialog.get_data()
                    obj = Student(name, int(age), email, record_id)
                    self.db_manager.update_student(obj)
            elif record_type == "Instructor":
                data = self.db_manager.get_instructor_by_id(record_id)
                dialog = EditInstructorDialog(data, self)
                if dialog.exec_() == QDialog.Accepted:
                    _, name, age, email = dialog.get_data()
                    obj = Instructor(name, int(age), email, record_id)
                    self.db_manager.update_instructor(obj)
            elif record_type == "Course":
                data = self.db_manager.get_course_by_id(record_id)
                dialog = EditCourseDialog(data, self)
                if dialog.exec_() == QDialog.Accepted:
                    _, name = dialog.get_data()
                    # Need to preserve the old instructor ID when updating.
                    obj = Course(record_id, name)
                    obj.instructor = data[2] # This is a raw ID, not an object.
                    # The update_course method in the DB manager is designed to handle this.
                    # We create a temporary object just for the update.
                    if data[2]:
                        obj.instructor = Instructor("dummy", 0, "dummy@email.com", data[2])
                    else:
                        obj.instructor = None
                    self.db_manager.update_course(obj)
            else: return
            QMessageBox.information(self, "Success", f"{record_type} record updated.")
            self.refresh_all_data()
        except ValueError as e: QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e: QMessageBox.critical(self, "Database Error", f"Could not update record: {e}")

    def delete_record(self):
        """Deletes a selected record from the database.

        This method first asks the user for confirmation. It handles the deletion for
        any record type (Student, Instructor, Course) and displays a user-friendly
        error if a record cannot be deleted due to being linked to other data (e.g.,
        deleting a student who is still registered for a course).

        :return: None
        :rtype: None
        """
        # This handles deleting any type of record.
        selected_row = self.records_table.currentRow()
        if selected_row < 0: return QMessageBox.warning(self, "Selection Error", "Please select a record to delete.")
        record_id = self.records_table.item(selected_row, 0).text()
        record_type = self.records_table.item(selected_row, 2).text()
        record_name = self.records_table.item(selected_row, 1).text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete the {record_type.lower()} '{record_name}' (ID: {record_id})?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if record_type == "Student": self.db_manager.delete_student(record_id)
                elif record_type == "Instructor": self.db_manager.delete_instructor(record_id)
                elif record_type == "Course": self.db_manager.delete_course(record_id)
                QMessageBox.information(self, "Success", f"{record_type} '{record_name}' deleted.")
                self.refresh_all_data()
            except sqlite3.IntegrityError as e:
                # User-friendly way to handle foreign key constraints.
                QMessageBox.warning(self, "Deletion Error", f"Could not delete {record_type.lower()} '{record_name}'.\nIt is likely still linked to other records.\n\nDetails: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not delete record: {e}")

    # --- Other Actions ---
    def export_to_csv(self):
        """Exports all student data from the database to a CSV file named 'students.csv'.

        It provides feedback to the user upon success or failure.

        :return: None
        :rtype: None
        """
        try:
            students = self.db_manager.get_all_students()
            if not students: return QMessageBox.information(self, "No Data", "There are no students to export.")
            with open('students.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['student_id', 'name', 'age', 'email']); writer.writerows(students)
            QMessageBox.information(self, "Success", "Student data has been exported to students.csv")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"An error occurred while exporting to CSV: {e}")

    def backup_database(self):
        """Creates a timestamped backup of the database file.

        This method calls the database manager's backup function and displays the
        path of the created backup file to the user, or an error if the backup failed.

        :return: None
        :rtype: None
        """
        try:
            backup_file = self.db_manager.backup_database()
            if backup_file:
                QMessageBox.information(self, "Backup Successful", f"Database backed up to:\n{backup_file}")
            else:
                QMessageBox.warning(self, "Backup Failed", "Could not create database backup.")
        except Exception as e:
                 QMessageBox.critical(self, "Backup Error", f"An error occurred during backup: {e}")

    def closeEvent(self, event):
        """Overrides the default close event to ensure the database connection is closed gracefully.

        :param event: The close event triggered by closing the window.
        :type event: QCloseEvent
        :return: None
        :rtype: None
        """
        # Special PyQt method, best place to close the DB connection.
        self.db_manager.close_connection()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SchoolManagementApp()
    ex.show()
    sys.exit(app.exec_())