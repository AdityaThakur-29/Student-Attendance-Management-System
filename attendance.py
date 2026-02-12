def add_student():
    name = input("Enter student name: ")
    with open("students.txt", "a") as f:
        f.write(name + "\n")
    print("Student added successfully!\n")


def get_students():
    try:
        with open("students.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []


def mark_attendance():
    students = get_students()
    if not students:
        print("No students found. Add students first.\n")
        return

    date = input("Enter date (DD-MM-YYYY): ")
    with open("attendance.txt", "a") as f:
        f.write(f"\n{date}\n")
        for student in students:
            status = input(f"Is {student} present? (P/A): ").upper()
            f.write(f"{student},{status}\n")

    print("Attendance marked!\n")


def view_attendance_by_date():
    date = input("Enter date to view attendance: ")
    try:
        with open("attendance.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("No attendance records found.\n")
        return

    found = False
    for i in range(len(lines)):
        if lines[i] == date:
            print(f"\nAttendance for {date}:")
            j = i + 1
            while j < len(lines) and lines[j] != "":
                print(lines[j])
                j += 1
            found = True
            break

    if not found:
        print("No record found for this date.\n")


def calculate_percentage():
    students = get_students()
    if not students:
        print("No students found.\n")
        return

    try:
        with open("attendance.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("No attendance data found.\n")
        return

    total_days = 0
    present_count = {student: 0 for student in students}

    i = 0
    while i < len(lines):
        if lines[i] != "":
            total_days += 1
            i += 1
            while i < len(lines) and lines[i] != "":
                if "," in lines[i]:   # ✅ SAFE CHECK
                    name, status = lines[i].split(",")
                    if status == "P":
                        present_count[name] += 1
                i += 1
        i += 1

    print("\n--- Attendance Percentage ---")
    for student in students:
        percent = (present_count[student] / total_days) * 100 if total_days else 0
        print(f"{student}: {percent:.2f}%")
    print()


# ---------------- MAIN MENU ----------------

while True:
    print("===== Student Attendance System =====")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. View Attendance by Date")
    print("4. View Attendance Percentage")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        mark_attendance()
    elif choice == "3":
        view_attendance_by_date()
    elif choice == "4":
        calculate_percentage()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice!\n")
