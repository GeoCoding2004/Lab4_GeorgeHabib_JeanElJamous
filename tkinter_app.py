import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from database_manager import DatabaseManager
from school_system_backend import Student, Instructor, Course

class SchoolManagementApp:
    """This class represents the main Tkinter application for managing the school system.
    It provides a GUI to add, edit, delete, and view students, instructors, and courses.
    It also allows registering students for courses.

    :param root: The root Tkinter window
    :type root: tk.Tk
    """
    def __init__(self, root):
        """Constructor method to set up the main application window and initialize the database manager."""
        self.root = root
        self.root.title("School Management System (Tkinter)")
        self.root.geometry("800x1024")

        # Set up the database connection.
        self.db_manager = DatabaseManager("school.db")
        self.db_manager.setup_database()

        # Moved widget creation to a separate function to keep __init__ clean.
        self.create_widgets()
        
        # Hook into the window close event to shut down the DB connection cleanly.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load all data from the DB into the UI on startup.
        self.refresh_all_data()

    def create_widgets(self):
        """ This function creates and arranges all the main widgets in the application.

        :return: None
        :rtype: None
        """
        forms_frame = tk.Frame(self.root)
        forms_frame.pack(padx=10, pady=10, fill="x")

        self.setup_data_entry_forms(forms_frame)
        self.setup_registration_form()
        self.setup_records_display()
        self.setup_action_buttons()
        
    def setup_data_entry_forms(self, parent_frame):
        """Sets up the forms for adding new students, instructors, and courses.

        :param parent_frame: The parent frame to contain the forms
        :type parent_frame: tk.Frame
        :return: None
        :rtype: None
        """

        # Student form
        student_form = ttk.LabelFrame(parent_frame, text="Add New Student", padding=(10, 5))
        student_form.pack(fill="x", expand=True, side="top", pady=(0, 10))
        self.name_entry = self.create_form_row(student_form, "Name:", 0)
        self.age_entry = self.create_form_row(student_form, "Age:", 1)
        self.email_entry = self.create_form_row(student_form, "Email:", 2)
        self.id_entry = self.create_form_row(student_form, "Student ID:", 3)
        ttk.Button(student_form, text="Add Student", command=self.add_student).grid(row=4, column=0, columnspan=2, pady=10)

        # Instructor form
        instructor_form = ttk.LabelFrame(parent_frame, text="Add New Instructor", padding=(10, 5))
        instructor_form.pack(fill="x", expand=True, side="top", pady=(0, 10))
        self.instructor_name_entry = self.create_form_row(instructor_form, "Name:", 0)
        self.instructor_age_entry = self.create_form_row(instructor_form, "Age:", 1)
        self.instructor_email_entry = self.create_form_row(instructor_form, "Email:", 2)
        self.instructor_id_entry = self.create_form_row(instructor_form, "Instructor ID:", 3)
        ttk.Button(instructor_form, text="Add Instructor", command=self.add_instructor).grid(row=4, column=0, columnspan=2, pady=10)

        # Course form
        course_form = ttk.LabelFrame(parent_frame, text="Add New Course", padding=(10, 5))
        course_form.pack(fill="x", expand=True, side="top")
        self.course_id_entry = self.create_form_row(course_form, "Course ID:", 0)
        self.course_name_entry = self.create_form_row(course_form, "Course Name:", 1)
        ttk.Button(course_form, text="Add Course", command=self.add_course).grid(row=2, column=0, columnspan=2, pady=10)

    def create_form_row(self, parent, label_text, row):
        """Helper function to create a labeled entry row in a form.

        :param parent: The parent frame to contain the row
        :type parent: tk.Frame
        :param label_text: The text for the label
        :type label_text: str
        :param row: The row number in the grid
        :type row: int
        :return: The created entry widget
        :rtype: ttk.Entry
        """
        # Helper to avoid repeating label/entry code.
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky="ew", pady=2, padx=5)
        parent.columnconfigure(1, weight=1)
        return entry
        
    def setup_registration_form(self):
        """Sets up the form for Registering a student for a course.

        :return: None
        :rtype: None
        """
        # The section for registering students to courses.
        reg_frame = ttk.LabelFrame(self.root, text="Manage Registrations", padding=(10, 5))
        reg_frame.pack(padx=10, pady=10, fill="x")
        self.reg_student_combobox = self.create_form_row(reg_frame, "Select Student:", 0)
        self.reg_student_combobox.config(state="readonly")
        self.reg_course_combobox = self.create_form_row(reg_frame, "Select Course:", 1)
        self.reg_course_combobox.config(state="readonly")
        ttk.Button(reg_frame, text="Register Student to Course", command=self.register_student_for_course).grid(row=2, column=0, columnspan=2, pady=10)
        
    def setup_records_display(self):
        """Sets up the display area for showing all records in a Treeview format with a scrollbar.

        :return: None
        :rtype: None
        """
        # The main table (Treeview) that shows all data.
        display_frame = ttk.LabelFrame(self.root, text="Records", padding=(10, 5))
        display_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.tree = ttk.Treeview(display_frame, columns=("ID", "Name", "Type", "Details"), show="headings")
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=100)
        self.tree.heading("Name", text="Name"); self.tree.column("Name", width=150)
        self.tree.heading("Type", text="Type"); self.tree.column("Type", width=80, anchor="center")
        self.tree.heading("Details", text="Details"); self.tree.column("Details", width=300)
        
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_action_buttons(self):
        """This function sets up the edit and delete buttons.

        :return: None
        :rtype: None
        """
        action_frame = ttk.Frame(self.root)
        action_frame.pack(padx=10, pady=(0, 10), fill="x")
        ttk.Button(action_frame, text="Edit Selected", command=self.edit_record).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self.delete_record).pack(side="left", padx=5)
        
    def on_closing(self):
        """This function makes sure that the database connection is closed properly.

        :return: None
        :rtype: None
        """
        self.db_manager.close_connection()
        self.root.destroy()
        
    def refresh_all_data(self):
        """This function makes sure that all the UI bits are updated after a data change.
        :return: None
        :rtype: None
        """
        self.refresh_records_display()
        self.update_comboboxes()

    def refresh_records_display(self):
        """This function fetches all the data from the database and redraws the main table.

        Shows an error message if the records cannot be loaded.

        :return: None
        :rtype: None
        """
        # Fetches all data from the database and redraws the main table.
        try:
            for item in self.tree.get_children(): self.tree.delete(item)
            for s in self.db_manager.get_all_students(): self.tree.insert("", "end", values=(s[0], s[1], "Student", f"Age: {s[2]}, Email: {s[3]}"))
            for i in self.db_manager.get_all_instructors(): self.tree.insert("", "end", values=(i[0], i[1], "Instructor", f"Age: {i[2]}, Email: {i[3]}"))
            for c in self.db_manager.get_all_courses(): self.tree.insert("", "end", values=(c[0], c[1], "Course", f"Instructor ID: {c[2] or 'N/A'}"))
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load records: {e}")

    def update_comboboxes(self):
        """ This function makes sure that the registration drowpdowns are updated with the current students and courses.
        It handles errors by showing a message box within the dialog.

        :return: None
        :rtype: None
        """
        # Updates the registration dropdowns with current students and courses.
        try:
            students = self.db_manager.get_all_students()
            self.reg_student_combobox['values'] = [f"{s[1]} ({s[0]})" for s in students]
            courses = self.db_manager.get_all_courses()
            self.reg_course_combobox['values'] = [f"{c[1]} ({c[0]})" for c in courses]
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load data for dropdowns: {e}")

    def add_student(self):
        """This function adds a new student to the database after validating the input fields.
        It provides appropriate error messages for validation errors or database issues.

        :return: None
        :rtype: None
        """
        name, age, email, student_id = self.name_entry.get(), self.age_entry.get(), self.email_entry.get(), self.id_entry.get()
        if not all([name, age, email, student_id]): return messagebox.showerror("Input Error", "All fields are required.")
        try:
            # First create the object to run backend validation, then add to DB.
            self.db_manager.add_student(Student(name, int(age), email, student_id))
            messagebox.showinfo("Success", f"Student {name} added.")
            self.refresh_all_data()
            for entry in [self.name_entry, self.age_entry, self.email_entry, self.id_entry]: entry.delete(0, "end")
        except ValueError as e: messagebox.showerror("Validation Error", str(e))
        except sqlite3.IntegrityError: messagebox.showerror("Database Error", f"Student ID '{student_id}' already exists.")
        except Exception as e: messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def add_instructor(self):
        """This function adds a new instructor to the database after validating the input fields.
        It provides appropriate error messages for validation errors or database issues.

        :return: None
        :rtype: None
        """
        name, age, email, inst_id = self.instructor_name_entry.get(), self.instructor_age_entry.get(), self.instructor_email_entry.get(), self.instructor_id_entry.get()
        if not all([name, age, email, inst_id]): return messagebox.showerror("Input Error", "All fields are required.")
        try:
            self.db_manager.add_instructor(Instructor(name, int(age), email, inst_id))
            messagebox.showinfo("Success", f"Instructor {name} added.")
            self.refresh_all_data()
            for entry in [self.instructor_name_entry, self.instructor_age_entry, self.instructor_email_entry, self.instructor_id_entry]: entry.delete(0, "end")
        except ValueError as e: messagebox.showerror("Validation Error", str(e))
        except sqlite3.IntegrityError: messagebox.showerror("Database Error", f"Instructor ID '{inst_id}' already exists.")
        except Exception as e: messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def add_course(self):
        """This function adds a new course to the database after validating the input fields.
        It provides appropriate error messages for validation errors or database issues.

        :return: None
        :rtype: None
        """
        course_id, name = self.course_id_entry.get(), self.course_name_entry.get()
        if not all([course_id, name]): return messagebox.showerror("Input Error", "All fields are required.")
        try:
            self.db_manager.add_course(Course(course_id, name))
            messagebox.showinfo("Success", f"Course '{name}' added.")
            self.refresh_all_data()
            self.course_id_entry.delete(0, "end"); self.course_name_entry.delete(0, "end")
        except sqlite3.IntegrityError: messagebox.showerror("Database Error", f"Course ID '{course_id}' already exists.")
        except Exception as e: messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def register_student_for_course(self):
        """This function registers a selected student for a selected course.

        It provides a warning message if a student or an instructor are not selected. It also provides a warnign message if the student is already registered in the course.
        
        This function throws an exception error when an unexpected error in the registration has occured.

        :return: None
        :rtype: None
        """
        student_sel = self.reg_student_combobox.get()
        course_sel = self.reg_course_combobox.get()
        if not student_sel or not course_sel: return messagebox.showwarning("Selection Error", "Please select both a student and a course.")
        try:
            # The dropdown shows "Name (ID)", so have to parse the ID out of the string.
            student_id = student_sel.split('(')[-1].strip(')')
            course_id = course_sel.split('(')[-1].strip(')')
            self.db_manager.register_student_in_course(student_id, course_id)
            messagebox.showinfo("Success", f"Registered Student '{student_id}' for Course '{course_id}'.")
            self.refresh_all_data()
            self.reg_student_combobox.set(''); self.reg_course_combobox.set('')
        except sqlite3.IntegrityError: messagebox.showwarning("Registration Error", "This student is already registered for this course.")
        except Exception as e: messagebox.showerror("Error", f"An unexpected registration error occurred: {e}")

    def delete_record(self):
        """This function deletes a selected record from the database. The record could be a student, course, or an instructor.

        Confirms the process of deleting a record with the user and handles errors for records that are still linked to other data.

        :return: None
        :rtype: None
        
        """
        selected_item = self.tree.focus()
        if not selected_item: return messagebox.showwarning("Selection Error", "Please select a record to delete.")
        
        values = self.tree.item(selected_item, "values")
        record_id, record_name, record_type = values[0], values[1], values[2]
        
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the {record_type.lower()} '{record_name}'?"): return
        
        try:
            # Check the type and call the correct DB manager method.
            if record_type == "Student": self.db_manager.delete_student(record_id)
            elif record_type == "Instructor": self.db_manager.delete_instructor(record_id)
            elif record_type == "Course": self.db_manager.delete_course(record_id)
            messagebox.showinfo("Success", f"{record_type} '{record_name}' was deleted.")
            self.refresh_all_data()
        except sqlite3.IntegrityError:
            # Catch foreign key errors, e.g., can't delete a student who is registered for a course.
            messagebox.showerror("Deletion Error", f"Cannot delete {record_name}. It is likely still linked to other records.")
        except Exception as e: messagebox.showerror("Error", f"An error occurred during deletion: {e}")

    def edit_record(self):
        """This handles the edit button for editing the records.

        If no item was selected, a warning message is showing indicating for th euser to select a record for editing.

        For each record, gets the data from the database, then updates the data with the new data

        :return: None
        :rtype: None
        """
        selected_item = self.tree.focus()
        if not selected_item: return messagebox.showwarning("Selection Error", "Please select a record to edit.")
        
        values = self.tree.item(selected_item, "values")
        record_id, _, record_type = values[0], values[1], values[2]

        if record_type == "Student":
            data = self.db_manager.get_student_by_id(record_id)
            self.create_edit_dialog("Edit Student", data, ["Name", "Age", "Email"], self.save_student_edit)
        elif record_type == "Instructor":
            data = self.db_manager.get_instructor_by_id(record_id)
            self.create_edit_dialog("Edit Instructor", data, ["Name", "Age", "Email"], self.save_instructor_edit)
        elif record_type == "Course":
            data = self.db_manager.get_course_by_id(record_id)
            self.create_edit_dialog("Edit Course", data, ["Course Name"], self.save_course_edit)

    def create_edit_dialog(self, title, data, field_labels, save_callback):
        """ This function creates the pop-up dialog for editing.

        :param title: The title of the dialog window
        :type title: str
        :param data: The existing data to pre-fill the form
        :type data: tuple
        :param field_labels: The labels for the fields to edit
        :type field_labels: list
        :param save_callback: The function to call to save the edited data
        :type save_callback: function
        :return: None
        :rtype: None 
        """
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        
        record_id = data[0]
        entries = []
        for i, label in enumerate(field_labels):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(dialog, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            # Pre-fill the entry with existing data.
            entry.insert(0, data[i+1])
            entries.append(entry)
        
        # The lambda is important here to pass arguments to the save callback.
        save_btn = ttk.Button(dialog, text="Save", command=lambda: save_callback(record_id, entries, dialog))
        save_btn.grid(row=len(field_labels), column=0, columnspan=2, pady=10)

    def save_student_edit(self, student_id, entries, dialog):
        """This function is for saving a student after editing to the database.
        It handles errors by showing a message box within the dialog.

        :param student_id: The ID of the student being edited
        :type student_id: str
        :param entries: The list of entry widgets containing the edited data
        :type entries: list
        :param dialog: The dialog window to close after saving
        :type dialog: tk.Toplevel

        :return: None
        :rtype: None
        """
        # Callback for saving a student.
        name, age, email = entries[0].get(), entries[1].get(), entries[2].get()
        try:
            student = Student(name, int(age), email, student_id)
            self.db_manager.update_student(student)
            dialog.destroy() # Close the pop-up.
            self.refresh_all_data()
        except Exception as e: messagebox.showerror("Save Error", str(e), parent=dialog)

    def save_instructor_edit(self, inst_id, entries, dialog):
        """This function is for saving an instructor after editing to the database
        It handles errors by showing a message box within the dialog.

        :param inst_id: The ID of the instructor being edited
        :type inst_id: str
        :param entries: The list of entry widgets containing the edited data
        :type entries: list
        :param dialog: The dialog window to close after saving
        :type dialog: tk.Toplevel
        :return: None
        :rtype: None
        """
        # Callback for saving an instructor.
        name, age, email = entries[0].get(), entries[1].get(), entries[2].get()
        try:
            instructor = Instructor(name, int(age), email, inst_id)
            self.db_manager.update_instructor(instructor)
            dialog.destroy()
            self.refresh_all_data()
        except Exception as e: messagebox.showerror("Save Error", str(e), parent=dialog)
        
    def save_course_edit(self, course_id, entries, dialog):
        """This function is for saving a course after editing to the database
        It handles errors by showing a message box within the dialog.

        :param course_id: The ID of the course being edited
        :type course_id: str
        :param entries: The list of entry widgets containing the edited data
        :type entries: list
        :param dialog: The dialog window to close after saving
        :type dialog: tk.Toplevel
        :return: None
        :rtype: None
        """
        # Callback for saving a course.
        name = entries[0].get()
        try:
            # Only editing the name, so need to preserve the existing instructor ID.
            course_data = self.db_manager.get_course_by_id(course_id)
            course = Course(course_id, name)
            # This feels a bit hacky, but I need to create a dummy instructor object
            # to satisfy the backend class structure for the update method.
            if course_data[2]:
                course.instructor = Instructor("dummy", 0, "dummy@email.com", course_data[2])
            
            self.db_manager.update_course(course)
            dialog.destroy()
            self.refresh_all_data()
        except Exception as e: messagebox.showerror("Save Error", str(e), parent=dialog)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()

