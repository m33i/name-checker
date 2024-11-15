import requests
import random
import time
import itertools

# TODO: 
# main function / organzie code
# create function for hardcoding inputs blabla
# ask user for regex instead of hardcoding it
# !!!!! show the user what characters / pattern is using to generate the usernames before "Lurking" !!!!

def get_input(prompt, expected_type, required=False):
    user_input = input(prompt)
    
    if required and user_input == "":
        print(" | This field cannot be empty. Please enter a value.")
        return get_input(prompt, expected_type, required)

    if user_input == "":
        return " "

    try:
        return expected_type(user_input)
    except ValueError:
        print(f" | Invalid input. Please enter a {expected_type.__name__}.")
        return get_input(prompt, expected_type, required)

def get_pattern(letters, numbers, use_hardcoded, hardcoded):
    if use_hardcoded:
        return hardcoded
    elif letters or numbers:
        return letters + str(numbers)
    else:
        return ""

def search_user(user):
    with open("saved/available.txt", "r+") as file, open("saved/taken.txt", "r+") as file2:
        #file.seek(0)
        content = file.read()
        content2 = file2.read()

        if user not in content or content2:
            dots = itertools.cycle(["  ", ".  ", ".. ", "...", "  "])
            response = requests.get(f"https://www.github.com/{user}/")

            if response.status_code == 200:
                for _ in range(10): 
                    print(f" | > Lurking ", end="")
                    print(next(dots), end="\r", flush=True)
                    time.sleep(0.2)

                # print(f" | > Taken: {user}")
                file2.write(user + "\n")

            elif response.status_code == 404:
                print(f" ----------------------------")
                print(f" | > Available: {user}")
                file.write(user + "\n")

            else:
                print(f"-----------------------------")
                print(f" | > Blocked by github... waiting 10 secs...")
                time.sleep(10)
        
def main():
    print(f" ----------------------------")
    key = get_input(" | Max. Characters: ", int, required=True)
    letters = get_input(" | Letters: ", str)
    numbers = get_input(" | Numbers: ", int)
    use_hardcoded = get_input(" | Use hardcoded pattern? (yes/no): ", str, required=True).lower() == "yes"
    
    if not use_hardcoded:
        letters = get_input(" | Letters: ", str)
        numbers = get_input(" | Numbers: ", int)    
    else:
        letters = ""
        numbers = ""
        
    pattern = get_pattern(letters, numbers, use_hardcoded, 'abcdfghijklmnopqrstuvwxyz1234567890')
            
    if not pattern:
        print(" | Error: No pattern provided and hardcoded is not used. Exiting...")
        return
    
    try:
        while True:
            user = "".join(random.choices(pattern, k=key))
            search_user(user)
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    main()
