import os

def init_var(): # Initialize boolean string
    file_path = os.path.dirname(os.path.abspath(__file__))
    joined_file = os.path.join(file_path,'initial_execution.txt')
    
    try:
        read(joined_file)
        write(joined_file, 'True')

        return True
        
    except FileNotFoundError as e:
        print("Error: {e}")

        write(joined_file, '')
        write(joined_file, 'True')
        
        return True
        
def var_false(): # Set boolean string to False
    file_path = os.path.dirname(os.path.abspath(__file__))
    joined_file = os.path.join(file_path,'initial_execution.txt')

    try:
        read(joined_file)
        write(joined_file, 'False')

        return False

    except FileNotFoundError as e:
        print("Error: {e}")

        write(joined_file, '')
        read(joined_file)
        write(joined_file, 'False')

        return False

def subproces(name_of_process: str, process_not_found: bool): # Get name of running process
    file_path = os.path.dirname(os.path.abspath(__file__))
    joined_file = os.path.join(file_path,'current_subprocess.txt')
    
    try:
        read(joined_file)
        
        if process_not_found:
            write(joined_file, '')

            return None
        
        else:
            write(joined_file, name_of_process)

            return name_of_process
        
    except FileNotFoundError as e:
        print("Error: {e}")

        write(joined_file, '')
        
        if process_not_found:
            write(joined_file, '')

            return None
        
        else:
            write(joined_file, name_of_process)

            return name_of_process
        
            
def write(path, to_write):
        with open(path, 'w') as file:
            file.write(to_write)
 
def read(path):
    with open(path, "r") as file:
        value = file.read().strip()
        return value
    
def string_to_int(path, integer): # Convert string to integer, add 1 then revert back to string
        integer = int(integer)
        newint = integer + 1

        intstring = str(newint)
        write(path, intstring)

        updated_int = int(intstring)

        return updated_int # Return new/updated number to error_thrown variable

def int_reset(): # Intended to reset the int to 0
            file_path = os.path.dirname(os.path.abspath(__file__))
            joined_file = os.path.join(file_path,'error_thrown.txt')

            write(joined_file, '0')