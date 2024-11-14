import requests
import random
import time

def get_input(prompt, expected_type):
    try:
        value = expected_type(input(prompt))
        return value
    except ValueError:
        print(f"Invalid input. Please enter a {expected_type.__name__}.")
        return get_input(prompt, expected_type)

key = get_input("max number of characters: ", int)
letters = get_input("letters: ", str)
numbers = get_input("numbers: ", int)

pattern = letters + str(numbers)
regex_pattern = '' # put your regex here!

def search_user(user):
    with open("available.txt", "r+") as file, open("takens.txt", "r+") as file2:
        #file.seek(0)
        content = file.read()
        content2 = file2.read()
        
        if user not in content or content2:
            response = requests.get(f"https://www.github.com/{user}/")

            if response.status_code == 200:
                print(f"taken: {user}")
                file2.write(user + "\n")     
            
            elif response.status_code == 404:
                print(f"available: {user}")
                file.write(user + "\n")     
            else:
                print("blocked from github")

while True:
    user = ""
    # change pattern var for regex if needed ;)
    for character in random.choices(pattern, k=key):
        user = user + character

    search_user(user)
