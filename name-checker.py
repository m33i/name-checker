import requests
import random
import time
import itertools
import re
import random

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

def get_regex_pattern():
    while True:
        print("\n | Please enter your regex pattern.")
        print(" | Example: ^[A-Za-z]{2,25}$ (2-25 letters)")
        print(" | Example: ^[A-Za-z\\s]{2,30}$ (2-30 letters with spaces allowed)")
        pattern = input(" | > Enter regex pattern (or press Enter to use default): ").strip()
        
        if not pattern:
            pattern = "^[A-Za-z]{2,25}$"  # Default pattern
        
        try:
            re.compile(pattern)
            return pattern
        except re.error:
            print(" | Invalid regex pattern. Please try again.")
            print(f" ----------------------------------")

def search_user(user, regex_pattern=None):
    if not (regex_pattern and not re.match(regex_pattern, user)):
        return
    
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
                print(f" ----------------------------------")
                print(f" | > Available: {user}")
                file.write(user + "\n")

            else:
                print(f" ----------------------------------")
                print(f" | > Blocked by github... waiting 10 secs...")
                time.sleep(10)

def get_name_structure():
    print(f" ----------------------------------")
    print(" | > Special characters:")
    print(" | -- '{L}' for random letters (a-z)")   
    print(" | -- '{N}' for random numbers (0-9)")
    print(" | -- '{A}' for random alphanumeric (a-z, 0-9)")
    print(" | -- '{S}' for random symbols (!@#$%^&*)")
    print(f" ----------------------------------")
    print(" | > Examples:")
    print(" | -- 0x{L}{L}{L} -> 0xabc, 0xdef, etc.")
    print(" | -- {N}{N}{L}{L} -> 12ab, 34cd, etc.")
    print(" | -- test{L}{N} -> testa1, testb2, etc.")
    print(" | -- {A}{A}{A} -> a1b, 2c3, etc.")
    print(" | -- {S}{S}{L} -> !@a, #$b, etc.")
    print(f" ----------------------------------")

    structure = input(" | > Enter name structure: ").strip()
    if not structure:
        print(" | Structure cannot be empty")
        print(f" ---------------------------------- ")
        return get_name_structure()
    return structure

def generate_name_from_structure(structure):
    result = []
    i = 0
    while i < len(structure):
        if structure[i:i+3] == '{L}':
            result.append(random.choice('abcdefghijklmnopqrstuvwxyz'))
            i += 3
        elif structure[i:i+3] == '{N}':
            result.append(random.choice('0123456789'))
            i += 3
        elif structure[i:i+3] == '{A}':
            result.append(random.choice('abcdefghijklmnopqrstuvwxyz0123456789'))
            i += 3
        elif structure[i:i+3] == '{S}':
            result.append(random.choice('!@#$%^&*'))
            i += 3
        else:
            result.append(structure[i])
            i += 1
    return ''.join(result)

def main():
    try:
        print(f" ----------------------------------")
        use_regex = get_input(" | > Use regex pattern? (yes/no): ", str, required=True).lower() == "yes"
        
        regex_pattern = None
        if use_regex:
            regex_pattern = get_regex_pattern()
            print(f" | Using regex pattern: {regex_pattern}")
        
        print(f" ----------------------------------")
        use_structure = get_input(" | > Use structure? (yes/no): ", str, required=True).lower() == "yes"
        
        if use_structure:
            name_structure = get_name_structure()
            print(f" ----------------------------------")
            print(f" | Looking for users with structure: {name_structure}")
            while True:
                generated_name = generate_name_from_structure(name_structure)
                search_user(generated_name, regex_pattern)
                time.sleep(0.5)
        else:
            key = get_input(" | Max. Characters: ", int, required=True)
            if key <= 0 or key > 39:  # GitHub username length limit
                print(" | Invalid length. Using default max length of 39")
                key = 39
                
            pattern = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            
            print(f" | Looking for random users with {key} characters max")
            while True:
                user = "".join(random.choices(pattern, k=key))
                search_user(user, regex_pattern)

    except KeyboardInterrupt:
        print(f"\n ----------------------------------")
        print(" | Stopped by user.")

if __name__ == "__main__":
    main()
