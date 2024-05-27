# Name: Dorji Wangdi
# Section: 1EE
# Student ID Number: 02230063
################################

# REFERENCES
# https://youtu.be/BRssQPHZMrc?si=yj4pfwEDPZnl9rdZ
# https://youtu.be/xTh-ln2XhgU?si=f34gchYuo9cG_jPF
# https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/


# we need to insert external module or libraries in the code, so we use the import statement
# the random module provides the code to generate the pseudo-random numbers which we need to use in generating the account_number
import random
import os
# OS stands for Operating system which allows the code to  access various operating system-dependent functions and features like creating, deleting file and making some changes in thr working file

# Define the Account class with necessary attributes and methods
class Account: # creating a base class which consist of account_number, default_password, account_type and account balance
    # Initializing the object and values (Account object with account type and default values)
    def __init__(self, account_type):   
        self.account_number = random.randint(10000, 99999) # will generate a random number with 5 digit as a account number
        self.password = 'default_password'  # Set a initial default password
        self.account_type = account_type # Set the account type
        self.balance = 0.0  # Initialize balance to zero after making the account 

    # this method will deposit the amount and update the account
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: {amount}. New Balance: {self.balance}")

    # Method to withdraw an amount and update the account and if the account has sufficient funds the executing the if statement 
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew: {amount}. New Balance: {self.balance}")

    # Method to save account details and updated information of account to a file 
    def save_to_file(self):
        with open('accounts.txt', 'a') as file:
            file.write(f"{self.account_number},{self.password},{self.account_type},{self.balance}\n")

# Defining PersonalAccount class
# derived account from the base class (personalAccount) using inheritance 
class PersonalAccount(Account):
    def __init__(self):
        super().__init__('Personal')

# Defining BusinessAccount class
# derived account from the base class (BusinessAccount) using inheritance 
class BusinessAccount(Account):
    def __init__(self):
        super().__init__('Business')
# this is the function to create the account based on the information and account type given above
def create_account(account_type):
    account_type = account_type.capitalize() # this will capatilaze the first letter for consistency of acount type
    if account_type == 'Personal':  # will create if the user chose the personal account type 
        account = PersonalAccount()
    elif account_type == 'Business':    # will create if the user chose the business account type 
        account = BusinessAccount()
    else:   # execute if writen other than the option given by the user
        print("Invalid account type.")
        return None
    account.save_to_file() #updates in the file info.

    print(f"Account created. Number: {account.account_number}, Password: {account.password}")
    return account
    # display the account information for user

# Function to handle login using account number and password(i.e. default password)
def login(account_number, password):
    file = open('accounts.txt', 'r')     # Open the file in read mode
    for line in file:
        acc_number, acc_password, _, _ = line.strip().split(',')    #steps for the login account 
        if acc_number == account_number and acc_password == password:
            print("Login successful.")
            file.close()    # Close the file after successful login
            return True
    file.close()    # Close the file if login fails
    print("Login failed.")  # execute if couldnot login
    return False

# Function to send money from one account to another
def send_money(from_account, to_account_number, amount):
    if from_account.balance < amount:  # Check for insufficient funds and execute it 
        print("Insufficient funds.")
        return

    # Open the file in read mode and read the lines
    file = open('accounts.txt', 'r')
    accounts = file.readlines()
    file.close()  # Close the file after reading

    # Open the file in write mode to update the accounts
    file = open('accounts.txt', 'w')
    for line in accounts:   # condition for execution if account is = to balance
        acc_number, acc_password, acc_type, balance = line.strip().split(',')
        if acc_number == to_account_number: 
            updated_balance = float(balance) + amount
            line = f"{acc_number},{acc_password},{acc_type},{updated_balance}\n"
        file.write(line)
    file.close()  # Close the file after writing

    # Withdraw the amount from the sender's account
    from_account.withdraw(amount)

def delete_account(account_number):

    # Open the file in read mode and read the lines like sending money
    file = open('accounts.txt', 'r')
    accounts = file.readlines()
    file.close()  # Close the file after reading same as sending money 

    # Open the file in write mode to update the accounts
    file = open('accounts.txt', 'w')
    for line in accounts:
        if line.startswith(account_number):
            continue  # this will Skip writing the account to be deleted
        file.write(line)
    file.close()  # Close the file after writing

    print(f"Account {account_number} deleted.")
    # information updated 

# Define the main function to run the banking application
def main():
    my_account = None  # Initialize my_account to None to track the current account session

    # this will Start an infinite loop to display the menu options
    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")  # Prompt the user for their choice 

        # this is for the condition for the user to Handle the choice
        if choice == '1':
            # Creating a new account
            account_type = input("Enter account type (Personal/Business): ")
            my_account = create_account(account_type)  # Store the created account by the user in my_account

        elif choice == '2': # this is for the second choice 
            # Attempt to log in if an account has been created
            if my_account:
                account_number = input("Enter account number: ")    # user input for the account number
                password = input("Enter password: ")    # user input of password
                if login(account_number, password):
                    # Display account options if login is successful
                    while True: # after the login is true/successful, this loop will will show the options
                        print("\n1. Deposit")
                        print("2. Withdraw")
                        print("3. Send Money")
                        print("4. Delete Account")
                        print("5. Logout")
                        action = input("Enter action: ")  # Prompt for the action to perform, user input 

                        # Handle the selected action, condition for the option user chose above
                        if action == '1':
                            amount = float(input("Enter deposit amount: "))
                            my_account.deposit(amount)  # Deposit the specified amount
                        elif action == '2':
                            amount = float(input("Enter withdrawal amount: "))
                            my_account.withdraw(amount)  # Withdraw the specified amount
                        elif action == '3':
                            to_account_number = input("Enter recipient account number: ")
                            amount = float(input("Enter amount to send: "))
                            send_money(my_account, to_account_number, amount)  # Send money to another account
                        elif action == '4':
                            delete_account(account_number)  # Delete the account
                            break  # Exit the inner loop after deleting the account
                        elif action == '5':
                            break  # Log out of the account
                        else:
                            print("Invalid action.")  # Handle invalid actions
            else:   #if the account is not created this condition will exicute
                print("Please create an account first.")  # Prompt to create an account if not already done
        elif choice == '3':
            break  # Exit the application if the choice is to exit
        else:
            print("Invalid choice. Please select again.")  # exicutes if the user enters invalid choices

# Define the get_account function to retrieve an account instance using the account number
def get_account(account_number):
    file = open('accounts.txt', 'r')  # Open the accounts file in read mode
    for line in file:
        acc_number, acc_password, acc_type, balance = line.strip().split(',')
        if acc_number == account_number:
            # Check the account type and create the appropriate account instance
            if acc_type == 'Personal':
                account = PersonalAccount()
            elif acc_type == 'Business':
                account = BusinessAccount()
            # Set the account details from the file
            account.password = acc_password
            account.balance = float(balance)
            file.close()  # Close the file after finding the account
            return account  # Return the account instance
    file.close()  # Close the file if the account is not found
    return None  # Return None if the account is not found

# Call the main function to start the application
main()

