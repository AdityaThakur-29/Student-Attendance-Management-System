import tkinter as tk
from tkinter import messagebox, simpledialog



def add_student_file(name):
    with open("students.txt", "a") as f:
        f.write(name + "\n")


def get_students():
    try:
        with open("students.txt", "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []


def delete_student_file(name):
    students = get_students()
    students = [s for s in students if s != name]

    with open("students.txt", "w") as f:
        for student in students:
            f.write(student + "\n")


def mark_attendance_file(date, records):
    with open("attendance.txt", "a") as f:
        f.write("DATE:" + date + "\n")
        for name, status in records:
            f.write(name + "," + status + "\n")
        f.write("\n")


def get_attendance_lines():
    try:
        with open("attendance.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []




def refresh_student_list():
    listbox.delete(0, tk.END)
    for student in get_students():
        listbox.insert(tk.END, student)


def add_student():
    name = simpledialog.askstring("Add Student", "Enter student name:")
    if not name:
        return
    add_student_file(name)
    refresh_student_list()
    messagebox.showinfo("Success", "Student added successfully!")


def delete_student():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a student to delete.")
        return

    student_name = listbox.get(selected[0])
    delete_student_file(student_name)
    refresh_student_list()
    messagebox.showinfo("Deleted", f"{student_name} deleted successfully!")



def mark_attendance():
    students = get_students()
    if not students:
        messagebox.showerror("Error", "No students found.")
        return

    date = simpledialog.askstring("Date", "Enter date (DD-MM-YYYY):")
    if not date:
        return

    records = []
    index = 0

    window = tk.Toplevel(root)
    window.title("Mark Attendance")
    window.geometry("300x200")
    window.resizable(False, False)

    name_label = tk.Label(window, text="", font=("Arial", 14, "bold"))
    name_label.pack(pady=20)

    def show_student():
        name_label.config(text=students[index])

    def mark(status):
        nonlocal index
        records.append((students[index], status))
        index += 1

        if index < len(students):
            show_student()
        else:
            mark_attendance_file(date, records)
            messagebox.showinfo("Success", "Attendance marked!")
            window.destroy()

    tk.Button(window, text="Present", width=12, bg="lightgreen",
              command=lambda: mark("P")).pack(pady=5)
    tk.Button(window, text="Absent", width=12, bg="lightcoral",
              command=lambda: mark("A")).pack(pady=5)

    show_student()



def view_attendance_by_date():
    date = simpledialog.askstring("View Attendance", "Enter date (DD-MM-YYYY):")
    if not date:
        return

    lines = get_attendance_lines()
    found = False
    data = []

    for i in range(len(lines)):
        if lines[i] == "DATE:" + date:
            found = True
            j = i + 1
            while j < len(lines) and lines[j] != "":
                if "," in lines[j]:
                    data.append(lines[j])
                j += 1
            break

    if not found:
        messagebox.showerror("Not Found", "No record found for this date.")
        return

    window = tk.Toplevel(root)
    window.title("Attendance Record")
    window.geometry("300x350")

    tk.Label(window, text=f"Attendance for {date}",
             font=("Arial", 12, "bold")).pack(pady=5)

    box = tk.Listbox(window, width=40)
    box.pack(fill="both", expand=True)

    present = absent = 0
    for line in data:
        name, status = line.split(",")
        if status == "P":
            box.insert(tk.END, f"{name} - Present")
            box.itemconfig(tk.END, fg="green")
            present += 1
        else:
            box.insert(tk.END, f"{name} - Absent")
            box.itemconfig(tk.END, fg="red")
            absent += 1

    tk.Label(window, text=f"Present: {present}", fg="green").pack()
    tk.Label(window, text=f"Absent: {absent}", fg="red").pack()



def calculate_percentage():
    students = get_students()
    lines = get_attendance_lines()

    if not students or not lines:
        messagebox.showerror("Error", "No attendance data found.")
        return

    total_days = 0
    present_count = {student: 0 for student in students}

    i = 0
    while i < len(lines):
        if lines[i].startswith("DATE:"):
            total_days += 1
            i += 1
            while i < len(lines) and lines[i] != "":
                if "," in lines[i]:
                    name, status = lines[i].split(",")
                    if name in present_count and status == "P":
                        present_count[name] += 1
                i += 1
        i += 1

    result = ""
    for student in students:
        percent = (present_count[student] / total_days) * 100 if total_days else 0
        result += f"{student}: {percent:.2f}%\n"

    messagebox.showinfo("Attendance Percentage", result)


# ---------------- GUI WINDOW ----------------

root = tk.Tk()
root.title("Student Attendance System")
root.geometry("400x500")
root.resizable(False, False)

tk.Label(root, text="Student Attendance System",
         font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Student List:").pack()

listbox = tk.Listbox(root, width=40, height=8)
listbox.pack(pady=5)

tk.Button(root, text="Add Student", width=25, command=add_student).pack(pady=3)
tk.Button(root, text="Delete Selected Student", width=25, command=delete_student).pack(pady=3)
tk.Button(root, text="Refresh Student List", width=25, command=refresh_student_list).pack(pady=3)

tk.Button(root, text="Mark Attendance", width=25, command=mark_attendance).pack(pady=5)
tk.Button(root, text="View Attendance by Date", width=25, command=view_attendance_by_date).pack(pady=5)
tk.Button(root, text="View Attendance Percentage", width=25, command=calculate_percentage).pack(pady=5)

tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=10)

refresh_student_list()
root.mainloop()
