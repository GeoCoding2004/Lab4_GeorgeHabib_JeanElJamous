-- This file defines the structure for my school database.
-- Using PRAGMA foreign_keys = ON is important for SQLite to enforce relationships.

PRAGMA foreign_keys = ON;

-- Table for students
CREATE TABLE IF NOT EXISTS students (
student_id TEXT PRIMARY KEY,
name TEXT NOT NULL,
age INTEGER,
email TEXT NOT NULL UNIQUE
);

-- Table for instructors
CREATE TABLE IF NOT EXISTS instructors (
instructor_id TEXT PRIMARY KEY,
name TEXT NOT NULL,
age INTEGER,
email TEXT NOT NULL UNIQUE
);

-- Table for courses
-- The instructor_id can be NULL if a course has no instructor assigned yet.
CREATE TABLE IF NOT EXISTS courses (
course_id TEXT PRIMARY KEY,
course_name TEXT NOT NULL,
instructor_id TEXT,
FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL
);

-- This is the join table to link students and courses.
-- It represents a many-to-many relationship.
-- ON DELETE CASCADE means if a student or course is deleted, the registration is also removed.
CREATE TABLE IF NOT EXISTS registrations (
registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id TEXT NOT NULL,
course_id TEXT NOT NULL,
FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
UNIQUE(student_id, course_id) -- Ensures a student can't register for the same course twice.
);