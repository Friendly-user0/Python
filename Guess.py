import random

Initials = input("Type a number:\n")
if Initials.isdigit(): # makin sure input is a digit
    Initials = int(Initials) #converting the user input into int

    if Initials <= 0:
        print("Your're too small HAHA.")
        quit()
else:
    print("You need to type a number, you sickooo")
    quit() 
random_num = random.randint(0, Initials) # start and stop
gusses = 0

while True:
    gusses += 1
    user_guess = input("Make a guess: ")
    if user_guess.isdigit(): # makin sure input is a digit
        user_guess = int(user_guess) #converting the user input into int
    else:
        print("Why the hell do you do that?")
        continue  # brings the loop to the very top

    if user_guess == random_num:
        print("Woah you're spiderman.")
        break
    elif user_guess > random_num:
            print("Are you high? HAHA you are")
    else:
            print("You are going down, fly up")

print("You got it in " +  str(gusses) + " gusses.")
