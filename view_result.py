import os
import csv
from tkinter import *
from tkinter import ttk, messagebox
from subprocess import call

class ViewResultAttendance:
    def __init__(self, root):
        self.root = root
        self.root.title("View Result and Attendance")
        self.root.geometry("800x500+300+100")
        self.root.config(bg="white")

        title = Label(self.root, text="View Result and Attendance", font=("goudy old style", 20, "bold"), bg="#343a40", fg="white")
        title.pack(side=TOP, fill=X)

        self.var_roll = StringVar()

        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=50, y=70, width=700, height=60)

        Label(search_frame, text="Enter Roll Number:", font=("times new roman", 14), bg="white").place(x=10, y=15)
        Entry(search_frame, textvariable=self.var_roll, font=("times new roman", 14), bg="lightyellow").place(x=180, y=15, width=200)
        Button(search_frame, text="Search", font=("goudy old style", 12), bg="#0b5377", fg="white", command=self.search_result).place(x=400, y=10, width=120, height=35)

        self.result_area = Text(self.root, font=("times new roman", 14), bg="lightgray")
        self.result_area.place(x=50, y=150, width=700, height=300)

        Button(self.root, text="Back to Dashboard", font=("goudy old style", 12), bg="#6c757d", fg="white", command=self.back_to_dashboard).place(x=600, y=20, width=180, height=35)

    def calculate_grade(self, total):
        if total >= 90:
            return "A+"
        elif total >= 80:
            return "A"
        elif total >= 70:
            return "B"
        elif total >= 60:
            return "C"
        elif total >= 50:
            return "D"
        else:
            return "F"

    def get_extra_marks(self, attendance_percent):
        if attendance_percent >= 90:
            return 5
        elif attendance_percent >= 80:
            return 4
        elif attendance_percent >= 75:
            return 3
        return 0

    def get_attendance(self, roll):
        if os.path.exists("attendance.csv"):
            with open("attendance.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == roll:
                        try:
                            return float(row[1])
                        except:
                            return 0
        return 0

    def search_result(self):
        roll = self.var_roll.get()
        found = False
        self.result_area.delete("1.0", END)

        if roll == "":
            messagebox.showerror("Error", "Please enter Roll Number", parent=self.root)
            return

        total_marks = 0
        subject_count = 0

        self.result_area.insert(END, f"Results for Roll Number: {roll}\n\n")
        self.result_area.insert(END, f"{'Subject':<30} {'Marks':>10}\n")
        self.result_area.insert(END, "-" * 45 + "\n")

        if os.path.exists("results.csv"):
            with open("results.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == roll:
                        found = True
                        try:
                            marks = float(row[2])
                            total_marks += marks
                            subject_count += 1
                            self.result_area.insert(END, f"{row[1]:<30} {marks:>10.2f}\n")
                        except:
                            continue

        if not found:
            self.result_area.insert(END, "\nNo results found for this Roll Number.")
            return

        # Attendance Handling
        attendance_percent = self.get_attendance(roll)
        extra_marks = self.get_extra_marks(attendance_percent)
        final_total = total_marks + extra_marks
        average_marks = final_total / subject_count if subject_count else 0
        grade = self.calculate_grade(average_marks)

        self.result_area.insert(END, "-" * 45 + "\n")
        self.result_area.insert(END, f"\nTotal Marks (Before Extra): {total_marks:.2f}")
        self.result_area.insert(END, f"\nAttendance: {attendance_percent:.2f}%")
        self.result_area.insert(END, f"\nExtra Marks for Attendance: {extra_marks}")
        self.result_area.insert(END, f"\nFinal Total Marks: {final_total:.2f}")
        self.result_area.insert(END, f"\nGrade: {grade}")

    def back_to_dashboard(self):
        self.root.destroy()
        call(["python", "dashboard.py"])


if __name__ == "__main__":
    root = Tk()
    obj = ViewResultAttendance(root)
    root.mainloop()
