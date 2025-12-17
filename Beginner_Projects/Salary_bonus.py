#Someone wants a bonus😆
n = int(input("Enter the months?\n"))
total = 0
for i in range(1,n+1):
    bonus = int(input("Enter bonus for month {i}: "))
    total += bonus
print(f"Total Bonus : {total}")
