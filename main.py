import threading
import random
import time
import os

NUM_HORSES = 1
RACE_LENGTH = 30
HORSE_DISTANCE = 3

def update_horse(i, mutex, start_time, shared_data):
    while shared_data["horses"][i] < RACE_LENGTH:
        mutex.acquire()
        shared_data["horses"][i] += HORSE_DISTANCE
        if shared_data["horses"][i] == RACE_LENGTH and not shared_data["winner"]:
            shared_data["winner"] = i
        mutex.release()
        time.sleep(random.uniform(0, 1.75))
        shared_data["graphics"][i] += ("-> ")
    shared_data["horses_done"][i] = time.time() - start_time

def print_race(shared_data):
    # Track when display is done
    local_done = False

    while not local_done:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        print("Horse:")
        for i in range(len(shared_data["graphics"])):
            print(f"{i+1} | {shared_data["graphics"][i]}", end="")
            
            # Print finish line by adding spaces between position and finish line
            distance_from_end = RACE_LENGTH - shared_data["horses"][i]
            print(" " * distance_from_end, end = "")
            if shared_data["horses_done"][i]:
                print(f" |*| ", end = "")
                if shared_data["winner"] == i:
                    print(f"Horse {i + 1} wins in {shared_data["horses_done"][i]:.2f}s!", end = "")
                else:
                    print(f"Done in {shared_data["horses_done"][i]:.2f}s.", end = "")
            else:
                print(" " * HORSE_DISTANCE, end ="")
                print(" | | ", end = "")
            print()
        if all(shared_data["horses_done"]):
            local_done = True
        time.sleep(0.3)

def place_bet(betting_balance):
    horse = input(f"Enter the horse you wish to bet on (1-{NUM_HORSES}): ")
    if int(horse) not in range(1, NUM_HORSES + 1):
        return False
    bet = input("Enter the amount you wish to bet: ")
    if not bet.isdigit() or int(bet) > betting_balance[0]:
        print(bet, betting_balance[0])
        return False
    betting_balance[1] = (int(horse), int(bet))  # Save bet
    return True

def menu(betting_balance):
    while True:
        print(f"Current balance: ${betting_balance[0]}")
        print()
        print("Menu:")
        print("1. Bet on a horse")
        print("2. Start Race ($0 bet)")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            bet_confirmed = place_bet(betting_balance)
            if bet_confirmed:
                winner = start_race()
                if winner == betting_balance[1][0] - 1:
                    print(f"You won by betting on horse {betting_balance[1][0]}!")
                    betting_balance[0] += betting_balance[1][1] 
                else:
                    print("You lose!")
                    betting_balance[0] -= betting_balance[1][1]
            else:
                print("Bet invalid, try again")
                continue
        elif choice == "2":
            start_race()
        elif choice == "3":
            break
        else:
            print("Invalid choice")

def start_race():
    shared_data = {
        "horses": [0] * NUM_HORSES,
        "graphics": [""] * NUM_HORSES,
        "bets": [0] * NUM_HORSES,
        "horses_done": [None] * NUM_HORSES,
        "finished": False,
        "winner": None,
        }
    mutex = threading.Lock()
    threads = []
    start_time = time.time()
    for i in range(NUM_HORSES):
        t = threading.Thread(target=update_horse, args=(i, mutex, start_time, shared_data))
        threads.append(t)
        t.start()

    print_thread = threading.Thread(target=print_race, args=(shared_data,))
    print_thread.start()

    for t in threads:
        t.join()

    shared_data["finished"] = True
    time.sleep(2)
    print_thread.join()
    return shared_data["winner"]

def main():
    betting_balance = [100, (0, 0)] # [balance, (horse, bet)]
    menu(betting_balance)
    print("Thanks for playing!")
    
if __name__ == "__main__":
    main()
