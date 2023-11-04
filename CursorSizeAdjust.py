import time
import pywinauto.keyboard as keyboard
import win32gui
import win32con
import os

os.startfile("ms-settings:")
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
keyboard.SendKeys("{RIGHT}")
time.sleep(0.2)
keyboard.SendKeys("{RIGHT}")

time.sleep(0.1)

# Hide window
win32gui.ShowWindow(settings_window, win32con.SW_HIDE)

# Move the settings window on-screen
win32gui.SetWindowPos(settings_window, None, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

time.sleep(0.5)

# Exit process
win32gui.PostMessage(settings_window, win32con.WM_CLOSE, 0, 0)