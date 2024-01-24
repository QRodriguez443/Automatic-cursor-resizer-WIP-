import pywinauto.keyboard as keyboard
import time
from pywinauto import Application
import subprocess
import os

# When batch file opens, access the window and set focus on the input field
app = Application(backend="uia").connect(title="Mouse_Cursor_Size_Adjust")

batch_window = app.window(title="Mouse_Cursor_Size_Adjust")

user_input_field = batch_window["Text Area"]

targetProcess = "swtor.exe"

# Check if the target process is present in the output
while True:
    # Loop the output to ensure the activation of the process is accurately detected
    output = subprocess.run(["tasklist"], capture_output=True, text=True)

    if targetProcess.lower() in output.stdout.lower():
        user_input_field.set_focus()

        keyboard.SendKeys('{ENTER}')
        time.sleep(1)

        os.startfile("AutoMove.py")
        break

    else:
        print('Process not found...')
        time.sleep(1)
