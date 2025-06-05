import threading
import os

class Account:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.balance = float(balance)

    def check_pin(self, pin):
        return self.pin == pin

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class Bank:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.lock = threading.Lock()

    def _load_accounts(self):
        accounts = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        acc, pin, bal = parts
                        accounts[acc] = Account(acc, pin, float(bal))
        return accounts

    def _save_accounts(self, accounts):
        with open(self.filename, "w") as f:
            for acc in accounts.values():
                f.write(f"{acc.account_number},{acc.pin},{acc.balance}\n")

    def authenticate(self, account_number, pin):
        with self.lock:
           accounts = self._load_accounts()
        account = accounts.get(account_number)
        if account and account.check_pin(pin):
                return account
        return None

    def create_account(self, account_number, pin, initial_balance=0):
        with self.lock:
            accounts = self._load_accounts()
            if account_number in accounts:
                return False
            accounts[account_number] = Account(account_number, pin, initial_balance)
            self._save_accounts(accounts)
            return True

    def deposit(self, account_number, amount):
        with self.lock:
            accounts = self._load_accounts()
            account = accounts.get(account_number)
            if account and account.deposit(amount):
                self._save_accounts(accounts)
                return True
        return False

    def withdraw(self, account_number, amount):
        with self.lock:
            accounts = self._load_accounts()
            account = accounts.get(account_number)
            if account and account.withdraw(amount):
                self._save_accounts(accounts)
                return True
        return False

    def get_account_balance(self, account_number, pin):
        with self.lock:
            accounts = self._load_accounts()
            account = accounts.get(account_number)
            if account and account.check_pin(pin):
                return account.get_balance()
        return None
    
