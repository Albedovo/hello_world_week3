import random


def show_status(battery, distance):
    print(f"\nBattery: {battery}% | Distance home: {distance} blocks")
    print("----------------------------------------")


def roll_dice(target):
    roll = random.randint(1, 10)
    print(f"Dice roll: {roll}/10")
    print(f"You need {target} or less to succeed.")
    return roll <= target


def play_game():
    battery = 10
    distance = 3

    print("10% BATTERY: FIND YOUR WAY HOME")
    print("You are 3 blocks from home with only 10% battery.")
    print("Reach home before your battery runs out!")
    print("Arriving with exactly 0% battery still counts as a win.")

    while battery > 0 and distance > 0:
        show_status(battery, distance)
        print("1. Use GPS             | Cost: 4% | Always succeeds")
        print("2. Call for directions | Cost: 3% | Success: roll 1-8")
        print("3. Ask a stranger      | Cost: 2% | Success: roll 1-5")
        print("4. Walk randomly       | Cost: 1% | Success: roll 1-3")
        choice = input("Choose an action (1-4): ").strip()

        if choice == "1":
            cost = 4
        elif choice == "2":
            cost = 3
        elif choice == "3":
            cost = 2
        elif choice == "4":
            cost = 1
        else:
            print("Please enter 1, 2, 3, or 4.")
            continue


        if battery < cost:
            print("Not enough battery. Choose a cheaper action.")
            continue

        battery -= cost
        print(f"\nBattery used: {cost}%")

        if choice == "1":
            distance -= 1
            print("GPS shows the way. Move 1 block closer! No roll needed.")
        elif choice == "2":
            if roll_dice(8):
                distance -= 1
                print("Correct directions! Move 1 block closer.")
            else:
                distance += 1
                print("Wrong directions! Move 1 block farther away.")
        elif choice == "3":
            if roll_dice(5):
                distance -= 1
                print("Someone helps you! Move 1 block closer.")
            else:
                print("Nobody knows the way. Stay in place.")
        else:
            if roll_dice(3):
                distance -= 1
                print("Lucky choice! Move 1 block closer.")
            else:
                distance += 1
                print("Wrong turn! Move 1 block farther away.")

    show_status(battery, distance)
    if distance == 0:
        print("You made it home! YOU WIN!")
    else:
        print("Battery dead. GAME OVER!")


if __name__ == "__main__":
    play_game()
