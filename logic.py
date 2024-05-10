import csv

from PyQt6.QtWidgets import *
from gui import *
from accountlogic import *


class GuiLogic(QMainWindow, Ui_yourBank):
    def __init__(self) -> None:
        """
        Set up the initial view of the GUI.
        """
        super().__init__()
        self.setupUi(self)

        self.bank_info.hide()
        self.personal_info.hide()
        self.amount_input.hide()
        self.confirm_button.hide()
        self.checking_radio.setChecked(True)

        self.withdrawal_button.clicked.connect(lambda: self.withdraw_button1())
        self.deposit_button.clicked.connect(lambda: self.deposit_button1())
        self.info_button.clicked.connect(lambda: self.info1())
        self.pushButton.clicked.connect(lambda: self.done())
        self.bank_info.clicked.connect(lambda: self.get_bank_total())
        self.personal_info.clicked.connect(lambda: self.__str__())
        self.confirm_button.clicked.connect(lambda: self.confirms())
        self.already_there: bool = False

        self.saving_names: list[str] = []
        self.checking_names: list[str] = []
        self.saving_account: list[SavingAccount] = []
        self.checking_account: list[Account] = []
        self.getaccountinfo()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def check_password(self):
        """
        Checks to see if the password input is empty.
        """
        password = self.password_input.text()
        if password.strip() == '':
            raise ValueError

    def checkCorrectPassword(self):
        """
        Checks if the password is the correct one connected to the account.
        """
        if (self.name_input.text() in self.checking_names) or (self.name_input.text() in self.saving_names):
            if self.password_input.text() != self.current_account.get_password():
                raise ValueError

    def check_name(self) -> bool:
        """
        Checks if the user inputted a valid name for an account.
        :return: (bool) True if the name is invalid, False if the name is valid.
        """
        name: str = self.name_input.text().strip()
        try:
            if name == '':
                raise ValueError
            elif name.isdecimal():
                raise TypeError
            else:
                return False
        except:
            return True

    def get_account_by_name(self, name) -> Account or SavingAccount:
        """
        Get the account by the owners name.
        :param name: (str) The name of the user on the account.
        :return: The account or None if there is no account under that name.
        """
        if self.checking_radio.isChecked():
            for account in self.checking_account:
                if account.get_name() == name:
                    return account
        else:
            for account in self.saving_account:
                if account.get_name() == name:
                    return account

    def info1(self) -> None:
        """
        Shows and allows the user to choose either bank information or personal information.
        """
        try:
            if self.check_name():
                raise ValueError
            self.check_password()
            self.success_label.clear()
            self.amount_label.clear()
            self.amount_input.clear()
            self.amount_input.hide()
            self.confirm_button.hide()
            self.name_input.setEnabled(False)
            self.password_input.setEnabled(False)
            self.checking_radio.setEnabled(False)
            self.saving_radio.setEnabled(False)
            self.info_text.setText('Click Done to return home')
            if self.checking_radio.isChecked():
                if self.name_input.text() not in self.checking_names:
                    self.current_account = Account(self.name_input.text(), password=self.password_input.text())
                    self.checking_names.append(self.name_input.text())
                    self.checking_account.append(self.current_account)
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()
            else:
                if self.name_input.text() not in self.saving_names:
                    self.current_account = SavingAccount(self.name_input.text(),password=self.password_input.text())
                    self.saving_names.append(self.name_input.text())
                    self.saving_account.append(self.current_account)
                    self.info_text.setText(
                        '$100 has been automatically deposited as per Saving Account minimum balance\n\n' + self.info_text.text())
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()

            self.bank_info.show()
            self.personal_info.show()
        except:
            self.success_label.setText('Invalid Name/Password')
            self.name_input.clear()
            self.password_input.clear()

    def get_bank_total(self) -> None:
        """
        adds together and displays the total amount of money in the bank.
        """
        try:
            total: float = 0
            for account in self.saving_account:
                total += account.get_balance()
            for account in self.checking_account:
                total += account.get_balance()
            self.bank_info_text.setText(f'Total amount of money in the bank: ${total:.2f}')
        except:
            pass

    def deposit_button1(self) -> None:
        """
        Takes the amount variable and tries to deposit it into their own account
        """

        try:
            self.name_input.setEnabled(False)
            self.password_input.setEnabled(False)
            self.checking_radio.setEnabled(False)
            self.saving_radio.setEnabled(False)
            self.info_text.setText('Click Done to return home')
            self.success_label.clear()
            self.bank_info.hide()
            self.personal_info.hide()
            self.bank_info_text.clear()
            self.personal_info_text.clear()
            self.amount_input.clear()

            if self.check_name():
                raise ValueError
            self.check_password()

            if self.checking_radio.isChecked():
                if self.name_input.text() not in self.checking_names:
                    self.current_account = Account(self.name_input.text(), password=self.password_input.text())
                    self.checking_names.append(self.name_input.text())
                    self.checking_account.append(self.current_account)
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()
            else:
                if self.name_input.text() not in self.saving_names:
                    self.current_account = SavingAccount(self.name_input.text(), password=self.password_input.text())
                    self.saving_names.append(self.name_input.text())
                    self.saving_account.append(self.current_account)
                    self.info_text.setText('$100 has been automatically deposited as per Saving Account minimum balance\n\n' + self.info_text.text())
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()

            self.amount_input.show()
            self.amount_label.setText('Amount: $')
            self.confirm_button.show()
            self.dep: bool = True
        except:
            self.success_label.setText('Invalid name/password')
            self.name_input.clear()
            self.password_input.clear()

    def withdraw_button1(self) -> None:
        """
        Takes the amount variable and tries to withdraw it from their own account.
        """
        try:
            if self.check_name():
                raise ValueError
            self.check_password()
            self.name_input.setEnabled(False)
            self.password_input.setEnabled(False)
            self.info_text.setText('Click Done to return home')
            self.success_label.clear()
            self.bank_info.hide()
            self.personal_info.hide()
            self.bank_info_text.clear()
            self.personal_info_text.clear()
            self.amount_input.clear()
            self.checking_radio.setEnabled(False)
            self.saving_radio.setEnabled(False)
            if self.checking_radio.isChecked():
                if self.name_input.text() not in self.checking_names:
                    self.current_account = Account(self.name_input.text(), password=self.password_input.text())
                    self.checking_names.append(self.name_input.text())
                    self.checking_account.append(self.current_account)
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()
            else:
                if self.name_input.text() not in self.saving_names:
                    self.current_account = SavingAccount(self.name_input.text(), password=self.password_input.text())
                    self.saving_names.append(self.name_input.text())
                    self.saving_account.append(self.current_account)
                    self.info_text.setText('$100 has been automatically deposited as per Saving Account minimum balance\n\n' + self.info_text.text())
                else:
                    self.current_account = self.get_account_by_name(self.name_input.text())
                    self.checkCorrectPassword()
            self.amount_input.show()
            self.amount_label.setText('Amount: $')
            self.confirm_button.show()
            self.dep: bool = False
        except:
            self.success_label.setText('Invalid name/password')
            self.name_input.clear()
            self.password_input.clear()


    def confirms(self) -> None:
        """
        Processes the transaction when trying to deposit or withdrawal
        """
        try:
            if self.amount_input.text() == '':
                raise ValueError
            else:
                amount: float = float(self.amount_input.text())
                if self.dep:
                    if self.current_account.deposit(amount):
                        self.success_label.setText(f'Success')
                    else:
                        self.success_label.setText('Failed to Deposit')
                else:
                    if self.current_account.withdraw(amount):
                        self.success_label.setText('Success')
                    else:
                        self.success_label.setText('Failed')
        except ValueError:
            self.success_label.setText('Invalid Amount')

    def done(self) -> None:
        """
        returns to the original UI screen.
        """
        self.bank_info.hide()
        self.personal_info.hide()
        self.amount_input.hide()
        self.confirm_button.hide()
        self.amount_label.clear()
        self.amount_input.clear()
        self.personal_info_text.clear()

        self.checking_radio.setChecked(True)
        self.saving_radio.setChecked(False)

        self.name_input.clear()
        self.password_input.clear()
        self.success_label.clear()
        self.bank_info_text.clear()
        self.info_text.clear()
        self.name_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.checking_radio.setEnabled(True)
        self.saving_radio.setEnabled(True)
        self.name_input.setFocus()

    def __str__(self) -> None:
        """
        Displays account information.
        """
        self.personal_info_text.setText(f"Account name = {self.current_account.get_name()}, Account balance = {self.current_account.get_balance():.2f}")

    def getaccountinfo(self):
        """
        Reads account info from CSV.
        """
        with open('checkaccount.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.current_account = Account(row[0], row[1], float(row[2]))
                self.checking_names.append(row[0])
                self.checking_account.append(self.current_account)
        with open('savingaccount.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                balance = max(float(row[2]), SavingAccount.minimum)  # Ensure balance is at least the minimum
                self.current_account = SavingAccount(row[0], row[1], balance, int(row[3]))
                # self.current_account = SavingAccount(row[0], row[1], int(row[3]))
                # self.current_account.set_balance((float(row[2]) - 100))
                self.saving_names.append(row[0])
                self.saving_account.append(self.current_account)
    def closeEvent(self, event):
        self.__exit__(None, None, None)
        QApplication.quit()
        event.accept()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Writes account information to CSV before exiting.
        :return:
        """
        with open('checkaccount.csv', 'w', newline='') as file:
            write = csv.writer(file)
            for account in self.checking_account:
                write.writerow([account.get_name(), account.get_password(), account.get_balance()])
        with open('savingaccount.csv', 'w', newline='') as file:
            write = csv.writer(file)
            for account in self.saving_account:
                write.writerow([account.get_name(), account.get_password(), account.get_balance(), account.get_depositcount()])