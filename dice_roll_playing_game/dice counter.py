import random


# Track the number of successful dice-rolling turns during this session.
roll_count = 0

while True:
    answer = input("Roll the dice? (yes/no): ").strip().lower()

    if answer == "yes":
        choice = input("How many dice do you want to roll? (1 or 2): ").strip()
        if choice == "1":
            roll = random.randint(1, 6)
            print(f"You rolled a {roll}.")
            roll_count += 1
        elif choice == "2":
            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            total = roll1 + roll2
            print(f"You rolled a {roll1} and a {roll2}. Total: {total}.")
            roll_count += 1
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue
        print(f"You have rolled the dice {roll_count} time(s) this session.")
    elif answer == "no":
        print(f"Thanks for playing! You rolled the dice {roll_count} time(s).")
        break
    else:
        print("Invalid input. Please enter yes or no.")