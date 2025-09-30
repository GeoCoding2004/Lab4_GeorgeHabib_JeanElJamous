class Person:
    """ This class describes a person in the school system. The person could be a Student or an Instructor.

    :param name: The name of the person
    :type name: str
    :param age: The age of the person
    :type age: int
    :param email: The email address of the person
    :type email: str
    :raises ValueError: If email is not valid or age is negative
    """
    def __init__(self, name: str, age: int, email: str):
        """Constructor method"""
        self.name = name
        self.age = age
        self._email = email

        # Validation right in the constructor. Fail early if the data is bad.
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer.")
        if '@' not in self._email or '.' not in self._email:
            raise ValueError("Email address is not valid.")

    def introduce(self):
        """Prints an introduction message of the Person, including his name and age.

        :return: None
        :rtype: None
        """
        print(f"Hi, my name is {self.name} and I am {self.age} years old.")

class Student(Person):
    """This class describes a student in the school system. It inherits from the class :class:`Person` the attributes
    of a generic person (age, name, email). It adds the student_id attribute which is unique for each student. It has also a list
    of registered_courses which represent the list of courses that the student is registerd in.

    :param name: The name of the student
    :type name: str
    :param age: The age of the student
    :type age: int
    :param email: The email address of the student
    :type email: str
    :param student_id: The id of the student
    :type student_id: str
    """

    def __init__(self, name: str, age: int, email: str, student_id: str):
        """Constructor method. Registered courses list is initialized as an empty list."""
        super().__init__(name, age, email)
        self.student_id = student_id
        # Will be a list of Course objects.
        self.registered_courses = []

    def register_course(self, course):
        """Function that registers a student in a course.
        It checks if the student is already registered in the course. If yes, then a message saying that the student is already registered is shown
        If the student is not registered, it registers him by appending the course to the registered_courses list of the student, then showing a message that says that the student has registered.
        
        :param course: The course that the student wants to register
        :type course: Course
        :return: None
        :rtype: None
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            print(f"Student {self.name} has registered for {course.course_name}.")
        else:
            print(f"Student {self.name} is already registered for {course.course_name}.")
            
    def to_dict(self):
        """Converts the data of the student to a dictionary.

         :return: The student's information in a dictionary
         :rtype: dict
         """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        }

    @classmethod
    def from_dict(cls, data):
        """Converts the dictionary data to a :class:`Student` object

        :param data: The dictionary that contains the information about the student
        :type data: dict
        :return: A "Student" object created from the dictionary data
        :rtype: Student
        """
        return cls(data['name'], data['age'], data['email'], data['student_id'])


class Instructor(Person):
    """This class describes an instructor. It inherits from the class :class:`Person` the attributes name, age, email.
    It adds the instructor_id attribute which is unique for every instructor.
    It has also a list of assigned_courses which represents the courses that the instructor was assigned to.

    :param name: The name of the instructor
    :type name: str
    :param age: The age of the instructor
    :type age: int
    :param email: The email of the instrucotr
    :type email: str
    :param instructor_id: The id that is unique for each instructor
    :type instructor_id: str
    """

    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        """Constructor method. Assgined_courses list is initialized to an empty list"""
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """Function that assigns a course to an instructor
        It checks if the instructor is already assigned to this course, it provide a message saying that the instructor is already assigned to this course
        If the instructor is not assigned to the course, then it assigns the instructor to the course by appending the course to the list of assigned_courses, then provide a message saying that the instructor was assigned to the course
        
        :param course: The course to be assigned to the instructor
        :type course: Course
        :return: None
        :rtype: None 
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"Instructor {self.name} has been assigned to {course.course_name}.")
        else:
            print(f"Instructor {self.name} is already assigned to {course.course_name}.")
            
    def to_dict(self):
        """Converts the data of the instructor to a dictionary.

        :return: The instructor's information in a dictionary
        :rtype: dict
        """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        }
        
    @classmethod
    def from_dict(cls, data):
        """Converts the dictionary data to a :class:`Instructor` object

        :param data: The dictionary that contains the information about the instructor
        :type data: dict
        :return: An "Instructor" object created from the dictionary data
        :rtype: Instructor
        """
        return cls(data['name'], data['age'], data['email'], data['instructor_id'])


class Course:
    """This class describes a course which can be assigned to instructors or enrolled in by students. The course has a course_id which provides a unique id for each course.
    It also has a course_name which represents the name of the course. It has an instructor which is the instructor assigned to the course
    It also has a list of enrolled_students representing the students enrolled in the course

    :param course_id: The id of the course
    :type course_id: str
    :param course_name: The name of the course
    :type course_name: str
    :param instructor: The instructor assigned to the course
    :type instructor: Instructor
    """

    def __init__(self, course_id: str, course_name: str, instructor: Instructor = None):
        """Constructor method. Enrolled_students list is initialized to an empty list."""
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student: Student):
        """Function that adds a student to a course.
        It checks if the student is already in the enrolled_students list. If yes, then a message saying that the student is already enrolled in the course is shown.
        If the student is not in the enrolled_students list (so not enrolled), it registers him by appending the student to the enrolled_students list, then showing a message that says that the student enrolled.
        
        :param student: The student that should be enrolled in the course
        :type student: Student
        :return: None
        :rtype: None
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"Student {student.name} has been enrolled in {self.course_name}.")
        else:
            print(f"Student {student.name} is already enrolled in {self.course_name}.")
            
    def to_dict(self):
        """Converts the data of the course to a dictionary.

        :return: The course's information in a dictionary
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }

    @classmethod
    def from_dict(cls, data, instructors):
        """Converts the dictionary data to a :class:`Course` object

        :param data: The dictionary that contains the information about the course
        :type data: dict
        :param instructors: The list of instructors to find the instructor by id
        :type instructors: list of Instructor
        :return: A "Course" object created from the dictionary data
        :rtype: Course
        """
        instructor = next((inst for inst in instructors if inst.instructor_id == data['instructor_id']), None)
        return cls(data['course_id'], data['course_name'], instructor)

