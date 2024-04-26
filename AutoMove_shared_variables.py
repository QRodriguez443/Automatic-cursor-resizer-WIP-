import os

# Shared by multiple modules to read and write booleans into corresponding variables' text files
# The idea was to create a way of declaring variables that can be shared between separate modules using text files(there's probably a better method I'm unaware of).
# NO NEED TO MANUALLY CREATE ANY TEXT FILES, read_variable() WILL DO IT AUTOMATICALLY

def update_bool(txt_filename: str) -> bool: # Unfortunately must be used separately from v() to read the main(THE MODULE IN WHICH THE VARIABLE IS FIRST DECLARED) txt from separate modules
    shared_variabletxt = variable_txtfile(txt_filename)

    try:
        with open(shared_variabletxt, "r") as file:
            shared_variabletxt = file.read().strip()
        return shared_variabletxt == 'True'
    
    except FileNotFoundError as e:
        #print('File not found, creating txt file')

        with open(shared_variabletxt, 'w') as file:
            file.write('')

        with open(shared_variabletxt, "r") as file:
            shared_variabletxt = file.read().strip()
        return shared_variabletxt == 'True'

def read_variable(shared_variabletxt: str) -> bool: # Used to get the state of a variable
    # Open and read value of the shared variable
    try:
        with open(shared_variabletxt, "r") as file:
            shared_variabletxt = file.read().strip()
            
    except FileNotFoundError as e:
        #print('File not found, creating txt file')

        with open(shared_variabletxt, 'w') as file:
            file.write('')

        with open(shared_variabletxt, "r") as file:
            shared_variabletxt = file.read().strip()

    #print('read_variable:', shared_variabletxt)
    global update_bool
    update_bool = shared_variabletxt == 'True'
    return shared_variabletxt == 'True'

def set_variable(shared_variabletxt: str, bvalue: bool) -> None: # Write true/false string into txt file
    # Modify the shared variable 
    with open(shared_variabletxt, "w") as file:
        #print('set_variable:', shared_variabletxt)
        
        #print('writing', bvalue)
        file.write(str(bvalue)) # Translate boolean into string

def variable_txtfile(txt_filename: str) -> str: # Get the relative path to a specified text file
    # Get this script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the relative path to txt file
    relative_path = txt_filename + '.txt' # So the parameter has better readability
    press_path = os.path.join(script_dir, relative_path)

    global variable
    variable = press_path
    return variable
    # variable will be path to the text file used by "result" in declare_variable

# Function should equal the value of txt file, replace parameter with txt name w/o extension
def declare_variable(var: str) -> tuple[str, bool, str]:
    global result
    result = variable_txtfile(var)
    #print('sending', result)

    truefalse_result = read_variable(result)
    return result, truefalse_result, var
    # Result is the txt file path being returned
    # truefalse_result is the boolean being returned

# Gets the txt file/variable: and reads the boolean, returns name of txt and the txt's path
def name_of_file(name: str) -> tuple[str, str]:
    declared_var = declare_variable(name) # Replaced with txt file name

    txt_path = declared_var[0]
    boo = declared_var[1]
    return txt_path, name

# Return boolean from specified txt file
def path_bool(var: str, boolean: bool) -> bool:
    set_variable(var, boolean)

    declared_var = declare_variable(name)
    boo = declared_var[1]
    return boo

# For better readability, executing the function looks similar to declaring a variable
# Ex: variable = v(variable, False)
def v(var: str, boolean: bool) -> bool: # Reads and modifies the txt file at the same time.
    global name
    txt_path, name = name_of_file(var)

    var = path_bool(txt_path, boolean)
    new_variable = var
    return new_variable
    
    