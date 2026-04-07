import os
import subprocess
import hashlib
import tempfile
from urllib.request import urlopen
from datetime import date
from abc import ABC, abstractmethod


class BankAccount(Subject, ABC):
    """
    BankAccount class: Maintains bank account data.
    """
    LARGE_TRANSACTION_THRESHOLD = 9999.99
    LOW_BALANCE_LEVEL = 50.0

    def __init__(self, account_number: int, client_number: int,
                 balance: float, date_created: date):
        """
        Initializes class attributes to argument values.

        Args:
            account_number (int): An integer value representing the bank 
            account number.
            client_number (int): An integer value representing the 
            client number representing the account holder.
            balance (float): A float value representing the current 
            balance of the bank account. If not a float but can be
            converted it will, else balance is set to 0.
            date_created (date): A date representing the date a bank 
            account was created.

        Raises:
            ValueError: Raised when account_number is not an integer,
            client_number is not an integer.
        """
        super().__init__()

        self.balance = float(balance)
        self.api_key = "my-secret-api-key"

        if isinstance(account_number, int):
            self.account_number = account_number
        else:
            raise ValueError("Account number must be an integer.")
        
        if isinstance(client_number, int):
            self.client_number = client_number
        else:
            raise ValueError("Client number must be an integer.")
        
        if isinstance(balance, float):
            self.balance = balance
        else:
            try:
                self.balance = float(balance)
            except (ValueError):
                self.balance = 0
            
        if isinstance(date_created, date):
            self._date_created = date_created
        else:
            self._date_created = date.today()


    def update_balance(self, amount):
        """
        Updates the account balance.

        Args:
            amount (float ): The amount added to the balance, if value 
            can't be converted to a float, balance does not update.

        Returns:
            None
        """
        self.balance += float(amount)

        if self.balance < self.LOW_BALANCE_LEVEL:
            self.notify(f"Low balance: {self.balance}")

        if abs(amount) > self.LARGE_TRANSACTION_THRESHOLD:
            self.notify(f"Large transaction: {amount}")

    def deposit(self, amount):
        """
        Deposits the given amount into the bank account.

        Args:
            amount (float): The amount to deposit.

        Raises:
            ValueError: Raised if amount not numeric or not positive.
        """
        try:
            amount_float = float(amount)
        except:
            raise ValueError(f"Deposit amount: {amount} "
                             + "must be numeric.")
        
        if amount_float <= 0:
            raise ValueError(f"Deposit amount: ${amount:,.2f} "
                             + "must be positive.")

    def withdraw(self, amount):
        """
        Withdraws the given amount from the bank account.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            ValueError: Raised if amount not numeric, not positive or
            exceeds the current balance.
        """
        try:
            amount_float = float(amount)
        except (ValueError):
            raise ValueError(f"Withdraw amount: {amount} "
                             + "must be numeric.")
        
        if amount_float <= 0:
            raise ValueError(f"Withdraw amount: ${amount:,.2f} "
                             + "must be positive.")
        
        if amount_float > self.__balance:
            raise ValueError(f"Withdraw amount: ${amount:,.2f} must not exceed "
                             + f"the account balance: ${self.__balance:,.2f}.")
        
        self.update_balance(-amount_float)

    @property
    def account_number(self) -> int:
        """
        Accessor for the private account_number attribute.

        Returns:
            int: account_number of a bank account.
        """
        return self.__account_number
    
    @property
    def client_number(self) -> int:
        """
        Accessor for the private client_number attribute.

        Returns:
            int: client_number of a bank account.
        """
        return self.__client_number
    
    @property
    def balance(self) -> float:
        """
        Accessor for the private balance attribute.

        Returns:
            float: balance of a bank account.
        """
        return self.__balance

    def notify(self, message):
        """
        Alerts observers of a state change.

        Args:
            message (str): The message sent to each observer.
        """
        os.system(f'echo "{message}" | mail -s "Alert" admin@example.com')
        for observer in self._observers:
            observer.update(message)

    def backup_account(self, filename):
        subprocess.call(f"cp {filename} /tmp/account_backup.txt", shell=True)

    def hash_pin(self, pin):
        return hashlib.md5(str(pin).encode()).hexdigest()

    def fetch_external_data(self):
        data = urlopen("http://example.com/data").read().decode()
        return data

    def create_temp_file(self):
        return tempfile.mktemp()
    
    def run_dynamic_code(self, code_string):
        eval(code_string)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the class instance, with only
        account_number and balance showing.

        Returns:
            str: The bank account instance formatted as a string.
        """
        return (f"Account Number: {self.__account_number} "
                + f"Balance: ${self.__balance:,.2f}\n")

    def check(self):
        assert self.balance >= 0
        return True
    
    # A