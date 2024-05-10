class Account():
    def __init__(self, name, password, balance=0):
        '''
        creates the initial account with the name and balance.
        :param name (str): name of the account owner.
        :param password (str): Password for the account
        :param balance (float): balance on the account, initially it is 0 because it was just opened.
        '''
        self.__account_name: str = name
        self.__account_balance: float = balance
        self.__account_password: str = password
        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        '''
        Deposits the amount into the account.
        :param amount (float): The amount wanting to be deposited.
        :return: bool: True if the money was deposited. False if it wasn't deposited.
        '''
        if amount > 0:
            self.__account_balance += amount
            return True
        else:
            return False

    def get_password(self) -> str:
        """
        Returns the password associated with the account.
        :return: str: Password for the account.
        """
        return self.__account_password

    def withdraw(self, amount: float) -> bool:
        '''
        Withdraws the amount from the account.
        :param amount (float): The amount that is wanting to be withdrawn.
        :return: bool: True if it was able to take the amount out of the account. False if it failed to withdraw the
        amount.
        '''
        if (amount > 0) and (self.get_balance() >= amount):
            self.__account_balance -= amount
            return True
        else:
            return False

    def get_balance(self) -> float:
        '''
        Returns the balance of the account.
        :return: float: the balance of the account.
        '''
        return self.__account_balance

    def get_name(self) -> str:
        '''
        Returns the name on the account.
        :return: str: the name on the account.
        '''
        return self.__account_name

    def set_balance(self, value: float) -> None:
        '''
        Sets the balance of the account as long as it is above 0.
        :param value (float): Amount that is wanting to be set on the account.
        '''
        if value >= 0:
            self.__account_balance = value
        else:
            self.__account_balance = 0

    def set_name(self, value: str) -> None:
        '''
        Sets the name of the account holder to the account.
        :param value (str): The name wanting to be put on the account.
        '''
        self.__account_name = value

    def __str__(self) -> str:
        '''
        returns a string showing the name on the account and the balance associated with it.
        :return: (str): a string with the name of the account and the balance.
        '''
        return f"Account name = {Account.get_name(self)}, Account balance = {Account.get_balance(self):.2f}"

class SavingAccount(Account):
    minimum: float = 100
    rate: float = 0.02
    def __init__(self, name: str, password: str, balance: float = 100, deposit: int = 0):
        '''
        Creates a saving account with the name, minimum account balance, and a track of the deposit count.
        :param name: (str): The name on the account.
        :param password: (str): The password on the account.
        :param balance: (float): The balance associated with the account.
        :param deposit: (int): The number of deposits on an account. Default is 0.
        '''
        super().__init__(name, password, balance)
        self.set_balance(self.minimum)
        self.__deposit_count: int = deposit

    def apply_interest(self) -> None:
        '''
        Applies interest for every fifth deposit into the account.
        '''
        if (self.__deposit_count % 5 == 0) and (self.__deposit_count != 0):
            interest_money: float = Account.get_balance(self) * self.rate
            Account.deposit(self,interest_money)

    def deposit(self, amount: float) -> bool:
        '''
        Deposits the amount into the account, adds one to the deposit count, and check to see if interest can be
        applied.
        :param amount: (float): Amount being deposited
        :return: bool: True if the amount was deposited. False if the deposit failed.
        '''
        if Account.deposit(self, amount):
            self.__deposit_count += 1
            self.apply_interest()
            return True
        else:
            return False

    def withdraw(self, amount: float) -> bool:
        '''
        Withdraws the amount from the account.
        :param amount: (float): The amount being withdrawn.
        :return: bool: True if the amount was successfully withdrawn. False if it failed to be withdrawn.
        '''
        if (amount > 0) and (self.get_balance() - amount >= self.minimum):
            Account.withdraw(self, amount)
            return True
        else:
            return False


    def set_balance(self, value: float) -> None:
        '''
        Sets the balance of the saving account to the specified value, as long as it is above the minimum value.
        :param value: (float): The new balance for the account.
        '''
        if value > self.minimum:
            self.__account_balance = value
        else:
            self.__account_balance = self.minimum

    def get_depositcount(self) -> int:
        """
        Returns the number of deposits on the account.
        :return: (int): Number of deposits.
        """
        return self.__deposit_count

    def __str__(self) -> str:
        '''
        Returns a string showing the account name and amount under the saving account.
        :return: str: Representing the name and value under the saving account.
        '''
        return 'Saving Account: ' + Account.__str__(self)