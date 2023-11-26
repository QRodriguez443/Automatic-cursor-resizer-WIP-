import time
import pywinauto.keyboard as keyboard
import win32gui
import win32con
import os
import subprocess
import pyautogui
import threading
import winreg
from pynput import mouse
global mouse_button_pressed
mouse_button_pressed = ""

def mouse_click_subprocess(): #Process for getting the mouse output and sending truthiness into variable
    while True:
        def on_click(x, y, button, pressed): 
                if (button == mouse.Button.left and pressed) or (button == mouse.Button.right and pressed):
                    global mouse_button_pressed
                    mouse_button_pressed = True  # Set True to indicate mouse button press
                    return False  # Stop the listener
        
        # Create a listener that calls the on_click function
        listener = mouse.Listener(on_click=on_click)
        # Start the listener to detect mouse events
        listener.start()
        listener.join()  # Wait for the listener to stop
        print("Clicked")
        time.sleep(1)
        global mouse_button_pressed
        mouse_button_pressed = False #Reset variable to prevent unintended functionality

def check_desktop_focus():
    # Ensure the targeted process window is out of focus before executing the rest of the code
    # and so that focus is not redirected from the settings window when the application closes
    while True:
        foreground_window = pyautogui.getActiveWindow()
        if foreground_window != "Star Wars™: The Old Republic™": #Title of application's window
            print("Desktop is within focus")
            break
def check_registry():
    key_path = r"Control Panel\Cursors"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
    cursor_path = winreg.QueryValueEx(reg_key, "Scheme Source")[0]
    print("Cursors folder path:", cursor_path)
    return cursor_path


def main_logic_restart(): #If main_logic loop is interrupted, open new instance of the program and close the current one
    while True:
        if mouse_button_pressed == True:
            file_path = "F:\SteamLibrary\steamapps\common\Star Wars - The Old Republic\CursorSizeAdjustDefault.py"
            subprocess.run(["cmd", "/c", "start", "python.exe", file_path], shell = True)
            os._exit(0)


def check_registry(): #Check cursor size
    key_path = r"Control Panel\Cursors"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
    for i in range(winreg.QueryInfoKey(reg_key)[1]):
        value_name, value_data, value_type = winreg.EnumValue(reg_key, i)
        if value_name == "CursorBaseSize" and value_data in [64, 48, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256]:
            return True 


def main_logic(): #The main function of the program, to open settings window and modify cursor size
    while True:
        settings_window = win32gui.FindWindow(None, "Settings")
        #In case settings is already open, close
        if settings_window == True: #evaluates to a value other than 0
            while True:
                win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)
                print("Closing settings, re-opening...")
                time.sleep(1)
                settings_window = win32gui.FindWindow(None, "Settings")
                if settings_window == False:
                    break
            
        os.startfile("ms-settings:") # Opens the Settings app in windows 10+, navigates to Accessibility, Mouse Pointer, and adjusts size slider.
        
        # All timings were tweaked for optimal speed and function
        # Move the settings window off-screen
        settings_window = win32gui.FindWindow(None, "Settings")
        win32gui.SetWindowPos(settings_window, None, -2000, -2000, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
        time.sleep(0.1)
    
        # Send key strokes to navigate to the Accessibility page
        keyboard.SendKeys("{TAB}")
        keyboard.SendKeys("{DOWN}")
        keyboard.SendKeys("{DOWN}")
        keyboard.SendKeys("{DOWN}")
        keyboard.SendKeys("{DOWN}")
        keyboard.SendKeys("{RIGHT}")
        keyboard.SendKeys("{ENTER}")
    
        time.sleep(0.15)
    
        # Modify mouse size
        keyboard.SendKeys("{TAB}")
        keyboard.SendKeys("{DOWN}")
        keyboard.SendKeys("{ENTER}")
        keyboard.SendKeys("{TAB}")
        time.sleep(0.2)
        keyboard.SendKeys("{LEFT}")
        time.sleep(0.5)
        keyboard.SendKeys("{LEFT}")
        check_registry()
        result = check_registry()
        if result == True: #Check if changes were updated, if not, then try again.
           time.sleep(0.5)
           keyboard.SendKeys("{LEFT}")
           if result == True: #Double-check
               time.sleep(1)
               keyboard.SendKeys("{LEFT}")
               
    
        time.sleep(0.1)
    
        # Hide window
        win32gui.ShowWindow(settings_window, win32con.SW_HIDE)
    
        # Move the settings window on-screen
        win32gui.SetWindowPos(settings_window, None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
    
        time.sleep(1)
    
        # Exit process
        win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)
    
        # Code execution is finished, close the console window
        os.system("taskkill /F /PID %d" % os.getpid())

    
def main(): # First section of code to execute when program starts
    check_desktop_focus()
    time.sleep(0.3)
    # Create new threads in order
    main_logic_thread = threading.Thread(target=main_logic,)#1.
    subprocess_thread = threading.Thread(target=mouse_click_subprocess,)#2.
    main_logic_restart_thread = threading.Thread(target=main_logic_restart)#3.
    main_logic_thread.start()#1.
    subprocess_thread.start()#2.
    main_logic_restart_thread.start()#3.
    main_logic_thread.join()#1.
    subprocess_thread.join()#2.
    main_logic_restart_thread.join()#3.


if __name__ == "__main__": #Set main() to be the first function to execute
    main()
