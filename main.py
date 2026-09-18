import json
import math
import statistics
import os
from datetime import datetime


# ============================================================
# STUDENT PERFORMANCE MANAGEMENT SYSTEM
# ============================================================
# This project is intentionally designed for testing the
# Autonomous CI/CD Healing Agent.
#
# Supported operations:
#   1. Student registration
#   2. Marks calculation
#   3. Grade calculation
#   4. Attendance calculation
#   5. Performance analysis
#   6. Report generation
#   7. Scholarship calculation
#   8. JSON export
# ============================================================


PROJECT_NAME = "Student Performance Management System"
PROJECT_VERSION = "2.0"


# ============================================================
# STUDENT CLASS
# ============================================================

class Student:

    def __init__(self, student_id, name, age, department, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks
        self.created_at = datetime.now()

    def calculate_total(self):
        total = sum(self.marks)
        return total

    def calculate_average(self):
        total = self.calculate_total()

        if len(self.marks) == 0:
            return 0

        average = total / len(self.marks)

        return average

    def calculate_percentage(self):
        total = self.calculate_total()
        maximum_marks = len(self.marks) * 100

        if maximum_marks == 0:
            return 0

        return (total / maximum_marks) * 100

    def calculate_grade(self):

        percentage = self.calculate_percentage()

        if percentage >= 90:
            return "A+"

        elif percentage >= 80:
            return "A"

        elif percentage >= 70:
            return "B"

        elif percentage >= 60:
            return "C"

        elif percentage >= 50:
            return "D"

        else:
            return "F"

    def get_result(self):

        percentage = self.calculate_percentage()

        if percentage >= 40:
            return "PASS"

        return "FAIL"

    def get_summary(self):

        return {
            "id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "total": self.calculate_total(),
            "average": self.calculate_average(),
            "percentage": self.calculate_percentage(),
            "grade": self.calculate_grade(),
            "result": self.get_result()
        }


# ============================================================
# STUDENT DATABASE
# ============================================================

class StudentDatabase:

    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def find_student(self, student_id):

        for student in self.students:

            if student.student_id == student_id:
                return student

        return None

    def find_by_name(self, name):

        for student in self.students:

            if student.name.lower() == name.lower():
                return student

        return None

    def remove_student(self, student_id):

        student = self.find_student(student_id)

        if student is None:
            return False

        self.students.remove(student)

        return True

    def get_students(self):
        return self.students

    def count(self):
        return len(self.students)


# ============================================================
# ATTENDANCE MANAGEMENT
# ============================================================

class AttendanceManager:

    def __init__(self):
        self.attendance = {}

    def add_attendance(self, student_id, present, total):

        self.attendance[student_id] = {
            "present": present,
            "total": total
        }

    def calculate_percentage(self, student_id):

        record = self.attendance.get(student_id)

        if record is None:
            return 0

        if record["total"] == 0:
            return 0

        return (
            record["present"] /
            record["total"]
        ) * 100

    def is_eligible(self, student_id):

        percentage = self.calculate_percentage(student_id)

        return percentage >= 75


# ============================================================
# PERFORMANCE ANALYZER
# ============================================================

class PerformanceAnalyzer:

    def __init__(self, database):
        self.database = database

    def class_average(self):

        students = self.database.get_students()

        if not students:
            return 0

        averages = []

        for student in students:
            averages.append(
                student.calculate_percentage()
            )

        return sum(averages) / len(averages)

    def highest_performer(self):

        students = self.database.get_students()

        if not students:
            return None

        highest = students[0]

        for student in students:

            if (
                student.calculate_percentage()
                > highest.calculate_percentage()
            ):
                highest = student

        return highest

    def lowest_performer(self):

        students = self.database.get_students()

        if not students:
            return None

        lowest = students[0]

        for student in students:

            if (
                student.calculate_percentage()
                < lowest.calculate_percentage()
            ):
                lowest = student

        return lowest

    def calculate_statistics(self):

        students = self.database.get_students()

        percentages = []

        for student in students:

            percentages.append(
                student.calculate_percentage()
            )

        if not percentages:
            return {}

        return {
            "mean": statistics.mean(percentages),
            "median": statistics.median(percentages),
            "maximum": max(percentages),
            "minimum": min(percentages)
        }


# ============================================================
# SCHOLARSHIP MANAGER
# ============================================================

class ScholarshipManager:

    def calculate_scholarship(self, student):

        percentage = student.calculate_percentage()

        if percentage >= 90:
            return 50000

        elif percentage >= 80:
            return 30000

        elif percentage >= 70:
            return 15000

        return 0

    def check_eligibility(self, student):

        amount = self.calculate_scholarship(student)

        if amount > 0:
            return True

        return False


# ============================================================
# REPORT MANAGER
# ============================================================

class ReportManager:

    def __init__(self, database, attendance_manager):

        self.database = database
        self.attendance_manager = attendance_manager

    def generate_report(self):

        report = []

        for student in self.database.get_students():

            attendance = (
                self.attendance_manager
                .calculate_percentage(
                    student.student_id
                )
            )

            student_report = student.get_summary()

            student_report["attendance"] = attendance

            report.append(student_report)

        return report

    def display_report(self):

        report = self.generate_report()

        print()
        print("=" * 70)
        print("STUDENT PERFORMANCE REPORT")
        print("=" * 70)

        for student in report:

            print("Student ID :", student["id"])
            print("Name       :", student["name"])
            print("Department :", student["department"])
            print("Total      :", student["total"])
            print("Average    :", round(student["average"], 2))
            print("Percentage :", round(student["percentage"], 2))
            print("Attendance :", round(student["attendance"], 2))
            print("Grade      :", student["grade"])
            print("Result     :", student["result"])

            print("-" * 70)


# ============================================================
# FILE MANAGER
# ============================================================

class FileManager:

    def save_json(self, filename, data):

        with open(filename, "w") as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print("Report saved:", filename)

    def load_json(self, filename):

        with open(filename, "r") as file:

            return json.load(file)


# ============================================================
# SAMPLE DATA
# ============================================================

def create_students(database):

    student1 = Student(
        101,
        "Rahul",
        21,
        "Computer Science",
        [88, 91, 76, 95, 89]
    )

    student2 = Student(
        102,
        "Priya",
        20,
        "Computer Science",
        [92, 85, 90, 94, 88]
    )

    student3 = Student(
        103,
        "Arun",
        22,
        "Information Science",
        [65, 70, 68, 72, 75]
    )

    student4 = Student(
        104,
        "Sneha",
        21,
        "Computer Science",
        [95, 97, 91, 94, 98]
    )

    student5 = Student(
        105,
        "Kiran",
        20,
        "Electronics",
        [55, 61, 48, 64, 58]
    )

    database.add_student(student1)
    database.add_student(student2)
    database.add_student(student3)
    database.add_student(student4)
    database.add_student(student5)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def calculate_class_percentage(database):

    students = database.get_students()

    total = 0

    for student in students:

        total += student.calculate_percentage()

    if len(students) == 0:
        return 0

    return total / len(students)


def print_top_student(analyzer):

    student = analyzer.highest_performer()

    if student is None:
        print("No students available.")
        return

    print()
    print("=" * 70)
    print("TOP PERFORMER")
    print("=" * 70)

    print("Name       :", student.name)
    print("Percentage :", student.calculate_percentage())
    print("Grade      :", student.calculate_grade())


def print_lowest_student(analyzer):

    student = analyzer.lowest_performer()

    if student is None:
        print("No students available.")
        return

    print()
    print("=" * 70)
    print("LOWEST PERFORMER")
    print("=" * 70)

    print("Name       :", student.name)
    print("Percentage :", student.calculate_percentage())
    print("Grade      :", student.calculate_grade())


def display_statistics(analyzer):

    statistics_data = analyzer.calculate_statistics()

    print()
    print("=" * 70)
    print("CLASS STATISTICS")
    print("=" * 70)

    print("Mean    :", statistics_data["mean"])
    print("Median  :", statistics_data["median"])
    print("Maximum :", statistics_data["maximum"])
    print("Minimum :", statistics_data["minimum"])


def print_scholarship_details(database):

    manager = ScholarshipManager()

    print()
    print("=" * 70)
    print("SCHOLARSHIP DETAILS")
    print("=" * 70)

    for student in database.get_students():

        amount = manager.calculate_scholarship(student)

        print(
            student.name,
            "=> Scholarship:",
            amount
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("=" * 70)
    print(PROJECT_NAME)
    print("Version:", PROJECT_VERSION)
    print("=" * 70)

    database = StudentDatabase()

    attendance_manager = AttendanceManager()

    analyzer = PerformanceAnalyzer(database)

    report_manager = ReportManager(
        database,
        attendance_manager
    )

    file_manager = FileManager()

    create_students(database)

    print()
    print("Students registered:", database.count())

    # --------------------------------------------------------
    # Attendance records
    # --------------------------------------------------------

    attendance_manager.add_attendance(
        101, 85, 100
    )

    attendance_manager.add_attendance(
        102, 92, 100
    )

    attendance_manager.add_attendance(
        103, 68, 100
    )

    attendance_manager.add_attendance(
        104, 96, 100
    )

    attendance_manager.add_attendance(
        105, 74, 100
    )

    # --------------------------------------------------------
    # Display main report
    # --------------------------------------------------------

    report_manager.display_report()

    # --------------------------------------------------------
    # Performance information
    # --------------------------------------------------------

    print_top_student(analyzer)

    print_lowest_student(analyzer)

    display_statistics(analyzer)

    # --------------------------------------------------------
    # Class percentage
    # --------------------------------------------------------

    class_percentage = calculate_class_percentage(
        database
    )

    print()
    print("Overall Class Percentage:",
          round(class_percentage, 2))

    # --------------------------------------------------------
    # Scholarship
    # --------------------------------------------------------

    print_scholarship_details(database)

    # --------------------------------------------------------
    # Save report
    # --------------------------------------------------------

    report = report_manager.generate_report()

    file_manager.save_json(
        "student_report.json",
        report
    )

    print()
    print("=" * 70)
    print("BASIC PROCESSING COMPLETED")
    print("=" * 70)


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":
    main()


# ============================================================
# ADVANCED PROCESSING SECTION
# ============================================================
# The following section is intentionally problematic.
# It executes after the main application and is designed to
# test the autonomous healing process.
# ============================================================


def calculate_bonus(student):

    percentage = student.calculate_percentage()

    if percentage >= 90:
        bonus = 5000

    elif percentage >= 80:
        bonus = 3000

    elif percentage >= 70:
        bonus = 2000

    else:
        bonus = 1000

    return bonus


def create_final_summary(database):

    summary = []

    for student in database.get_students():

        bonus = calculate_bonus(student)

        record = {
            "name": student.name,
            "percentage": student.calculate_percentage(),
            "grade": student.calculate_grade(),
            "bonus": bonus
        }

        summary.append(record)

    return summary


def calculate_bonus_percentage(student):

    bonus = calculate_bonus(student)

    percentage = student.calculate_percentage()

    if percentage == 0:
        return 0

    return (bonus / percentage) * 100


def print_final_summary(database):

    summary = create_final_summary(database)

    print()
    print("=" * 70)
    print("FINAL PERFORMANCE SUMMARY")
    print("=" * 70)

    for record in summary:

        print(
            "Student:",
            record["name"]
        )

        print(
            "Percentage:",
            round(record["percentage"], 2)
        )

        print(
            "Grade:",
            record["grade"]
        )

        print(
            "Bonus:",
            record["bonus"]
        )

        print("-" * 70)


def advanced_analysis(database):

    print()
    print("=" * 70)
    print("ADVANCED ANALYSIS")
    print("=" * 70)

    students = database.get_students()

    for student in students:

        percentage = student.calculate_percentage()

        if percentage > 85:

            print(
                student.name,
                "is an excellent performer."
            )

        elif percentage > 70:

            print(
                student.name,
                "is a good performer."
            )

        else:

            print(
                student.name,
                "needs improvement."
            )


def export_final_data(database):

    data = create_final_summary(database)

    filename = "final_student_data.json"

    with open(filename, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(
        "Final data exported successfully."
    )


# ============================================================
# INTENTIONALLY BROKEN EXECUTION SECTION
# ============================================================

print()
print("=" * 70)
print("STARTING ADVANCED HEALING TEST")
print("=" * 70)


# ERROR 1:
# Missing colon after elif
# This creates a SyntaxError and prevents the program from
# executing until Gemini repairs it.

def test_syntax_error(student):

    percentage = student.calculate_percentage()

    if percentage >= 90:
        return "Excellent"

    elif percentage >= 80
        return "Very Good"

    else:
        return "Needs Improvement"


# ------------------------------------------------------------
# The following functions contain additional errors.
# They become reachable after the first error is repaired.
# ------------------------------------------------------------


def test_name_error(student):

    percentage = student.calculate_percentage()

    # Intentional NameError
    result = percentage + undefined_bonus

    return result


def test_type_error(student):

    percentage = student.calculate_percentage()

    # Intentional TypeError
    result = percentage + " percentage"

    return result


def test_key_error(student):

    data = {
        "name": student.name,
        "department": student.department,
        "percentage": student.calculate_percentage()
    }

    # Intentional KeyError
    return data["student_email"]


def test_zero_division():

    total_students = 0

    total_marks = 500

    # Intentional ZeroDivisionError
    average = total_marks / total_students

    return average


def test_attribute_error(student):

    # Intentional AttributeError
    return student.get_full_name()


def test_file_error():

    # Intentional FileNotFoundError
    with open(
        "important_missing_configuration.json",
        "r"
    ) as file:

        return json.load(file)


# ============================================================
# FINAL TEST RUNNER
# ============================================================

def run_healing_test(database):

    students = database.get_students()

    first_student = students[0]

    print()
    print("Running autonomous healing test...")
    print()

    # First error after syntax repair
    print("Test 1: Name Error")

    value = test_name_error(
        first_student
    )

    print("Name error test result:", value)

    # Second error
    print("Test 2: Type Error")

    value = test_type_error(
        first_student
    )

    print("Type error test result:", value)

    # Third error
    print("Test 3: Key Error")

    value = test_key_error(
        first_student
    )

    print("Key error test result:", value)

    # Fourth error
    print("Test 4: Zero Division")

    value = test_zero_division()

    print("Division test result:", value)

    # Fifth error
    print("Test 5: Attribute Error")

    value = test_attribute_error(
        first_student
    )

    print("Attribute test result:", value)

    # Sixth error
    print("Test 6: File Error")

    value = test_file_error()

    print("File test result:", value)


# ============================================================
# END OF TEST FILE
# ============================================================

print_final_summary(database)

advanced_analysis(database)

export_final_data(database)

run_healing_test(database)

print()
print("=" * 70)
print("ALL TESTS COMPLETED")
print("=" * 70)
