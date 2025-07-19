import os
import csv
from tkinter import *
from tkinter import ttk, messagebox

class ResultEntry:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Entry")
        self.root.geometry("700x500+320+120")
        self.root.config(bg="white")

        title = Label(self.root, text="Enter Student Result", font=("goudy old style", 18, "bold"), bg="#033054", fg="white")
        title.pack(side=TOP, fill=X)

        self.var_roll = StringVar()
        self.var_subject = StringVar()
        self.var_marks = StringVar()

        Label(self.root, text="Roll No:", font=("times new roman", 14), bg="white").place(x=50, y=80)
        Entry(self.root, textvariable=self.var_roll, font=("times new roman", 14), bg="lightgray").place(x=180, y=80, width=200)

        Label(self.root, text="Subject:", font=("times new roman", 14), bg="white").place(x=50, y=130)
        Entry(self.root, textvariable=self.var_subject, font=("times new roman", 14), bg="lightgray").place(x=180, y=130, width=200)

        Label(self.root, text="Marks:", font=("times new roman", 14), bg="white").place(x=50, y=180)
        Entry(self.root, textvariable=self.var_marks, font=("times new roman", 14), bg="lightgray").place(x=180, y=180, width=200)

        Button(self.root, text="Save Result", font=("goudy old style", 14, "bold"), bg="#0b5377", fg="white", command=self.save_result).place(x=180, y=240, width=150, height=40)

        # Table
        frame = Frame(self.root, bg="white")
        frame.place(x=20, y=300, width=650, height=180)

        scroll_x = Scrollbar(frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(frame, orient=VERTICAL)

        self.result_table = ttk.Treeview(frame, columns=("roll", "subject", "marks"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.result_table.xview)
        scroll_y.config(command=self.result_table.yview)

        self.result_table.heading("roll", text="Roll No")
        self.result_table.heading("subject", text="Subject")
        self.result_table.heading("marks", text="Marks")
        self.result_table["show"] = "headings"

        self.result_table.column("roll", width=100)
        self.result_table.column("subject", width=200)
        self.result_table.column("marks", width=100)

        self.result_table.pack(fill=BOTH, expand=1)
        self.load_results()

        # Back to Dashboard button
        Button(self.root, text="Back to Dashboard", font=("Arial", 12, "bold"), bg="#007bff", fg="white",
               command=self.back_to_dashboard).place(x=10, y=10)

    def save_result(self):
        if self.var_roll.get() == "" or self.var_subject.get() == "" or self.var_marks.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                marks = float(self.var_marks.get())
                with open("results.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([self.var_roll.get(), self.var_subject.get(), marks])
                messagebox.showinfo("Success", "Result Saved Successfully", parent=self.root)
                self.load_results()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid marks (number)", parent=self.root)

    def load_results(self):
        self.result_table.delete(*self.result_table.get_children())
        if os.path.exists("results.csv"):
            with open("results.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.result_table.insert("", END, values=row)

    def back_to_dashboard(self):
        self.root.destroy()
        import dashboard
        dashboard_root = Tk()
        dashboard.Dashboard(dashboard_root)
        dashboard_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = ResultEntry(root)
    root.mainloop()
