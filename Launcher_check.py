import win32gui
import pyautogui
import os
import subprocess
import threading
import pygetwindow as gw
from AutoMove_shared_variables import v, update_bool
from initial_execution_funcs import subproces, init_var, var_false, read, write, string_to_int, int_reset
# Some functions are no longer used due to changes in code

LAUNCHER_TITLE = "Star Wars™: The Old Republic™" # Task title of launcher window

# Pointers to files
FILE_PATH = [ 
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "text_field_input_detection.py"),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "LauncherCreds.py"),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_thrown.txt"),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "Launcher_check.py")
             ]

if __name__ == "__main__":
    class LauncherChecker:
        def __init__(self):
            self.times = 0
            self.target_x = 1600
            self.target_y = 1110 # Co-ordinates for mouse pointer

            self.event = threading.Event()
            self.timeout = threading.Event()

            self.result = None
            self.launcher_window = None

        # Keeps track of amount of errors being thrown
        def update_int(self) -> int: # Gets current number in txt and increments by 1
            try:
                integer = read(FILE_PATH[2])
                updated_int = string_to_int(FILE_PATH[2], integer)
                return updated_int

            except FileNotFoundError as e:
                print("Error: {e}")
                write(FILE_PATH[2], '')
                write(FILE_PATH[2], '0')

                integer = read(FILE_PATH[2])
                updated_int = string_to_int(FILE_PATH[2], integer)
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

            global alrdy_executed
            alrdy_executed = False

            while True:
                # Find the target window in task list
                self.launcher_window = win32gui.FindWindow(None, LAUNCHER_TITLE)
                print(self.launcher_window)

                if self.launcher_window:
                    print("Launcher found")

                    try:
                    # Set focus to the launcher window, then retrieve the ID of the active window
                        launcher_window = gw.getWindowsWithTitle(LAUNCHER_TITLE)
                        self.event.wait()
                        self.event.clear() # Signals that the active_window has been updated

                        if not active_window: # If the target window is not in focus
                            alrdy_executed = True
                            print("activating")

                            launcher_window[-1].restore() # In case window is minimized
                            launcher_window[-1].activate() # Activate the first window in the list

                            # Get current mouse position, then move mouse over selection field
                            original_mouse_position = pyautogui.position()
                            pyautogui.moveTo(self.target_x, self.target_y, duration=0)
                            
                            speed_modified = update_bool("speed_modified") # See: mouse_speed.py

                            if not speed_modified: # Only open process if the mouse sensitivity is not currently modified
                                subprocess.Popen(["python.exe", FILE_PATH[0]], shell=True) # text_field_input_detection.py

                            while True: # Keep mouse cursor within field until operation completes
                                mouse_over_field = update_bool('mouse_over_field') # See: text_field_input_detection.py
                                pyautogui.moveTo(self.target_x, self.target_y, duration=0)

                                if mouse_over_field:
                                    pyautogui.click()
                                    pyautogui.moveTo(original_mouse_position)
                                    subprocess.Popen(["python.exe", FILE_PATH[1]], shell=True) # "LauncherCreds.py"
                                    break

                        else: # This block is executed only once if the launcher is in focus upon first run of this script.

                            if not alrdy_executed: # This if block is only executed once
                                original_mouse_position = pyautogui.position()
                                
                                pyautogui.moveTo(self.target_x, self.target_y, duration=0)
                                subprocess.Popen(["python.exe", FILE_PATH[0]], shell=True) # text_field_input_detection.py

                                while True: # Keep mouse cursor within field until operation completes
                                    mouse_over_field = update_bool('mouse_over_field')
                                    pyautogui.moveTo(self.target_x, self.target_y, duration=0)

                                    if mouse_over_field:
                                        pyautogui.click()
                                        pyautogui.moveTo(original_mouse_position)
                                        break

                                subprocess.Popen(["python.exe", FILE_PATH[1]], shell=True) # "LauncherCreds.py"
                                alrdy_executed = True
                                self.timeout.wait(0.3)

                        self.times += 1
                        if self.times == 8: # Only allow this section to run for 8 iterations
                            v('exit_code', True)
                            os._exit(0)

                    except gw.PyGetWindowException as e:
                        print(f"An error occurred, most likely due to   \
                                interruption of window's focus: {e}")
                        self.timeout.wait(1)

                        # Start new instance to escape error and continue
                        subprocess.Popen(["python.exe", FILE_PATH[3]], shell=True)

                        error_thrown = self.update_int()

                        if error_thrown >= 10: # Set amount of errors to be allowed
                            print('Max errors reached, exiting...')
                            int_reset() # Reset error_thrown to 0
                            v('exit_code', True)
                            os._exit(0) # Force kill all instances
            
                else:
                    print("Launcher not running...")
                    self.times += 1

                    if self.times == 30000: # if Launcher not found after 30000 iterations, close program
                        v('exit_code', True)
                        os._exit(0) # 30000 == about 5 seconds

    def main(): # Start instance of class
        v('exit_code', False)
        v("speed_modified", False) # Reset the indicator of mouse sensitivity modification
        int_reset() # Reset number of error_thrown
        
        first_instance = LauncherChecker()
        first_instance.check_launcher()

    main()