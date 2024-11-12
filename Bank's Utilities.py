import os
import getpass


class ATM:
    def __init__(self, username, pin, balance=0):
        self.username = username
        self.pin = pin
        self.balance = balance

    def register(self):
        filename = self.username + '.txt'
        if filename not in os.listdir():
            with open(filename, 'w') as file:
                file.write(self.pin + '\n')
                file.write(str(self.balance))
            print("Registration successful.")
        else:
            print("Username already exists.")

    def login(self):
        filename = self.username + '.txt'
        if filename in os.listdir():
            with open(filename, 'r') as file:
                saved_pin = file.readline().strip()
                if self.pin == saved_pin:
                    self.balance = int(file.readline().strip())
                    print("Login successful.")
                    return True
                else:
                    print("Incorrect PIN.")
                    return False
        else:
            print("User not registered. Please register first.")
            return False

    def view_statement(self):
        print(f"Your balance is: {self.balance} INR")

    def withdraw(self, amount):
        if amount % 10 != 0:
            print("Withdrawal amount must be in multiples of 10.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            print(f"Withdrawal successful. New balance: {self.balance} INR")
            self._update_balance()

    def deposit(self, amount):
        if amount % 10 != 0:
            print("Deposit amount must be in multiples of 10.")
        else:
            self.balance += amount
            print(f"Deposit successful. New balance: {self.balance} INR")
            self._update_balance()

    def change_pin(self, new_pin):
        if new_pin.isdigit() and len(new_pin) == 4 and new_pin != self.pin:
            self.pin = new_pin
            self._update_pin()
            print("PIN change successful.")
        else:
            print("New PIN must be 4 digits and different from the current PIN.")

    def _update_balance(self):
        filename = self.username + '.txt'
        with open(filename, 'w') as file:
            file.write(self.pin + '\n')
            file.write(str(self.balance))

    def _update_pin(self):
        self._update_balance()


def secure_input(prompt):
    try:
        # Attempt to use getpass, if it raises a warning, fallback to input()
        return getpass.getpass(prompt)
    except (getpass.GetPassWarning, OSError):
        # Fall back to `input` if getpass fails
        print("WARNING: Unable to hide input.")
        return input(prompt)


def main():
    print("Welcome to the ATM system!")
    while True:
        action = input("Choose an action: \n1. Register\n2. Login\n3. Exit\n")
        if action == '1':
            username = input("Enter a username: ")
            pin = secure_input("Enter a 4-digit PIN: ")
            balance = int(input("Enter initial deposit amount: "))
            if pin.isdigit() and len(pin) == 4:
                user = ATM(username, pin, balance)
                user.register()
            else:
                print("PIN must be 4 digits.")

        elif action == '2':
            username = input("Enter your username: ")
            pin = secure_input("Enter your PIN: ")
            user = ATM(username, pin)
            if user.login():
                while True:
                    print("\nATM Menu:")
                    option = input(
                        "Choose an option:\n(S)tate - View Balance\n(W)ithdraw\n(D)eposit\n(P)IN Change\n(B)ack to Main Menu\n").lower()
                    if option == 's':
                        user.view_statement()
                    elif option == 'w':
                        amount = int(input("Enter withdrawal amount: "))
                        user.withdraw(amount)
                    elif option == 'd':
                        amount = int(input("Enter deposit amount: "))
                        user.deposit(amount)
                    elif option == 'p':
                        new_pin = secure_input("Enter new PIN: ")
                        user.change_pin(new_pin)
                    elif option == 'b':
                        print("Back to Main Menu.")
                        break
                    else:
                        print("Invalid option.")
            else:
                print("Login failed.")

        elif action == '3':
            print("Exiting the ATM system. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
