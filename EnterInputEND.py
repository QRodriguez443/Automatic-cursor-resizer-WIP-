import pywinauto.keyboard as keyboard
from pywinauto import Application
import subprocess
import time

# When batch file opens, access the window and set focus on the input field
app = Application(backend='uia').connect(title='Mouse_Cursor_Size_Adjust')

batch_window = app.window(title='Mouse_Cursor_Size_Adjust')

if batch_window == False:
    while True:
        print('Reconnecting...')
        time.sleep(1)

        Application(backend='uia').connect(title='Mouse_Cursor_Size_Adjust')

        if batch_window == True:
            break

user_input_field = batch_window['Text Area']

targetProcess = "swtor.exe"

# Check if the target process is NOT present in the output/task list
while True:
    #Loop the output to ensure the ending of the process is accurately detected
    output = subprocess.run(['tasklist'], capture_output=True, text=True)

    if targetProcess.lower() not in output.stdout.lower():
        user_input_field.set_focus()

        keyboard.SendKeys('{ENTER}')
        break

    else:
        print('Process still running...')
        time.sleep(1)