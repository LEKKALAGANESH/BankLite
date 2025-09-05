import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Account:
    def __init__(self, account_id, name, balance=0.0, pin=None, mobile=None):
        self.id = account_id
        self.name = name
        self.pin = pin
        self.mobile = mobile
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        """Deposit money into the account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "DEPOSIT",
            "amount": amount,
            "balance_after": self.balance
        }
        self.transactions.append(transaction)
        return self.balance
    
    def withdraw(self, amount):
        """Withdraw money from the account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "WITHDRAWAL",
            "amount": amount,
            "balance_after": self.balance
        }
        self.transactions.append(transaction)
        return self.balance
    
    def get_balance(self):
        """Get current balance"""
        return self.balance
    
    def get_history(self):
        """Get transaction history"""
        return self.transactions.copy()

    def change_pin(self, new_pin):
        """Change the account PIN"""
        if not new_pin or len(str(new_pin)) < 4:
            raise ValueError("PIN must be at least 4 digits")
        self.pin = str(new_pin)
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "PIN_CHANGE",
            "amount": 0,
            "balance_after": self.balance
        }
        self.transactions.append(transaction)
        return True
    
    def to_dict(self):
        """Convert account object to dictionary for JSON storage"""
        return {
            "id": self.id,
            "name": self.name,
            "pin": self.pin,
            "mobile": self.mobile,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        """Create account object from dictionary"""
        account = cls(data["id"], data["name"], data["balance"], data.get("pin"), data.get("mobile"))
        account.transactions = data.get("transactions", [])
        return account
    
    def __str__(self):
        return f"Account {self.id}: {self.name} - Balance: ${self.balance:.2f}"

class Bank:
    def __init__(self):
        self.accounts = {}  # Use dict instead of list for faster lookups
    
    def create_account(self, name, initial_balance=0.0, pin=None, mobile=None):
        """Create a new account with a unique ID and check for duplicates"""
        # Check if account name already exists
        for account in self.accounts.values():
            if account.name.lower() == name.lower():
                raise ValueError("Account with this name already exists")
        
        # Check if mobile number already exists
        for account in self.accounts.values():
            if account.mobile == mobile:
                raise ValueError("Account with this mobile number already exists")
        
        account_id = len(self.accounts) + 1  # Simple ID generation
        new_account = Account(account_id, name, initial_balance, pin, mobile)
        self.accounts[account_id] = new_account
        return new_account
    
    def find_account_by_id(self, account_id):
        """Find an account by its ID"""
        return self.accounts.get(account_id)
    
    def find_account_by_name(self, name):
        """Find accounts by name (case-insensitive search)"""
        return [account for account in self.accounts.values() if name.lower() in account.name.lower()]
    
    def authenticate(self, account_id, pin):
        """Authenticate account with PIN"""
        account = self.find_account_by_id(account_id)
        if account and account.pin == pin:
            return account
        return None
    
    def deposit_to_account(self, account_id, amount):
        """Deposit money to an account"""
        account = self.find_account_by_id(account_id)
        if account:
            return account.deposit(amount)
        else:
            raise ValueError("Account not found")
    
    def withdraw_from_account(self, account_id, amount):
        """Withdraw money from an account"""
        account = self.find_account_by_id(account_id)
        if account:
            return account.withdraw(amount)
        else:
            raise ValueError("Account not found")
    
    def show_account_details(self, account_id):
        """Show account details"""
        account = self.find_account_by_id(account_id)
        if account:
            return str(account)
        else:
            raise ValueError("Account not found")

    def transfer_money(self, sender_id, receiver_id, amount, sender_pin):
        """Transfer money between accounts"""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        # Authenticate sender
        sender = self.authenticate(sender_id, sender_pin)
        if not sender:
            raise ValueError("Authentication failed. Invalid sender account ID or PIN.")

        # Check if receiver exists
        receiver = self.find_account_by_id(receiver_id)
        if not receiver:
            raise ValueError("Receiver account not found")

        # Check if sender and receiver are different
        if sender_id == receiver_id:
            raise ValueError("Cannot transfer to the same account")

        # Withdraw from sender
        sender.withdraw(amount)

        # Deposit to receiver
        receiver.deposit(amount)

        # Log transfer in sender's history
        sender.transactions.append({
            "date": sender.transactions[-1]["date"],  # Use the same timestamp as the withdrawal
            "type": "TRANSFER_OUT",
            "amount": amount,
            "receiver_id": receiver_id,
            "balance_after": sender.balance
        })

        # Log transfer in receiver's history
        receiver.transactions.append({
            "date": receiver.transactions[-1]["date"],  # Use the same timestamp as the deposit
            "type": "TRANSFER_IN",
            "amount": amount,
            "sender_id": sender_id,
            "balance_after": receiver.balance
        })

        return sender.balance, receiver.balance

    def change_pin(self, account_id, mobile, new_pin):
        """Change PIN for an account after verifying mobile number"""
        account = self.find_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        if account.mobile != mobile:
            raise ValueError("Mobile number does not match account details")

        account.change_pin(new_pin)
        return True

    def save_to_file(self, filename="bank.json"):
        """Save all accounts to a JSON file"""
        with open(filename, 'w') as f:
            json.dump([account.to_dict() for account in self.accounts.values()], f)
    
    def load_from_file(self, filename="bank.json"):
        """Load accounts from a JSON file"""
        try:
            with open(filename, 'r') as f:
                accounts_data = json.load(f)
                self.accounts = {data["id"]: Account.from_dict(data) for data in accounts_data}
        except FileNotFoundError:
            print("File not found. Starting with an empty bank.")

    def run(self):
        """Run the console menu for the banking system"""
        while True:
            print("\nWelcome to BankLite!")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Balance")
            print("5. View Transaction History")
            print("6. Save & Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                name = input("Enter account holder's name: ")
                initial_balance = float(input("Enter initial balance: "))
                pin = input("Set a PIN for the account: ")
                account = self.create_account(name, initial_balance, pin)
                print(f"Account created: {account}")
                input("Press Enter to return to the menu...")

            elif choice == '2':
                account_id = int(input("Enter account ID: "))
                pin = input("Enter PIN: ")
                account = self.authenticate(account_id, pin)
                if account:
                    amount = float(input("Enter amount to deposit: "))
                    new_balance = self.deposit_to_account(account_id, amount)
                    print(f"New balance: ${new_balance:.2f}")
                input("Press Enter to return to the menu...")

            elif choice == '3':
                account_id = int(input("Enter account ID: "))
                pin = input("Enter PIN: ")
                account = self.authenticate(account_id, pin)
                if account:
                    amount = float(input("Enter amount to withdraw: "))
                    new_balance = self.withdraw_from_account(account_id, amount)
                    print(f"New balance: ${new_balance:.2f}")
                input("Press Enter to return to the menu...")

            elif choice == '4':
                account_id = int(input("Enter account ID: "))
                pin = input("Enter PIN: ")
                account = self.authenticate(account_id, pin)
                if account:
                    account_details = self.show_account_details(account_id)
                    print(account_details)
                input("Press Enter to return to the menu...")

            elif choice == '5':
                account_id = int(input("Enter account ID: "))
                pin = input("Enter PIN: ")
                account = self.authenticate(account_id, pin)
                if account:
                    history = account.get_history()
                    for transaction in history:
                        print(transaction)
                input("Press Enter to return to the menu...")

            elif choice == '6':
                self.save_to_file()
                print("Data saved. Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

class BankLiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BankLite - Banking System")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")

        # Load bank data
        self.bank = Bank()
        self.bank.load_from_file()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")

        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self.root, bg="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Main frame
        self.main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(self.main_frame, text="Welcome to BankLite", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)

        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=20)

        # Buttons
        self.create_button(buttons_frame, "Create Account", self.create_account)
        self.create_button(buttons_frame, "Deposit Money", self.deposit_money)
        self.create_button(buttons_frame, "Withdraw Money", self.withdraw_money)
        self.create_button(buttons_frame, "Transfer Money", self.transfer_money)
        self.create_button(buttons_frame, "Change PIN", self.change_pin)
        self.create_button(buttons_frame, "View Balance", self.view_balance)
        self.create_button(buttons_frame, "View Transaction History", self.view_history)
        self.create_button(buttons_frame, "Save & Exit", self.save_and_exit)

        # Status label
        self.status_label = ttk.Label(self.main_frame, text="", foreground="blue")
        self.status_label.pack(pady=10)

    def create_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(fill=tk.X, pady=5)
        return button

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_account(self):
        name = simpledialog.askstring("Create Account", "Enter account holder's name:")
        if not name:
            return
        mobile = simpledialog.askstring("Create Account", "Enter mobile number:")
        if not mobile:
            return
        initial_balance = simpledialog.askfloat("Create Account", "Enter initial balance:")
        if initial_balance is None:
            return
        pin = simpledialog.askstring("Create Account", "Set a PIN for the account:")
        if not pin:
            return

        try:
            account = self.bank.create_account(name, initial_balance, pin, mobile)
            messagebox.showinfo("Success", f"Account created successfully!\n\nAccount ID: {account.id}\nMobile: {account.mobile}\nPIN: {account.pin}\n\nPlease save this information securely.")
            self.status_label.config(text=f"Account {account.id} created successfully")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def authenticate_and_get_account(self):
        account_id = simpledialog.askinteger("Authentication", "Enter account ID:")
        if account_id is None:
            return None
        pin = simpledialog.askstring("Authentication", "Enter PIN:")
        if not pin:
            return None

        account = self.bank.authenticate(account_id, pin)
        if not account:
            messagebox.showerror("Error", "Authentication failed. Invalid account ID or PIN.")
            return None
        return account

    def deposit_money(self):
        account = self.authenticate_and_get_account()
        if not account:
            return

        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is None or amount <= 0:
            messagebox.showerror("Error", "Invalid amount")
            return

        try:
            new_balance = self.bank.deposit_to_account(account.id, amount)
            messagebox.showinfo("Success", f"Deposit successful. New balance: ${new_balance:.2f}")
            self.status_label.config(text=f"Deposited ${amount:.2f} to account {account.id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def withdraw_money(self):
        account = self.authenticate_and_get_account()
        if not account:
            return

        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is None or amount <= 0:
            messagebox.showerror("Error", "Invalid amount")
            return

        try:
            new_balance = self.bank.withdraw_from_account(account.id, amount)
            messagebox.showinfo("Success", f"Withdrawal successful. New balance: ${new_balance:.2f}")
            self.status_label.config(text=f"Withdrew ${amount:.2f} from account {account.id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def transfer_money(self):
        # Get sender account details
        sender_id = simpledialog.askinteger("Transfer Money", "Enter your account ID:")
        if sender_id is None:
            return
        sender_pin = simpledialog.askstring("Transfer Money", "Enter your PIN:")
        if not sender_pin:
            return

        # Select receiver account from list
        receiver_id = self.select_account("Select Receiver Account")
        if receiver_id is None:
            return

        # Get transfer amount
        amount = simpledialog.askfloat("Transfer Money", "Enter amount to transfer:")
        if amount is None or amount <= 0:
            messagebox.showerror("Error", "Invalid amount")
            return

        try:
            sender_balance, receiver_balance = self.bank.transfer_money(sender_id, receiver_id, amount, sender_pin)
            messagebox.showinfo("Success", f"Transfer successful!\nYour new balance: ${sender_balance:.2f}\nReceiver's new balance: ${receiver_balance:.2f}")
            self.status_label.config(text=f"Transferred ${amount:.2f} from account {sender_id} to {receiver_id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def change_pin(self):
        account_id = simpledialog.askinteger("Change PIN", "Enter your account ID:")
        if account_id is None:
            return
        mobile = simpledialog.askstring("Change PIN", "Enter your registered mobile number:")
        if not mobile:
            return
        new_pin = simpledialog.askstring("Change PIN", "Enter your new PIN (at least 4 digits):")
        if not new_pin or len(new_pin) < 4:
            messagebox.showerror("Error", "PIN must be at least 4 digits")
            return

        try:
            self.bank.change_pin(account_id, mobile, new_pin)
            messagebox.showinfo("Success", "PIN changed successfully.")
            self.status_label.config(text=f"PIN changed for account {account_id}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def select_account(self, title):
        """Create a dialog to select an account from the list"""
        if not self.bank.accounts:
            messagebox.showerror("Error", "No accounts available")
            return None

        # Create a new window for account selection
        select_window = tk.Toplevel(self.root)
        select_window.title(title)
        select_window.geometry("400x300")
        select_window.configure(bg="#f0f0f0")

        ttk.Label(select_window, text="Select an account:", font=("Arial", 12)).pack(pady=10)

        # Listbox for accounts
        listbox = tk.Listbox(select_window, font=("Arial", 10), selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate listbox
        account_ids = []
        for account_id, account in self.bank.accounts.items():
            listbox.insert(tk.END, f"ID: {account_id} - {account.name}")
            account_ids.append(account_id)

        selected_id = None

        def on_select():
            nonlocal selected_id
            selection = listbox.curselection()
            if selection:
                selected_id = account_ids[selection[0]]
                select_window.destroy()

        ttk.Button(select_window, text="Select", command=on_select).pack(pady=10)

        # Wait for window to close
        select_window.wait_window()
        return selected_id

    def view_balance(self):
        account = self.authenticate_and_get_account()
        if not account:
            return

        details = self.bank.show_account_details(account.id)
        messagebox.showinfo("Account Details", details)
        self.status_label.config(text=f"Viewed balance for account {account.id}")

    def view_history(self):
        account = self.authenticate_and_get_account()
        if not account:
            return

        history = account.get_history()
        if not history:
            messagebox.showinfo("Transaction History", "No transactions found.")
            return

        history_text = "\n".join([f"{t['date']} - {t['type']}: ${t['amount']:.2f} (Balance: ${t['balance_after']:.2f})" for t in history])
        messagebox.showinfo("Transaction History", history_text)
        self.status_label.config(text=f"Viewed history for account {account.id}")

    def save_and_exit(self):
        self.bank.save_to_file()
        messagebox.showinfo("Saved", "Data saved successfully. Exiting...")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankLiteGUI(root)
    root.mainloop()
