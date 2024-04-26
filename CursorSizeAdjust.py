import pywinauto.keyboard as keyboard
from pynput import keyboard as kb
import win32gui
import win32con
import os
import winreg
import threading
import subprocess
from access_registry import close_key, get_key_info
import concurrent.futures

timer = threading.Event()
left_right = threading.Event() # Ensures logic is properly synched
key_block = threading.Event()
result = None

# Choose desired cursor size
actions = { # Defines all possible size selections
    32: 1,
    48: 2,
    64: 3,
    80: 4, # Desired cursor size
    96: 5,
    112: 6,
    128: 7,
    144: 8,
    160: 9,
    176: 10,
    192: 11,
    208: 12,
    224: 13,
    240: 14,
    256: 15
}

key_list = list(actions.keys())
SELECTED_SIZE = key_list[3]

def key_input(key: str, iters: int): # Maintain compact code for identical keys used in succession
    for i in range(iters):
        keyboard.send_keys(key)

        if i == iters:
            break

def check_registry(): # Check cursor size before continuing program
    key_path = r"Control Panel\Cursors"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

    for i in range(winreg.QueryInfoKey(reg_key)[1]):
        value_name, value_data, value_type = winreg.EnumValue(reg_key, i)
            
        if value_name == "CursorBaseSize":
            if value_data == SELECTED_SIZE:
                print("Correct size already set, no changes required.")
                os._exit(0)
            else:
                return False
            
def get_current_size() -> int:
    value_data = get_key_info() # Get the starting size level
    
    if value_data in actions:
        action = actions[value_data]
        print("Current cursor size level:", action)
        return action

def update_current_size_right():
    global listener
    global size
    global current_value

    if current_value == size:
        key_block.set()
        listener.stop()

    if current_value == actions[256]: # If max size is reached, stop incrementing current_value
        print("Max level reached")
        print(current_value)
        
    if current_value:
        current_value = current_value + 1

        for action in actions:
            if actions[action] == current_value: # Find the key that matches the new value
                current_value = actions[action]  # Update current size level
        left_right.set()
    print(current_value)

def update_current_size_left():
    global listener
    global current_value
    global size

    if current_value == size:
        key_block.set()
        listener.stop()


    if current_value == actions[32]: # If min size is reached, stop subtracting current_value
        print("Minimum level reached")
        print(current_value)
        
    if current_value:
        current_value = current_value - 1

        for action in actions:
            if actions[action] == current_value: # Find the key that matches the new value
                current_value = actions[action]  # Update current size level
        left_right.set()
    print(current_value)

def right_left_listener(key):
    print("listener")

    if key == kb.Key.right:
        print("Entered right")
        update_current_size_right()
        left_right.set()
        
    if key == kb.Key.left:
        print("Entered left")
        update_current_size_left()
        left_right.set()

def start_size_updater(desired_size: int):
    '''
    *desired_size: size selection ranges from 1-15

    Gets the current cursor size from registry, then any subsequent changes will be
    updated using a keyboard listener based on the right and left keys' inputs.
    
    (Registry updating introduces delays when synchronizing with changes to the pointer size in control panel)
    '''
    global listener
    global current_value
    global size
    size = desired_size
    current_value = get_current_size()
    close_key()
    listener = kb.Listener(on_press=right_left_listener)
    listener.start()

    left_right.set()
    listener.join()

def queue_up():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(start_size_updater, 4)  # Submit the function call
        result = future.result()  # Get the result when it's ready


def modify_size_check_registry(): # Modify the cursor size in accordance to logic
    global current_value
    file_path = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "execute_left_key.exe"),
                 os.path.join(os.path.dirname(os.path.abspath(__file__)), "execute_right_key.exe")]
    while True:
        left_right.wait()

        if current_value == size:
            break

        if current_value > size:
            subprocess.call([file_path[0]]) # Press left key with c++
            print(current_value)

        if current_value < size:
            subprocess.call([file_path[1]]) # Press right key with c++
            print(current_value)


if __name__ == "__main__":
    # Start of program:
    check_registry()
    
    settings_window = win32gui.FindWindow(None, "Settings")
    print("old:", settings_window)

    #In case settings is already open, close
    if settings_window:

            for i in range(4):
                win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)
                print("Closing settings, re-opening...")
                timer.wait(0.2)
        
                settings_window = win32gui.FindWindow(None, "Settings")
        
                if not settings_window:
                    break
                elif i == 3:
                    print("Incorrect handle being retrieved")
                    try:
                        os.startfile("ms-settings:") # Resets window
                    except OSError as e:
                        print("error", e)
                    finally:
                        timer.wait(0.2)

    os.startfile("ms-settings:")
    timer.wait(0.2)
    settings_window = win32gui.FindWindow(None, "Settings")
    print("new:", settings_window)

    if not settings_window: # In case settings fails to open, try again
        while True:
            print("Failed to open, retrying...", settings_window)
    
            os.startfile("ms-settings:")
            timer.wait(0.5)
    
            settings_window = win32gui.FindWindow(None, "Settings")
            print("new:", settings_window)

            if settings_window:
                break
    
    # All timings were tweaked for optimal speed and function
    # Opens the Settings app in windows 10+, navigates to Accessibility, Mouse Pointer, and adjusts size slider.
    
    # Move the settings window off-screen
    settings_window = win32gui.FindWindow(None, "Settings")
    #win32gui.SetForegroundWindow(settings_window)
    #win32gui.SetWindowPos(settings_window, None, -2000, -2000, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    
    print(os.path.dirname(os.path.abspath(__file__)),"\", "navigation.exe")
    exit(0)
    # Modify cursor size based on logic
    thread1 = threading.Thread(target=queue_up)
    thread1.start()
    modify_size_check_registry()
    timer.wait(0.2)
    thread1.join()
    
    
    
    # Hide window
    #win32gui.ShowWindow(settings_window, win32con.SW_HIDE)
    
    # Move the settings window on-screen
    #win32gui.SetWindowPos(settings_window, None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    
    timer.wait(1.5)
    
    # Exit process
    #win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)