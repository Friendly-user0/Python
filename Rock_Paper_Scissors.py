import random

# Keep scores outside so they are not reset every round
user_points = 0
computer_points = 0

# Function to get choices from player and computer
def choices():
    human_choose = input("Enter your choice (rock, paper, scissor):\n").lower()
    options = ["rock", "paper", "scissor"]
    bot_choice = random.choice(options)
    return {"player": human_choose, "computer": bot_choice}

# Function to decide winner and update scores
def winner(player, computer):
    global user_points, computer_points  # Use the global score variables

    print(f"You choose {player} | Computer choose {computer}")

    if player == computer:
        print("It's a tie!")
    
    elif player == "rock":
        if computer == "scissor":
            print("Rock smashes scissors.")
            user_points += 1
        else:
            print("Paper covers rock.")
            computer_points += 1
    
    elif player == "paper":
        if computer == "rock":
            print("Paper covers rock.")
            user_points += 1
        else:
            print("Scissor cuts paper.")
            computer_points += 1
    
    elif player == "scissor":
        if computer == "paper":
            print("Scissor cuts paper.")
            user_points += 1
        else:
            print("Rock smashes scissor.")
            computer_points += 1
    else:
        print("Invalid choice! No points awarded.")

    # Show current score after each round
    print("You won " + str(user_points) + " | Computer wins " + str(computer_points) + ".")
    print("-" * 30)  # separator for readability

# Main game loop
for _ in range(3):  # Play 3 rounds (change this number if you want more)
    get_choices = choices()
    winner(get_choices["player"], get_choices["computer"])

# Final result
print("Final Score -> You: " + str(user_points) + " | Computer: " + str(computer_points))
if user_points > computer_points:
    print("🎉 You are the overall winner!")
elif computer_points > user_points:
    print("💻 Computer wins the game!")
else:
    print("🤝 It's an overall tie!")
