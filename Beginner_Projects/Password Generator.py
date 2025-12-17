
import random 
import string

def generation(min_length, numbers=True, special_characters=True):  #taking necessary parameters
    letters = string.ascii_letters #alphabet
    digits = string.digits         #numbers
    special = string.punctuation   #special characters
    print("\n")
    characters = letters
    if numbers:
        characters += digits
    if special_characters:
        characters += special

    passwd = ""
    req = False
    req_num = False
    req_special = False
    while not req or len(passwd) < min_length:
        new_char = random.choice(characters)
        passwd += new_char

        if new_char in digits:
            req_num = True
        elif new_char in special:
            req_special = True

        req = True
        if numbers:
            req = req_num
        if special_characters:
            req = req and req_special
    return passwd
min_lenght = int(input("ENter the length: "))
req_num = input("Want numbers?").lower == "yes"
req_special = input("want specials ").lower() == "yes"
passwd = generation(min_lenght, req_num, req_special)
print(passwd)
