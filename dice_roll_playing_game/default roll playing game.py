import random


while True:
    answer = input("Roll the dice? (yes/no): ").strip().lower()
    choice = input("How many dice do you want to roll? (1 or 2): ").strip()

    if answer == "yes":
        if choice == "1":
            roll = random.randint(1, 6)
            print(f"You rolled a {roll}.")
        elif choice == "2":
            roll1 = random.randint(1, 6)
            roll2 = random.randint(1, 6)
            total = roll1 + roll2
            print(f"You rolled a {roll1} and a {roll2}. Total: {total}.")
        else:
            print("Invalid choice. Please enter 1 or 2.")
    elif answer == "no":
        print("Thanks for playing!")
        break
    else:
        print("Invalid input. Please enter yes or no.")