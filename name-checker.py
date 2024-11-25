import requests
import random
import time
import itertools
import exrex

LETTERS = "[a-z]"
NUMBERS = "[0-9]"
ALPHANUMERIC = "[a-z0-9]"
# SYMBOLS = "[!@#$%^&*]" Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen.

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

def search_user(user):
    with open("saved/available.txt", "r+") as file, open("saved/taken.txt", "r+") as file2:
        #file.seek(0)
        content = file.read()
        content2 = file2.read()
        # print(f" user tried : {user}") debug
        if user not in content or user not in content2:
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
    print(" | -- '[L]' for random letters (a-z)")   
    print(" | -- '[N]' for random numbers (0-9)")
    print(" | -- '[A]' for random alphanumeric (a-z, 0-9)")
    # print(" | -- '[S]' for random symbols (!@#$%^&*)")
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
        if structure[i] == '[':
            end_brace = structure.find(']', i)
            if end_brace == -1:
                raise ValueError("Unmatched ']' in structure")
            
            token = structure[i+1:end_brace]
            for char in token:
                if char == 'L':
                    result.append(next(exrex.generate(LETTERS)))
                elif char == 'N':
                    result.append(next(exrex.generate(NUMBERS)))
                elif char == 'A':
                    result.append(next(exrex.generate(ALPHANUMERIC)))
                # elif char == 'S':
                #     result.append(next(exrex.generate(SYMBOLS)))
                else:
                    raise ValueError(f"Unknown token '{char}' in structure")
            i = end_brace + 1
        else:
            result.append(structure[i])
            i += 1
    return ''.join(result)

def get_random_name(max_length=None):
    if max_length is None:
        max_length = 25
    regex = f"^[a-z0-9]{{2,{max_length}}}$"
    generated_list = list(exrex.generate(regex))
    return random.choice(generated_list) # DEFAULT_REGEX = "^[a-z0-9]{2,25}$"

def main():
    try:
        use_structure = get_input(" | > Use structure? (yes/no): ", str, required=True).lower() == "yes"
        
        if use_structure:
            name_structure = get_name_structure()
            print(f" ----------------------------------")
            print(f" | Looking for users with structure: {name_structure}")
            while True:
                generated_name = generate_name_from_structure(name_structure)
                search_user(generated_name)
                time.sleep(0.5)
        else:
            max_length_input = get_input(" | > Enter maximum length for random names: ", str, required=False)
            max_length = int(max_length_input) if max_length_input.strip() else None
            print(f" | Looking for users with default regex ^[a-z0-9]{{2,{max_length}}}$")
            while True:
                generated_name_rex = get_random_name(max_length)
                search_user(generated_name_rex)
                time.sleep(0.5)

    except KeyboardInterrupt:
        print(f"\n ----------------------------------")
        print(" | Stopped by user.")
        print(f" ----------------------------------")

if __name__ == "__main__":
    main()
