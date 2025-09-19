print("Welcome to my Quiz Game :)")

def new_line(): #making a new function
    print("\n")


choice = input("Do you wish to continue? ") #user input
if choice.lower() != "yes":
    quit()

print("Let's move forward ^_^")
points = 0


ans = input("Who created C-Programming? ")
if ans.title() == "Dennis Ritchie":
    print("Hurray! The answer is correct")
    points +=1
else:
    print("Oops! That was incorrect.") 

    #Copy these and input the other questions

print(f"You got {points} questions correct")
