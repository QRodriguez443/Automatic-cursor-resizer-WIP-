import pywinauto.keyboard as keyboard
import pyperclip
import random
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# An attempt to better obscure the vision of the password and increase security in the event an attacker uses a keylogger

def has_two_digits(n):
    """
    Checks if an integer has exactly two distinct digits.
    
    Args:
        n (int): The integer to check.
        
    Returns:
        bool: True if the integer has exactly two distinct digits, False otherwise.
    """
    # Convert the integer to a string to access its digits
    try:    
        digits = set(str(abs(n)))
        
    except TypeError as e:
        digits = set(str(abs(int(n))))
    
    # Check if the set of digits has exactly 2 elements
    return len(digits) == 2

def contains_number(input_str):
    """
    Checks if an integer is present within a string and returns it.
    
    Args:
        input_str (str): The string to check.
        
    Returns:
        int: The first integer found in the string, or None if no integer is present.
    """
    current_num = ''
    try:
        for char in input_str:
            if char in '0123456789':
                current_num += char
            elif current_num:
                return int(current_num)
    except TypeError as e:
        return input_str
    
    return int(current_num) if current_num else None

# For every character copied, (an) extra random character(s) is/are added
def copy_paste(array: list):

    print(array)
    pyperclip.copy(array)
    keyboard.send_keys('^v')
 
    int_rand = random.randrange(0, 9)
    chosen_chars = []

    chosen_chars = random.choices(shuffle_abc, k=int_rand)
    absstr = ''.join(chosen_chars)
    pyperclip.copy(absstr)

prev_num = None
prev_prev_value = None
u_triggered = False
not_int_triggered = False
double_digit_triggered = False
iterations = 0

abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' '!', '@', '#', '$', '%', '^', '&', '*'])
shuffle_abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' '!', '@', '#', '$', '%', '^', '&', '*'])

random.shuffle(shuffle_abc)
characters = [] # User's password is appended into the array one by one

user_pass = os.environ.get('USER_PASS') # User's created password
for j, i in enumerate(user_pass): # Organize and separate each character into the array
    print(i)
    if iterations == 2: # After the second iteration, store every previous, previous value of i (i - 2)
        ind = user_pass.index(i)  
        try:
            prev_prev_value = int(characters[ind - 2])
        except ValueError as e:
            prev_prev_value = int(characters[ind - 3])

        print("prevprevnum:", prev_prev_value)

    if iterations != 2:
        iterations += 1
    try:
        if prev_num is not None and has_two_digits(prev_num) is False:
            if prev_num != '0' and i != "u": # Handles double digits
                int(prev_num)
                if int(i):
                    print("There were 2 numbers")  
                    characters.remove(int(prev_num))  
                    double_digit_int = prev_num + i # combine the string of 2 individual nums
                    characters.append(int(double_digit_int)) # append the string of 2 as a whole integer
                    prev_num = int(double_digit_int) # To ensure proper functionality if user adds 'u' in front of double-digit
                    continue # Skip iteration so as not to duplicate the current number to the list
        
        print("prev_num set")    
        if i != " " and i != "u":
            prev_num = i
        num = int(i)
        characters.append(num)
        double_digit_triggered = False

    except ValueError as e:
        ind1 = user_pass.index(i)
        if i == 'u':
            print("Entered u")
            integer = contains_number(characters[ind1 - 1])
            print("This is why i == prev_num: ", prev_prev_value, integer)
            if prev_prev_value == integer:
                print("REMOVING")
                try:
                    characters.remove(int(characters[ind1 - 1]))
                except ValueError as e:
                    characters.remove(int(characters[ind1 - 2]))

            characters.append(str(prev_num) + 'u')

            if j == len(user_pass) - 1:
                print("WORKED", characters[-2])
                del characters[-2]
            double_digit_triggered = False
        else:
            print("prev_num set error")
            if i != " " and i != "u":
                prev_num = i
            try:
                num = int(i)
                characters.append(num)
                double_digit_triggered = False

            except ValueError as e: # If a space is encountered, skip iteration
                continue
print(characters)


for i in range(len(characters)): # User password's translator, determines whether a letter is intended to be uppercase
    try:
        if characters[i].is_integer:
            copy_paste(abc[characters[i]])
            
    except AttributeError as e:
        convert_to_number = characters[i][0]
        number = int(convert_to_number)
        if abc[number] not in range(26, 43):
            copy_paste(abc[number].upper())

keyboard.send_keys("{TAB}") # switch to next field for authentication key

clear_clipboard = ""
pyperclip.copy(clear_clipboard)