import time
import pywinauto.keyboard as keyboard
import win32gui
import win32con
import os
import winreg

def check_registry(): #Check cursor size
    key_path = r"Control Panel\Cursors"
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
    for i in range(winreg.QueryInfoKey(reg_key)[1]):
        value_name, value_data, value_type = winreg.EnumValue(reg_key, i)
        if value_name == "CursorBaseSize" and value_data in [64, 48, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256]:
            return True 


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
os.startfile("ms-settings:")
time.sleep(1)
settings_window = win32gui.FindWindow(None, "Settings")
if settings_window == False: #In case settings fails to open, try again
    while True:
        print(settings_window)
        time.sleep(1)
        os.startfile("ms-settings:")
        time.sleep(1)
        settings_window = win32gui.FindWindow(None, "Settings")
        if settings_window == True:
            break

#All timings were tweaked for optimal speed and function
# Opens the Settings app in windows 10+, navigates to Accessibility, Mouse Pointer, and adjusts size slider.

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
keyboard.SendKeys("{RIGHT}")
time.sleep(0.5)
keyboard.SendKeys("{RIGHT}")
check_registry()
result = check_registry()
if result != True: #Check if changes were made
    time.sleep(0.5)
    keyboard.SendKeys("{RIGHT}")
    time.sleep(0.5)
    keyboard.SendKeys("{RIGHT}")

time.sleep(0.1)

# Hide window
win32gui.ShowWindow(settings_window, win32con.SW_HIDE)

# Move the settings window on-screen
win32gui.SetWindowPos(settings_window, None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

time.sleep(1)

# Exit process
win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)
