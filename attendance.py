import os
import csv
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class ViewResultAttendance:
    def __init__(self, root):
        self.root = root
        self.root.title("View Result and Attendance")
        self.root.geometry("900x600+250+80")
        self.root.config(bg="white")

        title = Label(self.root, text="View Result and Attendance", font=("goudy old style", 20, "bold"), bg="#343a40", fg="white")
        title.pack(side=TOP, fill=X)

        self.var_roll = StringVar()
        self.var_attendance = StringVar(value="Present")

        search_frame = Frame(self.root, bg="white")
        search_frame.place(x=50, y=70, width=800, height=60)

        Label(search_frame, text="Enter Roll Number:", font=("times new roman", 14), bg="white").place(x=10, y=15)
        Entry(search_frame, textvariable=self.var_roll, font=("times new roman", 14), bg="lightyellow").place(x=180, y=15, width=150)
        Button(search_frame, text="Search Result", font=("goudy old style", 12), bg="#0b5377", fg="white", command=self.search_result).place(x=340, y=10, width=130, height=35)
        Button(search_frame, text="View Attendance", font=("goudy old style", 12), bg="#6c757d", fg="white", command=self.view_attendance).place(x=480, y=10, width=150, height=35)

        # Result Display Area
        self.result_area = Text(self.root, font=("times new roman", 14), bg="lightgray")
        self.result_area.place(x=50, y=150, width=800, height=200)

        # Attendance Panel
        attendance_frame = LabelFrame(self.root, text="Mark Attendance", font=("goudy old style", 14, "bold"), bg="white", fg="#333")
        attendance_frame.place(x=50, y=370, width=800, height=150)

        Label(attendance_frame, text="Date:", font=("times new roman", 14), bg="white").place(x=10, y=20)
        self.date_entry = DateEntry(attendance_frame, font=("times new roman", 14), background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry.place(x=80, y=20, width=150)

        Label(attendance_frame, text="Status:", font=("times new roman", 14), bg="white").place(x=260, y=20)
        self.attendance_cb = ttk.Combobox(attendance_frame, textvariable=self.var_attendance, font=("times new roman", 14), state="readonly")
        self.attendance_cb['values'] = ("Present", "Absent")
        self.attendance_cb.place(x=340, y=20, width=150)
        self.attendance_cb.current(0)

        Button(attendance_frame, text="Mark/Update", font=("goudy old style", 12), bg="#198754", fg="white", command=self.mark_attendance).place(x=520, y=20, width=150, height=35)

        # Back to Dashboard button
        Button(self.root, text="Back to Dashboard", font=("Arial", 12, "bold"), bg="#007bff", fg="white",
               command=self.back_to_dashboard).place(x=10, y=10)

    def back_to_dashboard(self):
        self.root.destroy()
        import dashboard
        dashboard_root = Tk()
        dashboard.Dashboard(dashboard_root)
        dashboard_root.mainloop()

    def search_result(self):
        roll = self.var_roll.get().strip()
        found = False
        self.result_area.delete("1.0", END)

        if roll == "":
            messagebox.showerror("Error", "Please enter Roll Number", parent=self.root)
            return

        if os.path.exists("results.csv"):
            with open("results.csv", "r") as file:
                reader = csv.reader(file)
                self.result_area.insert(END, f"Results for Roll Number: {roll}\n\n")
                for row in reader:
                    if row[0] == roll:
                        self.result_area.insert(END, f"Subject: {row[1]} | Marks: {row[2]}\n")
                        found = True

        if not found:
            self.result_area.insert(END, "No results found for this Roll Number.")

    def mark_attendance(self):
        roll = self.var_roll.get().strip()
        date = self.date_entry.get()
        status = self.var_attendance.get()

        if roll == "":
            messagebox.showerror("Error", "Roll number is required!", parent=self.root)
            return

        records = []
        updated = False

        if os.path.exists("attendance.csv"):
            with open("attendance.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == roll and row[1] == date:
                        row[2] = status
                        updated = True
                    records.append(row)

        if not updated:
            records.append([roll, date, status])

        with open("attendance.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(records)

        if updated:
            messagebox.showinfo("Updated", "Attendance updated successfully.", parent=self.root)
        else:
            messagebox.showinfo("Marked", "Attendance marked successfully.", parent=self.root)

    def view_attendance(self):
        roll = self.var_roll.get().strip()
        self.result_area.delete("1.0", END)

        if roll == "":
            messagebox.showerror("Error", "Please enter Roll Number", parent=self.root)
            return

        found = False
        if os.path.exists("attendance.csv"):
            self.result_area.insert(END, f"Attendance History for Roll Number: {roll}\n\n")
            with open("attendance.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == roll:
                        self.result_area.insert(END, f"Date: {row[1]} | Status: {row[2]}\n")
                        found = True

        if not found:
            self.result_area.insert(END, "No attendance record found for this Roll Number.")

if __name__ == "__main__":
    root = Tk()
    obj = ViewResultAttendance(root)
    root.mainloop()
