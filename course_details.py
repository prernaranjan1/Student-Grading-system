from tkinter import *
from tkinter import ttk, messagebox
import csv
import os

class CourseDetails:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Details")
        self.root.geometry("800x500+350+150")
        self.root.config(bg="white")

        self.var_course_id = StringVar()
        self.var_course_name = StringVar()
        self.var_course_type = StringVar()

        Label(self.root, text="Course Details", font=("Helvetica", 20, "bold"), bg="#0b5377", fg="white").pack(fill=X)

        # Labels and Entries
        Label(self.root, text="Course ID:", font=("Arial", 14), bg="white").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_course_id, font=("Arial", 14), bg="lightyellow").place(x=180, y=80, width=200)

        Label(self.root, text="Course Name:", font=("Arial", 14), bg="white").place(x=50, y=130)
        Entry(self.root, textvariable=self.var_course_name, font=("Arial", 14), bg="lightyellow").place(x=180, y=130, width=200)

        Label(self.root, text="Course Type:", font=("Arial", 14), bg="white").place(x=50, y=180)
        self.type_combo = ttk.Combobox(self.root, textvariable=self.var_course_type, font=("Arial", 14), state="readonly")
        self.type_combo['values'] = ("Core", "Elective", "Lab")
        self.type_combo.place(x=180, y=180, width=200)
        self.type_combo.current(0)

        # Buttons
        Button(self.root, text="Add Course", font=("Arial", 12), bg="#28a745", fg="white", command=self.add_course).place(x=420, y=80, width=140)
        Button(self.root, text="Search Course", font=("Arial", 12), bg="#17a2b8", fg="white", command=self.search_course).place(x=580, y=80, width=160)
        Button(self.root, text="Delete Course", font=("Arial", 12), bg="#dc3545", fg="white", command=self.delete_course).place(x=420, y=130, width=140)
        Button(self.root, text="Show All Courses", font=("Arial", 12), bg="#6f42c1", fg="white", command=self.display_courses).place(x=580, y=130, width=160)

        # Text area with scrollbar
        frame = Frame(self.root, bg="white")
        frame.place(x=50, y=250, width=700, height=200)

        self.scrollbar = Scrollbar(frame, orient=VERTICAL)
        self.course_list = Text(frame, font=("Arial", 12), bg="lightgrey", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.course_list.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.course_list.pack(fill=BOTH, expand=1)

        Button(self.root, text="Back to Dashboard", font=("Arial", 12, "bold"), bg="#007bff", fg="white",
               command=self.back_to_dashboard).place(x=10, y=10)

        self.display_courses()

    def back_to_dashboard(self):
        self.root.destroy()

    def add_course(self):
        cid = self.var_course_id.get().strip()
        cname = self.var_course_name.get().strip()
        ctype = self.var_course_type.get().strip()

        if cid == "" or cname == "" or ctype == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        # Check for duplicate course ID
        if os.path.exists("courses.csv"):
            with open("courses.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == cid:
                        messagebox.showerror("Error", "Course ID already exists!", parent=self.root)
                        return

        with open("courses.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([cid, cname, ctype])

        messagebox.showinfo("Success", "Course added successfully.", parent=self.root)
        self.display_courses()

    def search_course(self):
        cid = self.var_course_id.get().strip()
        self.course_list.delete("1.0", END)
        found = False

        if os.path.exists("courses.csv"):
            with open("courses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == cid:
                        self.course_list.insert(END, f"ID: {row[0]} | Name: {row[1]} | Type: {row[2]}\n")
                        found = True

        if not found:
            self.course_list.insert(END, "No course found with the given ID.")

    def delete_course(self):
        cid = self.var_course_id.get().strip()
        rows = []
        deleted = False

        if os.path.exists("courses.csv"):
            with open("courses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] != cid:
                        rows.append(row)
                    else:
                        deleted = True

            with open("courses.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        if deleted:
            messagebox.showinfo("Deleted", "Course deleted successfully.", parent=self.root)
        else:
            messagebox.showinfo("Info", "No course found with the given ID.", parent=self.root)

        self.display_courses()

    def display_courses(self):
        self.course_list.delete("1.0", END)

        if os.path.exists("courses.csv"):
            with open("courses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.course_list.insert(END, f"ID: {row[0]} | Name: {row[1]} | Type: {row[2]}\n")


if __name__ == "__main__":
    root = Tk()
    obj = CourseDetails(root)
    root.mainloop()
