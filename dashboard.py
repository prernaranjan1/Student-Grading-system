from tkinter import *
from tkinter import messagebox
import os

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grading Management System")
        self.root.geometry("600x400+450+200")
        self.root.config(bg="white")

        Label(self.root, text="Main Dashboard", font=("Helvetica", 20, "bold"), bg="#0b5377", fg="white").pack(fill=X)

        # Main Functional Buttons
        Button(self.root, text="1. Course Details", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white",
               command=self.open_course_details).place(x=180, y=80, width=250, height=40)

        Button(self.root, text="2. Student Registration", font=("Arial", 14, "bold"), bg="#28a745", fg="white",
               command=self.open_student_registration).place(x=180, y=140, width=250, height=40)

        Button(self.root, text="3. Result Entry", font=("Arial", 14, "bold"), bg="#ffc107", fg="black",
               command=self.open_result_entry).place(x=180, y=200, width=250, height=40)

        Button(self.root, text="4. View Result & Attendance", font=("Arial", 14, "bold"), bg="#6f42c1", fg="white",
               command=self.open_view_result_attendance).place(x=180, y=260, width=250, height=40)

        Button(self.root, text="Logout", font=("Arial", 12, "bold"), bg="#dc3545", fg="white",
               command=self.logout).place(x=500, y=350, width=80)

    # ===================== Module Launchers =====================

    def open_course_details(self):
        try:
            import course_details
            new_win = Toplevel(self.root)
            course_details.CourseDetails(new_win)
        except ImportError:
            messagebox.showerror("Error", "course_details.py not found!")

    def open_student_registration(self):
        try:
            import student_registration
            new_win = Toplevel(self.root)
            student_registration.StudentRegistration(new_win)
        except ImportError:
            messagebox.showerror("Error", "student_registration.py not found!")

    def open_result_entry(self):
        try:
            import result_entry
            new_win = Toplevel(self.root)
            result_entry.ResultEntry(new_win)
        except ImportError:
            messagebox.showerror("Error", "result_entry.py not found!")

    def open_view_result_attendance(self):
        try:
            import view_result
            new_win = Toplevel(self.root)
            view_result.ViewResultAttendance(new_win)
        except ImportError:
            messagebox.showerror("Error", "view_result.py not found!")

    # ===================== Logout =====================

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Do you really want to logout?", parent=self.root)
        if confirm:
            self.root.destroy()
            os.system("py login.py")




# ===================== Main =====================
if __name__ == "__main__":
    root = Tk()
    app = Dashboard(root)
    root.mainloop()
