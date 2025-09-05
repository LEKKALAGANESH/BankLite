import json
from account import Account

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
