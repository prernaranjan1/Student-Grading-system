import os
import csv
from tkinter import *
from tkinter import ttk, messagebox

class StudentRegistration:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Registration")
        self.root.geometry("750x600+300+80")
        self.root.config(bg="white")

        title = Label(self.root, text="Student Registration Form", font=("goudy old style", 18, "bold"), bg="#033054", fg="white")
        title.pack(side=TOP, fill=X)

        # Variables
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_course = StringVar()
        self.var_gender = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()

        # Form Labels & Entries
        Label(self.root, text="Student Name:", font=("times new roman", 14), bg="white").place(x=30, y=70)
        Entry(self.root, textvariable=self.var_name, font=("times new roman", 14), bg="lightgray").place(x=200, y=70, width=250)

        Label(self.root, text="Roll Number:", font=("times new roman", 14), bg="white").place(x=30, y=120)
        Entry(self.root, textvariable=self.var_roll, font=("times new roman", 14), bg="lightgray").place(x=200, y=120, width=250)

        Label(self.root, text="Course:", font=("times new roman", 14), bg="white").place(x=30, y=170)
        self.course_combobox = ttk.Combobox(self.root, textvariable=self.var_course, font=("times new roman", 14), state="readonly")
        self.course_combobox["values"] = ("Select", "B.Tech", "B.Sc", "BCA", "MCA", "MBA")
        self.course_combobox.current(0)
        self.course_combobox.place(x=200, y=170, width=250)

        Label(self.root, text="Gender:", font=("times new roman", 14), bg="white").place(x=30, y=220)
        self.gender_combobox = ttk.Combobox(self.root, textvariable=self.var_gender, font=("times new roman", 14), state="readonly")
        self.gender_combobox["values"] = ("Select", "Male", "Female", "Other")
        self.gender_combobox.current(0)
        self.gender_combobox.place(x=200, y=220, width=250)

        Label(self.root, text="Email:", font=("times new roman", 14), bg="white").place(x=30, y=270)
        Entry(self.root, textvariable=self.var_email, font=("times new roman", 14), bg="lightgray").place(x=200, y=270, width=250)

        Label(self.root, text="Contact No:", font=("times new roman", 14), bg="white").place(x=30, y=320)
        Entry(self.root, textvariable=self.var_contact, font=("times new roman", 14), bg="lightgray").place(x=200, y=320, width=250)

        # Buttons
        Button(self.root, text="Submit", font=("goudy old style", 12, "bold"), bg="#0b5377", fg="white", command=self.save_data).place(x=200, y=380, width=100, height=40)
        Button(self.root, text="View", font=("goudy old style", 12, "bold"), bg="#198754", fg="white", command=self.view_students).place(x=310, y=380, width=100, height=40)
        Button(self.root, text="Update", font=("goudy old style", 12, "bold"), bg="#ffc107", fg="black", command=self.update_student).place(x=420, y=380, width=100, height=40)
        Button(self.root, text="Delete", font=("goudy old style", 12, "bold"), bg="#dc3545", fg="white", command=self.delete_student).place(x=530, y=380, width=100, height=40)
        Button(self.root, text="Back to Dashboard", font=("goudy old style", 12, "bold"), bg="#007bff", fg="white", command=self.back_to_dashboard).place(x=30, y=10)

        # Table
        frame = Frame(self.root, bg="white")
        frame.place(x=30, y=440, width=690, height=140)

        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(frame, columns=("roll", "name", "course", "gender", "email", "contact"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("contact", text="Contact No")
        self.student_table["show"] = "headings"

        self.student_table.column("roll", width=80)
        self.student_table.column("name", width=120)
        self.student_table.column("course", width=100)
        self.student_table.column("gender", width=80)
        self.student_table.column("email", width=150)
        self.student_table.column("contact", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_selected_data)

        self.view_students()

    def back_to_dashboard(self):
        self.root.destroy()

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("Select")
        self.var_gender.set("Select")
        self.var_email.set("")
        self.var_contact.set("")

    def save_data(self):
        if self.var_name.get() == "" or self.var_roll.get() == "" or self.var_course.get() == "Select":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        if os.path.exists("students.csv"):
            with open("students.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == self.var_roll.get():
                        messagebox.showerror("Error", "Roll number already exists!", parent=self.root)
                        return

        with open("students.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                             self.var_gender.get(), self.var_email.get(), self.var_contact.get()])
        messagebox.showinfo("Success", "Student Registered Successfully!", parent=self.root)
        self.view_students()
        self.clear_fields()

    def view_students(self):
        if not os.path.exists("students.csv"):
            return
        self.student_table.delete(*self.student_table.get_children())
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    self.student_table.insert("", END, values=row)

    def get_selected_data(self, event):
        selected = self.student_table.focus()
        data = self.student_table.item(selected)
        values = data["values"]
        if values:
            self.var_roll.set(values[0])
            self.var_name.set(values[1])
            self.var_course.set(values[2])
            self.var_gender.set(values[3])
            self.var_email.set(values[4])
            self.var_contact.set(values[5])

    def delete_student(self):
        roll_to_delete = self.var_roll.get().strip()
        if not roll_to_delete:
            messagebox.showerror("Error", "Please select a student record first!", parent=self.root)
            return

        students = []
        deleted = False
        if os.path.exists("students.csv"):
            with open("students.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] != roll_to_delete:
                        students.append(row)
                    else:
                        deleted = True

            with open("students.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(students)

        if deleted:
            messagebox.showinfo("Deleted", "Student Record Deleted!", parent=self.root)
            self.view_students()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Roll Number not found!", parent=self.root)

    def update_student(self):
        students = []
        updated = False
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == self.var_roll.get():
                    row = [self.var_roll.get(), self.var_name.get(), self.var_course.get(),
                           self.var_gender.get(), self.var_email.get(), self.var_contact.get()]
                    updated = True
                students.append(row)

        if updated:
            with open("students.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(students)
            messagebox.showinfo("Success", "Student Updated Successfully!", parent=self.root)
            self.view_students()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Roll Number not found!", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = StudentRegistration(root)
    root.mainloop()
