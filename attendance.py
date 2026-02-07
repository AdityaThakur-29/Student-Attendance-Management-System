# Student Attendance Management System

def add_student():
    name = input("Enter student name: ")
    with open("students.txt", "a") as f:
        f.write(name + "\n")
    print("Student added successfully!\n")


def mark_attendance():
    try:
        with open("students.txt", "r") as f:
            students = f.readlines()
    except FileNotFoundError:
        print("No students found. Add students first.\n")
        return

    date = input("Enter date (DD-MM-YYYY): ")
    with open("attendance.txt", "a") as f:
        f.write(f"\nDate: {date}\n")
        for student in students:
            student = student.strip()
            status = input(f"Is {student} present? (P/A): ")
            f.write(f"{student}: {status}\n")

    print("Attendance marked!\n")


def view_attendance():
    try:
        with open("attendance.txt", "r") as f:
            print("\n--- Attendance Records ---")
            print(f.read())
    except FileNotFoundError:
        print("No attendance records found.\n")


while True:
    print("===== Student Attendance System =====")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. View Attendance")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        mark_attendance()
    elif choice == "3":
        view_attendance()
    elif choice == "4":
        print("Exiting program...")
        break
    else:
        print("Invalid choice! Try again.\n")
