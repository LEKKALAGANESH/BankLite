import json
from datetime import datetime

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
