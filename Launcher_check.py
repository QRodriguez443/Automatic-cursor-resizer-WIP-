import win32gui
import pyautogui
import os
import subprocess
import threading
import pygetwindow as gw
from AutoMove_shared_variables import v, update_bool
# Some functions are no longer used due to changes in code
from initial_execution_funcs import subproces, init_var, var_false, read, write, string_to_int, int_reset

LAUNCHER_TITLE = "Star Wars™: The Old Republic™" # Task title of launcher window

# Pointers to modules to open in a subprocess
FILE_PATH = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "Launcher_check.py"), 
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "text_field_input_detection.py"),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "LauncherCreds.py")]

target_x, target_y = 1600, 1110 # Co-ordinates for mouse pointer

if __name__ == "__main__":
    class LauncherChecker:
        def __init__(self):
            self.times = 0

            self.event = threading.Event()
            self.timeout = threading.Event()

            self.result = None
            self.launcher_window = None


        def update_int(self): # Gets current number in txt and increments by 1
            file_path = os.path.dirname(os.path.abspath(__file__))
            joined_file = os.path.join(file_path,'error_thrown.txt')

            try:
                integer = read(joined_file)
                updated_int = string_to_int(joined_file, integer)
                return updated_int

            except FileNotFoundError as e:
                print("Error: {e}")
                write(joined_file, '')
                write(joined_file, '0')

                integer = read(joined_file)
                updated_int = string_to_int(joined_file, integer)
                return updated_int
            
        def is_window_active(self):
            global active_window

            while True: # Check if the target hWnd matches the currently focused hWnd
                self.timeout.wait(0.05)
                # Target window
                launcher_windows = win32gui.FindWindow(None, LAUNCHER_TITLE)

                if launcher_windows:
                    # Currently focused window
                    get_focused_window = win32gui.GetForegroundWindow()
                    window_handle = launcher_windows == get_focused_window
                    print("does handle match?", window_handle)

                    active_window = window_handle
                    self.event.set() # Signals that the active_window has been updated
        
        
        def check_launcher(self):
            active_thread = threading.Thread(target=self.is_window_active)
            active_thread.start()

            while True:
                # Find the target window in task list
                self.launcher_window = win32gui.FindWindow(None, LAUNCHER_TITLE)
                print(self.launcher_window)

                if self.launcher_window:
                    print("Launcher found")
                    alrdy_executed = False

                    for i in range(40):
                        print(i)
                        
                        if i == 39:
                            os.system("taskkill /IM python.exe /F")
                        
                        try:
                        # Set focus to the launcher window, then retrieve the ID of the active window
                            launcher_window = gw.getWindowsWithTitle(LAUNCHER_TITLE)
                            self.event.wait()
                            self.event.clear() # Signals that the active_window has been updated

                            if not active_window: # If the target window is not in focus
                                v('handle', False)
                                print("activating")
                                self.timeout.wait(0.15)

                                launcher_window[0].restore() # In case window is minimized
                                launcher_window[0].activate() # Activate the first window in the list
                                v('handle', True)

                                # Get current mouse position, then move mouse over selection field
                                original_mouse_position = pyautogui.position()
                                pyautogui.moveTo(target_x, target_y, duration=0)

                                speed_modified = update_bool("speed_modified") # See: mouse_speed.py

                                if not speed_modified: # Only open process if the mouse sensitivity is not currently modified
                                    subprocess.Popen(["python.exe", FILE_PATH[1]], shell=True) # text_field_input_detection.py

                                while True:
                                    mouse_over_field = update_bool('mouse_over_field') # See: text_field_input_detection.py
                                    if mouse_over_field:
                                        pyautogui.click()
                                        pyautogui.moveTo(original_mouse_position)
                                        break

                            else: # When the launcher is within focus, this block is executed
                                """
                                When launcher first starts, execution of this program interrupts focus to launcher, so 
                                immediately refocus with mouse. """
                                if not alrdy_executed: # This if block is only executed once
                                    original_mouse_position = pyautogui.position()
                                    pyautogui.moveTo(target_x, target_y, duration=0)
                                    subprocess.Popen(["python.exe", FILE_PATH[1]], shell=True) # text_field_input_detection.py

                                    while True:
                                        mouse_over_field = update_bool('mouse_over_field')

                                        if mouse_over_field:
                                            pyautogui.click()
                                            pyautogui.moveTo(original_mouse_position)
                                            break

                                    subprocess.Popen(["python.exe", FILE_PATH[2]], shell=True) # "LauncherCreds.py"
                                    v('handle', True)
                                    alrdy_executed = True

                                self.timeout.wait(0.3)

                        except gw.PyGetWindowException as e:
                            print(f"An error occurred: {e}")
                            print("wait for sleep:")
                            self.timeout.wait(0.2)

                            v('handle', False)
                            error_thrown = self.update_int()

                            if error_thrown >= 10: # Set amount of errors to be allowed
                                print('Max errors reached, exiting...')
                                int_reset() # Reset error_thrown to 0

                                os.system("taskkill /IM python.exe /F") # Force kill all instances
            
                else:
                    print("Launcher not running...")
                    self.times += 1

                    if self.times == 30000: # if Launcher not found after 30000 iterations, close program
                        os.system("taskkill /IM python.exe /F") # 30000 == about 5 seconds

    def main(): # Start instance of class
        int_reset() # Reset number of error_thrown
        
        first_instance = LauncherChecker()
        first_instance.check_launcher()

    main()