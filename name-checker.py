import requests
import random
import time
import itertools

# TODO: 
# ask user for regex instead of hardcoding it

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

def use_regex_pattern(regex):
    #todo
    return

def main():
    try:
        print(f" ----------------------------")
        regex = get_input(" | Use regex pattern? (yes/no): ", str, required=True).lower() == "yes"
        key = get_input(" | Max. Characters: ", int, required=True)
        use_hardcoded = get_input(" | Use hardcoded pattern? (yes/no): ", str, required=True).lower() == "yes"

        if regex:
            use_regex_pattern(regex)

        if not use_hardcoded:
            print(" | You must provide either letters or numbers to generate the pattern.")
            
            letters = ""
            numbers = ""

            while not letters and not numbers:
                letters = get_input(" | Letters (leave blank if not needed): ", str).strip()
                
                if not letters:
                    numbers_input = get_input(" | Numbers : ", str, required=True).strip()
                else:
                    numbers_input = get_input(" | Numbers (leave blank if not needed): ", str).strip()

                if numbers_input:
                    try:
                        numbers = int(numbers_input)
                    except ValueError:
                        print(" | Error: Numbers must be a valid integer.")
                        numbers = None

                if not letters and not numbers:
                    print(" | Error: You must provide either 'letters' or 'numbers'. Try again.")
        else:
            letters = ""
            numbers = ""

        pattern = get_pattern(letters, numbers, use_hardcoded, 'abcdfghijklmnopqrstuvwxyz1234567890') #change here hardcoded pattern :)
        if not pattern:
            print(" | Error: No pattern provided and hardcoded is not used. Exiting...")
            return

        print(f" | Looking for users with letters/numbers: " + pattern + " with " + str(key) + " characters max")
        while True:
            user = "".join(random.choices(pattern, k=key))
            search_user(user)
    except KeyboardInterrupt:
        print(f"\n ----------------------------")
        print("\nStopped by user.")

if __name__ == "__main__":
    main()
