import threading
import random
import time
import os

NUM_HORSES = 5

shared_data = {
        "horses": [0] * NUM_HORSES,
        "graphics": [""] * NUM_HORSES,
        "bets": [0] * NUM_HORSES,
        "horses_done": [False] * NUM_HORSES,
        "finished": False,
        "winner": None,
        }

def update_horse(i, mutex):
    while shared_data["horses"][i] < 20:
        mutex.acquire()
        shared_data["horses"][i] += 2
        mutex.release()
        time.sleep(random.uniform(0.25, 1.5))
       # print(f"Horse {i} is at {shared_data['horses'][i]}")
        shared_data["graphics"][i] += ("-> ")
    shared_data["horses_done"][i] = True
    if not shared_data["winner"]:
        shared_data["winner"] = i

def print_race(shared_data):
    # Track when display is done
    local_done = False

    while not local_done:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        print("Horse:")
        for i in range(len(shared_data["graphics"])):
            print(f"{i} | {shared_data["graphics"][i]}", end="")
            if shared_data["horses_done"][i]:
                print(f" ** ", end = "")
            if shared_data["winner"] == i:
                print(f"Horse {i + 1} wins! ", end = "")
            print()
        if all(shared_data["horses_done"]):
            local_done = True
        time.sleep(0.3)



def main():
    mutex = threading.Lock()
    threads = []
    for i in range(NUM_HORSES):
        t = threading.Thread(target=update_horse, args=(i, mutex))
        threads.append(t)
        t.start()

    print_thread = threading.Thread(target=print_race, args=(shared_data,))
    print_thread.start()

    for t in threads:
        t.join()

    shared_data["finished"] = True
    time.sleep(2)
    print_thread.join()


if __name__ == "__main__":
    main()
