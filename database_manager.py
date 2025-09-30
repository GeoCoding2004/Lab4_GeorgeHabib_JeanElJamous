import sqlite3
import shutil
import datetime

# Handles all the database stuff. Keeps the SQL separate from the GUI code.
class DatabaseManager:
    """Manages the database operations for the school system functionalities.

    :param db_name: The name of the database file
    :type db_name: str
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def setup_database(self):
        # Read the schema from the .sql file, way cleaner than a huge string here.
        """Sets up the database tables from an external schema file.

        Reads and executes the `database_schema.sql` file. This method
        handles exceptions by printing the corresponding message.

        :return: None
        :rtype: None
        """
        try:
            with open('database_schema.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            self.cursor.executescript(sql_script)
            self.conn.commit()
        except FileNotFoundError:
            print("Error: database_schema.sql not found.")
        except Exception as e:
            print(f"An error occurred during database setup: {e}")

    # --- Student Methods ---
    def add_student(self, student):
        """Function that adds a student to the database.

        :raises sqlite3.IntegrityError: if the student_id already exists in the database.
        :param student: The student to be added to the database
        :type student: Student
        :return: None
        :rtype: None
        """
        try:
            self.cursor.execute(
                "INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                (student.student_id, student.name, student.age, student._email)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def get_all_students(self):
        """Function to get all the students from the database.
        
        :return: A list of all students in the database
        :rtype: list of tuples
        """
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id):
        """Function to get a student that has an id equal to student_id from the database.

        :param student_id: The id of the student that we want to fetch from the database
        :type student_id: str
        :return: A tuple representing the student with the given id, or None if not found
        :rtype: tuple or None
        """
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student):
        """Function to update the information of a student in the database.

        :param student: The student object with updated information
        :type student: Student
        :return: None
        :rtype: None
        """
        self.cursor.execute(
            "UPDATE students SET name = ?, age = ?, email = ? WHERE student_id = ?",
            (student.name, student.age, student._email, student.student_id)
        )
        self.conn.commit()

    def delete_student(self, student_id):
        """Function to remove a student from the database based on the student_id.

        :param student_id: The id of the student to be deleted
        :type student_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.conn.commit()

    # --- Instructor Methods ---
    def add_instructor(self, instructor):
        """Function that adds an instructor to the database.

        :param instructor: The instructor to be added to the database
        :type instructor: Instructor
        :raises sqlite3.IntegrityError: if the instructor_id already exists in the database.
        :return: None
        :rtype: None
        """
        try:
            self.cursor.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                (instructor.instructor_id, instructor.name, instructor.age, instructor._email)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def get_all_instructors(self):
        """Function to get all the instructors from the database.
        
        :return: A list of all instructors in the database
        :rtype: list of tuples
        """
        self.cursor.execute("SELECT * FROM instructors")
        return self.cursor.fetchall()
        
    def get_instructor_by_id(self, instructor_id):
        """Function to get an instructor that has an id equal to instructor_id from the database.

        :param instructor_id: The id of the instructor that we want to fetch from the database
        :type instructor_id: str
        :return: A tuple representing the instructor with the given id, or None if not found
        :rtype: tuple or None
        """
        self.cursor.execute("SELECT * FROM instructors WHERE instructor_id = ?", (instructor_id,))
        return self.cursor.fetchone()

    def update_instructor(self, instructor):
        """Function to update the information of an instructor in the database.

        :param instructor: The instructor object with updated information
        :type instructor: Instructor
        :return: None
        :rtype: None
        """
        self.cursor.execute(
            "UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?",
            (instructor.name, instructor.age, instructor._email, instructor.instructor_id)
        )
        self.conn.commit()

    def delete_instructor(self, instructor_id):
        """Function to delete an instructor from the database based on the instructor_id.

        :param instructor_id: The id of the instructor to be deleted
        :type instructor_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,))
        self.conn.commit()

    # --- Course Methods ---
    def add_course(self, course):
        """Function that adds an course to the database.

        :raises sqlite3.IntegrityError: if the course_id already exists in the database.
        :param course: The course to be added to the database
        :type course: Course
        :return: None
        :rtype: None
        """
        try:
            # A course might not have an instructor assigned yet.
            instructor_id = course.instructor.instructor_id if course.instructor else None
            self.cursor.execute(
                "INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)",
                (course.course_id, course.course_name, instructor_id)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def get_all_courses(self):
        """Function to get all the courses from the database.

        :return: A list of all courses in the database
        :rtype: list of tuples
        """
        self.cursor.execute("SELECT * FROM courses")
        return self.cursor.fetchall()

    def get_course_by_id(self, course_id):
        """Function to get a course that has an id equal to course_id from the database.

        :param course_id: The id of the course that we want to fetch from the database
        :type course_id: str
        :return: A tuple representing the course with the given id, or None if not found
        :rtype: tuple or None
        """
        self.cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        return self.cursor.fetchone()

    def update_course(self, course):
        """Function to update the information of a course in the database.

        :param course: The course object with updated information
        :type course: Course
        :return: None
        :rtype: None
        """
        instructor_id = course.instructor.instructor_id if course.instructor else None
        self.cursor.execute(
            "UPDATE courses SET course_name = ?, instructor_id = ? WHERE course_id = ?",
            (course.course_name, instructor_id, course.course_id)
        )
        self.conn.commit()

    def delete_course(self, course_id):
        """Function to delete a course from the database based on the course_id.

        :param course_id: The id of the course to be deleted
        :type course_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
        self.conn.commit()

    # --- Registration Methods ---
    def register_student_in_course(self, student_id, course_id):
        """This function is to register a student in a course by adding an entry to the registrations join table.

        :raises sqlite3.IntegrityError: if the student is already registered in the course.
        :param student_id: The id of the student to be registered
        :type student_id: str
        :param course_id: The id of the course in which the student should be registered
        :type course_id: str
        :return: None
        :rtype: None
        """
        try:
            self.cursor.execute(
                "INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
                (student_id, course_id)
            )
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise e
            
    def get_registrations_for_display(self):
        """Function to get all registrations with student names and course names for display purposes.

        :return: A list of all registrations with student names and course names
        :rtype: list of tuples
        """
        query = """
            SELECT s.student_id, s.name, c.course_id, c.course_name
            FROM registrations r
            JOIN students s ON r.student_id = s.student_id
            JOIN courses c ON r.course_id = c.course_id
            ORDER BY s.name, c.course_name
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def backup_database(self):
        """Makes a timestamped backup of the db file.

        This method handles exceptions by printing to the console
        and returning None on failure.

        :return: The name of the backup file created, or None if backup failed
        :rtype: str or None
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.db_name}_backup_{timestamp}.db"
            shutil.copy2(self.db_name, backup_filename)
            print(f"Database backed up to {backup_filename}")
            return backup_filename
        except Exception as e:
            print(f"Database backup failed: {e}")
            return None

    def close_connection(self):
        """The function closes the connection when the app exits.

        :return: None
        :rtype: None
        """
        self.conn.close()

