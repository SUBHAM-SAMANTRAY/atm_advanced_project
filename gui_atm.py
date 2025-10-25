from tkinter import *
from tkinter import messagebox, simpledialog
import db
db.init_db()

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title('ATM GUI')
        self.username = None
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def main_menu(self):
        self.clear()
        Label(self.root, text='ATM System', font=('Arial', 16)).pack(pady=10)
        Button(self.root, text='Sign Up', command=self.signup, width=10).pack(pady=2)
        Button(self.root, text='Login', command=self.login, width=10).pack(pady=2)
        Button(self.root, text='Exit', command=self.root.quit, width=10).pack(pady=2)

    def signup(self):
        self.clear()
        username = simpledialog.askstring("Signup", "Username:")
        pin = simpledialog.askstring("Signup", "4-digit PIN:", show='*')
        if not(username and pin and pin.isdigit() and len(pin)==4):
            messagebox.showerror("Error", "Invalid input!")
            self.main_menu(); return
        try:
            db.add_user(username, pin)
            messagebox.showinfo("Success", "Account created.")
        except:
            messagebox.showerror("Error", "User exists!")
        self.main_menu()

    def login(self):
        self.clear()
        username = simpledialog.askstring("Login", "Username:")
        pin = simpledialog.askstring("Login", "PIN:", show='*')
        user = db.get_user(username)
        if not user or pin != user[0]:
            messagebox.showerror("Login Failed", "Wrong username/PIN")
            self.main_menu(); return
        self.username = username
        self.atm_menu()

    def atm_menu(self):
        self.clear()
        Label(self.root, text=f'Welcome, {self.username}', font=('Arial', 15)).pack(pady=10)
        Button(self.root, text='Balance', command=self.check_bal, width=15).pack(pady=2)
        Button(self.root, text='Deposit', command=self.deposit, width=15).pack(pady=2)
        Button(self.root, text='Withdraw', command=self.withdraw, width=15).pack(pady=2)
        Button(self.root, text='History', command=self.history, width=15).pack(pady=2)
        Button(self.root, text='PIN Change', command=self.pin_change, width=15).pack(pady=2)
        Button(self.root, text='Logout', command=self.main_menu, width=15).pack(pady=10)

    def check_bal(self):
        bal = db.get_user(self.username)[1]
        messagebox.showinfo("Balance", f"Your balance: Rs {bal}")

    def deposit(self):
        amt = simpledialog.askinteger("Deposit", "Amount:")
        if amt and amt > 0:
            db.change_balance(self.username, amt)
            db.log_transaction(self.username, f"Deposited Rs {amt}")
            messagebox.showinfo("Done", "Deposited.")
        else:
            messagebox.showerror("Error", "Invalid!")
        self.atm_menu()

    def withdraw(self):
        amt = simpledialog.askinteger("Withdraw", "Amount:")
        bal = db.get_user(self.username)[1]
        if amt and 0 < amt <= bal:
            db.change_balance(self.username, -amt)
            db.log_transaction(self.username, f"Withdrew Rs {amt}")
            messagebox.showinfo("Done", "Withdrawn.")
        else:
            messagebox.showerror("Error", "Invalid or insufficient funds")
        self.atm_menu()

    def history(self):
        hist = db.get_history(self.username)
        messagebox.showinfo("History", "\n".join(hist) if hist else "No transactions.")

    def pin_change(self):
        pin = simpledialog.askstring("PIN", "New 4-digit PIN:", show='*')
        if pin and pin.isdigit() and len(pin)==4:
            db.add_user(self.username, pin) # Just update pin (overwrites)
            messagebox.showinfo("Done", "PIN changed.")
        else:
            messagebox.showerror("Error", "Invalid!")
        self.atm_menu()

if __name__ == '__main__':
    root = Tk()
    ATMApp(root)
    root.mainloop()
