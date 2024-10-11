import pywinauto.keyboard as keyboard
import ctypes
import pyperclip
import random
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

# An attempt to better obscure the vision of the password and increase security in the event an attacker uses a keylogger

def has_two_digits(n, currentNum):
    """
    Checks if an integer has exactly two distinct digits.
    
    Args:
        n (int): The integer to check.
        
    Returns:
        bool: True if the integer has exactly two distinct digits, False otherwise.
    """
    # Convert the integer to a string to access its digits

    digit = set(str(abs(int(n))))
    currentDigit = set(str(abs(int(currentNum))))
    
    # Check if the set of digits has exactly 2 elements
    print(len(digit), len(currentDigit))
    return len(digit) == 1 and len(currentDigit) == 1

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
        print("unimportant error", e)
        return input_str
    
    return int(current_num) if current_num else None

# For every character copied, (an) extra random character(s) is/are added
def copy_paste(array: str):

    print(array)
    pyperclip.copy(array)
    keyboard.send_keys('{'+ array +'}')
    SendInput = ctypes.windll.user32.SendInput

    # Virtual key code for 'F'
    VK_F = 0x46
    
    # Press and release the 'F' key
    SendInput(1, ctypes.pointer(ctypes.c_ulong(VK_F)), ctypes.sizeof(ctypes.c_ulong))
    SendInput(1, ctypes.pointer(ctypes.c_ulong(VK_F | 0x0002)), ctypes.sizeof(ctypes.c_ulong))
 
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

abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*'])
shuffle_abc = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*'])

random.shuffle(shuffle_abc)
characters = [] # User's password is appended into the array one by one

user_pass = os.environ.get('USER_PASS') # User's created password
for j, i in enumerate(user_pass): # Organize and separate each character into the array
    print(characters)
    if iterations == 2: # After the second iteration, store every previous, previous value of i (j - 2)
        try:
            prev_prev_value = int(user_pass[j - 2])
        except ValueError as e:
            prev_prev_value = None

        print("prevprevnum:", prev_prev_value)

    if iterations != 2:
        iterations += 1
    try:
        if prev_num is not None:
            print("ENTER VALUE")
            prev_num_is_number = contains_number(prev_num)

            if prev_num_is_number is not None and user_pass[j] is not None:
                value = has_two_digits(prev_num_is_number, user_pass[j])
            else:
                value = False
                
            if value is True:
                print("There were 2 numbers", prev_num, user_pass[j])  
                del characters[-1]
                print("REMOVE NUM")
                double_digit_int = str(prev_num) + str(user_pass[j]) # combine the string of 2 individual nums
                characters.append(int(double_digit_int)) # append the string of 2 as a whole integer
                prev_num = int(double_digit_int) # To ensure proper functionality if user adds 'u' in front of double-digit
                continue # Skip iteration so as not to duplicate the current number to the list
        
        print("prev_num set")    
        prev_num = user_pass[j]
        num = int(i)
        characters.append(num)
        double_digit_triggered = False

    except ValueError as e:
        if user_pass[j] == 'u':
            print("Entered u")
            print("This is why i == prev_num: ", prev_prev_value, user_pass[j - 1])

            if prev_prev_value == user_pass[j - 1]:
                print("REMOVING")
                characters.remove(characters[j - 1])
            elif j == 1: # In case "u" is presented before prev_prev_value is defined
                characters.remove(characters[j - 1])

            characters.append(str(prev_num) + 'u')

            if prev_prev_value is None and j != len(user_pass) - 1: # If the last current character contains "u", then delete duplicate character behind it
                str(characters[-1])
                num = contains_number(characters[-1])
                try:
                    if num == characters[-2]:
                        del characters[-2]
                except IndexError as e:
                    None
                
            if j == len(user_pass) - 1: # If the last character contains "u" then delete the duplicate character behind it
                print("WORKED", characters[-2])
                del characters[-2]
            double_digit_triggered = False
        else:
            print("prev_num set error")
            prev_num = user_pass[j]
            try:
                num = int(i)
                characters.append(num)
                double_digit_triggered = False

            except ValueError as e: # If a space is encountered, skip iteration
                print("Space Error")
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