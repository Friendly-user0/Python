
#User and Machine Initilization Phase
while True:
    print("Welcome to our ATM :) \n")
    user = input("Do you wish to proceed the interaction with the ATM? \n")
    if user.lower() != "yes":
        quit("Thank you for visiting.")
    print("\nPlease wait a few seconds...\n")

#Authentication 

    password = "Hello"
    attempts = 3
    while attempts > 0:
        user_input = input("Enter password:\n")
        if user_input == password:
            print("""Welcome User.
                  How would you want to proceed?\n""")
            break
        else:
         attempts -= 1
        print(f"Wrong password. {attempts} attempts left.")
        if attempts == 0:
            print("Access denied")

# ATM Functionality

    balance = 100
    print("1. Check balance\n 2. Deposit\n 3. Withdraw\n 4. Exit")
    choice = input("Enter Choice:")
    if choice == "1":
        print("\nBalance: ",balance)
    elif choice == "2":
        amount = int(input("\nEnter amount:"))
        balance += amount
    elif choice =="3":
        amount = int(input("\nEnter amount:"))
        if amount <= balance:
            balance -= amount
        else:
            print("Insufficent funds")
    elif choice == "4":
                print("Thank you for visiting.")
                break
    else:
        print("\nInvalid Choice")
