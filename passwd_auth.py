password = "Hello"
attempts = 3
while attempts > 0:
    user_input = input("Enter password:\n")
    if user_input == password:
        print("Access Granted")
        break
    else:
        attempts -= 1
        print(f"Wrong password. {attempts} attempts left.")
    if attempts == 0:
        print("Access denied")

