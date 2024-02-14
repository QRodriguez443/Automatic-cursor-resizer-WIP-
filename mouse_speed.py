import ctypes
import threading
from AutoMove_shared_variables import v

"""
Modifies mouse speed for a limited time so that when the cursor is directed to the 
selection field using Launcher_check, it is not accidentally moved by user.
"""
SPI_SETMOUSESPEED = 0x71

def set_mouse_sensitivity(speed):
    sms = SPI_SETMOUSESPEED
    ctypes.windll.user32.SystemParametersInfoW(sms, 0, speed, 0)

def main():
    current_sensitivity = 10 # Set default mouse sensitivity
    try:
        # Get the current mouse sensitivity setting
        print("Current mouse sensitivity:", current_sensitivity)
        
        # Set a temporary sensitivity (for demonstration)
        new_sensitivity = 1
        
        # Modify the sensitivity temporarily
        set_mouse_sensitivity(new_sensitivity)
        print("Temporary sensitivity set to:", new_sensitivity)

        v("speed_modified", True)

        threading.Event().wait(0.5)

        # Restore the original sensitivity
        set_mouse_sensitivity(current_sensitivity)
        print("Restored sensitivity to:", current_sensitivity)
        v("speed_modified", False)

    except Exception as e:
        print("An error occurred:", e)
        
if __name__ == '__main__':
    main()