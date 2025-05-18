import os


def create_folder(folder_name:str):
    """
    Create a folder with the given name.
    if the folder already exists, append a number to the name.
    a folder with the same name and number might already exist.
    in that case, increment the number until a unique name is found. 
    """
    counter = 1
    new_folder_name = folder_name
    while os.path.exists(new_folder_name):
        new_folder_name = f"{folder_name}_{counter}"
        counter += 1
    os.makedirs(new_folder_name)
    return new_folder_name
def create_file(file_name:str):
    """
    Create a file with the given name.
    if the file already exists, append a number to the name.
    a file with the same name and number might already exist.
    in that case, increment the number until a unique name is found. 
    """
    base_name, ext = os.path.splitext(file_name)
    counter = 1
    new_file_name = file_name
    while os.path.exists(new_file_name):
        new_file_name = f"{base_name}_{counter}{ext}"
        counter += 1
    with open(new_file_name, 'w') as f:
        pass  # Create an empty file
    return new_file_name

log_file = ""
def init_log(input_file:str):
    """
    Initialize the log file by creating it if it doesn't exist.
    """
    global log_file
    log_file = os.path.splitext(input_file)[0] + ".log"
    log_file = create_file(log_file) 
    with open(log_file, 'w') as f:
        f.write("Log file initialized.\n")
        print(f"Log file created: {log_file}")

def log(section:str, message:str, verbose=False, mandatory=False):
    """
    Print a message to the console, formatted with the section name.
    Prints if verbose is True or if the message is mandatory.
    """
    if verbose:
        save_log(log_file, f"{section}: {message}")
    if mandatory:
        print(f"{section}: {message}")

def save_log(log_file:str, message:str):
    """
    Save a message to the log file.
    """
    with open(log_file, 'a') as f:
        f.write(message + '\n')