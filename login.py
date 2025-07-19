from tkinter import *
from tkinter import messagebox

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300+500+200")
        self.root.config(bg="white")

        # Title
        Label(self.root, text="Student Grading System Login", font=("Helvetica", 16, "bold"), bg="#0b5377", fg="white", pady=10).pack(fill=X)

        # Username
        Label(self.root, text="Username", font=("Arial", 12), bg="white").place(x=50, y=80)
        self.username_entry = Entry(self.root, font=("Arial", 12), bg="lightgray")
        self.username_entry.place(x=150, y=80, width=200)

        # Password
        Label(self.root, text="Password", font=("Arial", 12), bg="white").place(x=50, y=130)
        self.password_entry = Entry(self.root, show="*", font=("Arial", 12), bg="lightgray")
        self.password_entry.place(x=150, y=130, width=200)

        # Login Button
        Button(self.root, text="Login", font=("Arial", 12, "bold"), bg="#0b5377", fg="white", command=self.login).place(x=150, y=180, width=100)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Success", "Login Successful", parent=self.root)
            self.root.destroy()  # Close login window

            # Open Main Dashboard
            import dashboard
            from dashboard import Dashboard

            new_root = Tk()
            dashboard_app = Dashboard(new_root)
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = LoginPage(root)
    root.mainloop()
