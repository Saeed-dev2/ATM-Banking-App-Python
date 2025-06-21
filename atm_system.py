import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import hashlib

# Constants
USER_DIR = "users"
LOG_DIR = "transactions"
DEFAULT_BALANCE = 250000
DEFAULT_PIN = "5678"

# Create directories if they don't exist
os.makedirs(USER_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Color scheme
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
ACCENT_COLOR = "#e74c3c"
BACKGROUND_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
BUTTON_HOVER = "#2980b9"
SUCCESS_COLOR = "#27ae60"
ERROR_COLOR = "#e74c3c"


# Helper functions
def user_file_path(user_id):
    return os.path.join(USER_DIR, f"{user_id}.txt")


def log_file_path(user_id):
    return os.path.join(LOG_DIR, f"{user_id}_log.txt")


def load_user_data(user_id):
    path = user_file_path(user_id)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"{DEFAULT_PIN}\n{DEFAULT_BALANCE}")
    with open(path, "r") as f:
        lines = f.read().splitlines()
        return lines[0], int(lines[1])


def save_user_data(user_id, pin, balance):
    path = user_file_path(user_id)
    with open(path, "w") as f:
        f.write(f"{pin}\n{balance}")


def log_transaction(user_id, action, amount, balance):
    log_path = log_file_path(user_id)
    with open(log_path, "a") as f:
        f.write(f"{datetime.now()} | {action}: Rs.{amount} | Balance: Rs.{balance}\n")


def read_transaction_log(user_id):
    path = log_file_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "No transactions yet."


def hash_pin(pin):
    """Simple PIN hashing for demonstration purposes"""
    return hashlib.sha256(pin.encode()).hexdigest()


class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SKF ATM System")
        self.root.geometry("800x600")
        self.root.configure(bg=BACKGROUND_COLOR)

        # Set application icon
        try:
            img = tk.PhotoImage(file='icon.png')
            self.root.iconphoto(False, img)
        except:
            pass  # Continue without icon if not found

        # Configure styles
        self.configure_styles()

        # Initialize variables
        self.user_id = ""
        self.pin = ""
        self.balance = 0
        self.account_label = None
        self.balance_label = None

        # Create main container
        self.main_container = ttk.Frame(root, style="Main.TFrame")
        self.main_container.pack(fill="both", expand=True)

        # Show login screen
        self.login_screen()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure main frame
        style.configure("Main.TFrame", background=BACKGROUND_COLOR)

        # Configure labels
        style.configure("Title.TLabel",
                        background=BACKGROUND_COLOR,
                        foreground=PRIMARY_COLOR,
                        font=("Arial", 24, "bold"),
                        padding=10)

        style.configure("Subtitle.TLabel",
                        background=BACKGROUND_COLOR,
                        foreground=TEXT_COLOR,
                        font=("Arial", 14),
                        padding=5)

        style.configure("Normal.TLabel",
                        background=BACKGROUND_COLOR,
                        foreground=TEXT_COLOR,
                        font=("Arial", 12))

        # Configure buttons
        style.configure("Primary.TButton",
                        background=BUTTON_COLOR,
                        foreground="white",
                        font=("Arial", 12, "bold"),
                        borderwidth=1,
                        padding=10)

        style.map("Primary.TButton",
                  background=[('active', BUTTON_HOVER), ('pressed', BUTTON_HOVER)])

        style.configure("Secondary.TButton",
                        background=SECONDARY_COLOR,
                        foreground="white",
                        font=("Arial", 12),
                        borderwidth=1,
                        padding=8)

        style.map("Secondary.TButton",
                  background=[('active', BUTTON_HOVER), ('pressed', BUTTON_HOVER)])

        style.configure("Danger.TButton",
                        background=ERROR_COLOR,
                        foreground="white",
                        font=("Arial", 12),
                        borderwidth=1,
                        padding=8)

        style.map("Danger.TButton",
                  background=[('active', "#c0392b"), ('pressed', "#c0392b")])

        # Configure entry fields
        style.configure("TEntry",
                        fieldbackground="white",
                        font=("Arial", 12),
                        padding=5,
                        relief="flat")

        # Configure text widget
        style.configure("History.TFrame", background="white")
        style.configure("History.Text",
                        background="white",
                        foreground=TEXT_COLOR,
                        font=("Courier New", 10),
                        relief="flat",
                        padx=10,
                        pady=10)

    def clear_screen(self):
        """Clear all widgets from the main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
        # Reset header references
        self.account_label = None
        self.balance_label = None

    def create_header(self, title):
        """Create a header section for each screen"""
        header_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        header_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(header_frame, text="SKF Bank", style="Title.TLabel").pack(side="left")

        if self.user_id:
            account_frame = ttk.Frame(header_frame, style="Main.TFrame")
            account_frame.pack(side="right")

            # Create account label if it doesn't exist
            if not self.account_label:
                self.account_label = ttk.Label(account_frame, text=f"Account: {self.user_id}", style="Normal.TLabel")
                self.account_label.pack(anchor="e")

            # Create balance label if it doesn't exist
            if not self.balance_label:
                self.balance_label = ttk.Label(account_frame, text=f"Balance: Rs.{self.balance}/-",
                                               style="Normal.TLabel")
                self.balance_label.pack(anchor="e")
            else:
                # Update existing balance label
                self.balance_label.config(text=f"Balance: Rs.{self.balance}/-")

        separator = ttk.Separator(self.main_container, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=5)

        title_label = ttk.Label(self.main_container, text=title, style="Subtitle.TLabel")
        title_label.pack(pady=(20, 10))

        return title_label

    def login_screen(self):
        """Create the login screen"""
        self.clear_screen()
        self.create_header("Secure Login")

        # Create form container
        form_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        form_frame.pack(fill="both", expand=True, padx=100, pady=20)

        # Account ID field
        id_frame = ttk.Frame(form_frame, style="Main.TFrame")
        id_frame.pack(fill="x", pady=10)
        ttk.Label(id_frame, text="Account ID:", style="Normal.TLabel").pack(side="left", padx=(0, 10))
        self.user_entry = ttk.Entry(id_frame, style="TEntry", width=20)
        self.user_entry.pack(side="right", fill="x", expand=True)
        self.user_entry.focus()

        # PIN field
        pin_frame = ttk.Frame(form_frame, style="Main.TFrame")
        pin_frame.pack(fill="x", pady=10)
        ttk.Label(pin_frame, text="PIN:", style="Normal.TLabel").pack(side="left", padx=(0, 10))
        self.pin_entry = ttk.Entry(pin_frame, style="TEntry", show="•", width=20)
        self.pin_entry.pack(side="right", fill="x", expand=True)

        # Buttons
        button_frame = ttk.Frame(form_frame, style="Main.TFrame")
        button_frame.pack(fill="x", pady=30)

        ttk.Button(button_frame, text="Login", style="Primary.TButton",
                   command=self.authenticate).pack(side="right", padx=5)

        # Footer
        footer_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Label(footer_frame, text="© 2025 SKF Bank. All rights reserved.",
                  style="Normal.TLabel").pack()

        # Bind Enter key to login
        self.root.bind("<Return>", lambda e: self.authenticate())

    def authenticate(self):
        """Authenticate user credentials"""
        user_id = self.user_entry.get().strip()
        pin_input = self.pin_entry.get().strip()

        if not user_id or not pin_input:
            messagebox.showerror("Error", "Please enter both Account ID and PIN", parent=self.root)
            return

        try:
            pin, balance = load_user_data(user_id)
            if pin_input == pin:
                self.user_id = user_id
                self.pin = pin
                self.balance = balance
                self.root.unbind("<Return>")
                self.main_menu()
            else:
                messagebox.showerror("Error", "Incorrect PIN", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}", parent=self.root)

    def main_menu(self):
        """Create the main menu screen"""
        self.clear_screen()
        self.create_header("Main Menu")

        # Create button grid
        button_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        button_frame.pack(fill="both", expand=True, padx=50, pady=20)

        # Row 1
        row1_frame = ttk.Frame(button_frame, style="Main.TFrame")
        row1_frame.pack(fill="x", pady=10)

        ttk.Button(row1_frame, text="Balance Inquiry", style="Primary.TButton",
                   command=self.balance_inquiry, width=20).pack(side="left", expand=True, padx=10)

        ttk.Button(row1_frame, text="Withdraw", style="Primary.TButton",
                   command=self.withdraw, width=20).pack(side="left", expand=True, padx=10)

        # Row 2
        row2_frame = ttk.Frame(button_frame, style="Main.TFrame")
        row2_frame.pack(fill="x", pady=10)

        ttk.Button(row2_frame, text="Deposit", style="Primary.TButton",
                   command=self.deposit, width=20).pack(side="left", expand=True, padx=10)

        ttk.Button(row2_frame, text="Change PIN", style="Primary.TButton",
                   command=self.change_pin, width=20).pack(side="left", expand=True, padx=10)

        # Row 3
        row3_frame = ttk.Frame(button_frame, style="Main.TFrame")
        row3_frame.pack(fill="x", pady=10)

        ttk.Button(row3_frame, text="Transaction History", style="Secondary.TButton",
                   command=self.show_history, width=20).pack(side="left", expand=True, padx=10)

        ttk.Button(row3_frame, text="Exit", style="Danger.TButton",
                   command=self.exit_app, width=20).pack(side="left", expand=True, padx=10)

        # Footer
        footer_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        footer_frame.pack(side="bottom", fill="x", pady=10)
        ttk.Label(footer_frame, text=f"Logged in as: {self.user_id} | Press 'Exit' to logout",
                  style="Normal.TLabel").pack()

    def balance_inquiry(self):
        """Show balance information"""
        messagebox.showinfo("Balance Inquiry",
                            f"Your current balance is Rs. {self.balance}/-\n\n"
                            "Available for withdrawal: Rs. {}/-".format(min(self.balance, 25000)),
                            parent=self.root)

    def withdraw(self):
        """Handle withdrawal operation"""
        amount = simpledialog.askstring("Withdraw",
                                        "Enter amount (multiples of 5.00, max Rs.25,000):",
                                        parent=self.root)
        if not amount:
            return

        try:
            amount = int(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive", parent=self.root)
                return

            if amount % 5.00 != 0:
                messagebox.showerror("Error", "Amount must be in multiples of 5.00", parent=self.root)
                return

            if amount > 25000:
                messagebox.showerror("Error", "Maximum withdrawal is Rs.25,000 per transaction", parent=self.root)
                return

            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient funds", parent=self.root)
                return

            # Confirm withdrawal
            confirm = messagebox.askyesno("Confirm Withdrawal",
                                          f"Withdraw Rs.{amount}?\n\n"
                                          f"Current balance: Rs.{self.balance}\n"
                                          f"New balance: Rs.{self.balance - amount}",
                                          parent=self.root)
            if not confirm:
                return

            self.balance -= amount
            log_transaction(self.user_id, "Withdraw", amount, self.balance)
            save_user_data(self.user_id, self.pin, self.balance)

            # Update balance in header
            if self.balance_label:
                self.balance_label.config(text=f"Balance: Rs.{self.balance}/-")

            messagebox.showinfo("Success",
                                f"Rs.{amount} successfully withdrawn.\n\n"
                                f"Your new balance is Rs.{self.balance}/-",
                                parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount", parent=self.root)

    def deposit(self):
        """Handle deposit operation"""
        amount = simpledialog.askstring("Deposit",
                                        "Enter amount (multiples of 5.00, max Rs.90,000):",
                                        parent=self.root)
        if not amount:
            return

        try:
            amount = int(amount)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive", parent=self.root)
                return

            if amount % 5.00 != 0:
                messagebox.showerror("Error", "Amount must be in multiples of 5.00", parent=self.root)
                return

            if amount > 90000:
                messagebox.showerror("Error", "Maximum deposit is Rs.90,000 per transaction", parent=self.root)
                return

            # Confirm deposit
            confirm = messagebox.askyesno("Confirm Deposit",
                                          f"Deposit Rs.{amount}?\n\n"
                                          f"Current balance: Rs.{self.balance}\n"
                                          f"New balance: Rs.{self.balance + amount}",
                                          parent=self.root)
            if not confirm:
                return

            self.balance += amount
            log_transaction(self.user_id, "Deposit", amount, self.balance)
            save_user_data(self.user_id, self.pin, self.balance)

            # Update balance in header
            if self.balance_label:
                self.balance_label.config(text=f"Balance: Rs.{self.balance}/-")

            messagebox.showinfo("Success",
                                f"Rs.{amount} successfully deposited.\n\n"
                                f"Your new balance is Rs.{self.balance}/-",
                                parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount", parent=self.root)

    def change_pin(self):
        """Handle PIN change"""
        current = simpledialog.askstring("Change PIN", "Enter current PIN:",
                                         show="•", parent=self.root)
        if not current:
            return

        if current != self.pin:
            messagebox.showerror("Error", "Incorrect current PIN", parent=self.root)
            return

        new1 = simpledialog.askstring("Change PIN", "Enter new PIN:",
                                      show="•", parent=self.root)
        if not new1:
            return

        if len(new1) < 4:
            messagebox.showerror("Error", "PIN must be at least 4 digits", parent=self.root)
            return

        new2 = simpledialog.askstring("Change PIN", "Confirm new PIN:",
                                      show="•", parent=self.root)
        if not new2:
            return

        if new1 != new2:
            messagebox.showerror("Error", "PINs do not match", parent=self.root)
            return

        self.pin = new1
        save_user_data(self.user_id, self.pin, self.balance)
        messagebox.showinfo("Success", "PIN changed successfully", parent=self.root)

    def show_history(self):
        """Display transaction history"""
        history = read_transaction_log(self.user_id)

        # Create history window
        top = tk.Toplevel(self.root)
        top.title("Transaction History")
        top.geometry("800x500")
        top.configure(bg=BACKGROUND_COLOR)
        top.resizable(True, True)

        # Header
        header_frame = ttk.Frame(top, style="Main.TFrame")
        header_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(header_frame, text="Transaction History", style="Title.TLabel").pack(side="left")
        ttk.Label(header_frame, text=f"Account: {self.user_id}", style="Normal.TLabel").pack(side="right")

        separator = ttk.Separator(top, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=5)

        # History content
        content_frame = ttk.Frame(top, style="History.TFrame")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget for history
        text = tk.Text(content_frame, wrap="word", font=("Courier New", 10),
                       bg="white", fg=TEXT_COLOR, yscrollcommand=scrollbar.set)
        text.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=text.yview)

        # Insert history
        text.insert("1.0", history)
        text.config(state="disabled")

        # Close button
        button_frame = ttk.Frame(top, style="Main.TFrame")
        button_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(button_frame, text="Close", style="Secondary.TButton",
                   command=top.destroy).pack(side="right")

    def exit_app(self):
        """Exit the application"""
        save_user_data(self.user_id, self.pin, self.balance)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()