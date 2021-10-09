from pathlib import Path
import sys

# Input format : [COMMAND] [INPUT] [[-]OPTION] [INPUT]
CMD_2_OPTIONS = ['-r', '-f', '-s', '-e']

def get_content(path) -> list:
    """Returns sorted list of the content of the directory,
    including the files and directories.
    Sorts files first THEN directories.
    param: path object
    returns: list"""

    file_list, dir_list = [], []
    if not path.exists():  # File or directory doesn't exist
        print_error()
        return []

    for item in path.iterdir():
        if item.stem.startswith('.'):
            continue  # Ignore hidden files
        elif item.is_file():
            file_list.append(item.absolute())
        elif item.is_dir():
            dir_list.append(item.absolute())

    return file_list + dir_list
            

def print_list(lst: list) -> None:
    """Prints all the items in a list."""
    for i in lst:
        print(i)


def create_file(file_path) -> None:
    """Creates a file with the given path and
    raises an 'ERROR' incase a file with the given path
    already exists."""
    try:
        with open(file_path, 'x') as _:
            print(file_path)
    except FileExistsError:  # File already exists
        print_error()


def read_file(file_path) -> None:
    """Opens the file path and reads its contents.
    If the file is empty, it will print 'EMPTY'
    """
    with open(file_path, 'r') as f:
        file_content = f.read().strip()
        if file_content == '':
            print('EMPTY')
        else:
            print(file_content)


def delete_file(path) -> None:
    """Deletes a file and prints 'DELETED'
    """
    path.unlink()
    print(path.absolute(), 'DELETED')


def print_error() -> None:
    """Prints 'ERROR'
    """
    print('ERROR')
    


def end_program() -> None:
    """Ends the program."""
    sys.exit()


class Input_Manager:
    """This class handles the path name and for
    getting commands in the input string."""
    def __init__(self, input_list):
        self.input_list = input_list
        self.cmds_used = False
    def empty_list(self):
        self.input_list = []
    
    def check_cmds(self, item):
        """Checks to see if the commands -r, -f, -s, or -e are used."""
        if item in CMD_2_OPTIONS:
            self.cmds_used = True
            return True  # The user has used commands in the input

    def get_path_name(self):
        """Retrieves the path name until the first command.
        The path name can be fully retrieved even if it has spaces in the name."""
        for index, item in enumerate(self.input_list):
            if self.check_cmds(item):
                path_name = ' '.join(self.input_list[:index])
                self.input_list = self.input_list[index:]  # New input_list with only commands
                break

        if self.cmds_used:
            return path_name

        else:
            return ' '.join(self.input_list)


class Optional_Listing:
    """Handles listing files and directories
    depending on the option given."""

    def __init__(self, path):
        self.path = path
        self.recursion = False
        self.file_only = False
        self.searching = False
        self.extension = False

        self.lst = []

    def go_through_commands(self, command_list):
        """Goes through commands incase there are multiple commands used, like -r -f."""
        while command_list:  # While there is still commands in the input
            if command_list[0] in CMD_2_OPTIONS:
                self.pick_option(command_list.pop(0))  # Deletes command from list
            else:
                 break
                # The rest of the command list is turned into
                #a string that is either a filename or extension
    
    def pick_option(self, option):
        """Set boolean values to True depending on which command is used."""
        if option == '-r':
            self.recursion = True
        elif option == '-f':
            self.file_only = True
        elif option == '-s':
            self.searching = True
        elif option == '-e':
            self.extension = True

    def get_recursive_content(self, path):
        """Goes through all the subdirectories and retrieves files and directories
        This is used when only the -r command is used."""
        # Append all the files to list first
        lst1 = get_content(path)
        for item in lst1:
            if item.is_file():
                self.lst.append(item.absolute())
            else:
                self.lst.append(item.absolute())
                self.get_recursive_content(item)
                

    def get_files(self, path):
        """Goes through the path directory and retrieves files only."""
        lst1 = get_content(path)
        for item in lst1:
            if item.is_file():
                self.lst.append(item.absolute())
            elif item.is_dir() and self.recursion:  # If the -r command was used before the -f command
                self.get_files(item)

            
    def search(self, file_name, path):
        """Goes through the path directory and searches for the given file name."""
        for item in path.iterdir():            
            if item.is_file() and item.name== file_name:
                self.lst.append(item.absolute())
            elif item.is_dir() and self.recursion:  # If the -r command was used before the -s command
                self.search(file_name, item)
            
    def find_extension(self, extension, path):
        """Goes through the path directory and searches for the given extension."""
        for item in path.iterdir():
            if item.is_file() and item.suffix == '.' + extension:
                self.lst.append(item.absolute())
            elif item.is_dir() and self.recursion:  # If the -r command was used before the -e command
                self.find_extension(extension, item)


class Dsu_File_Manager:
    """Handles the creation, reading, and deletion of DSU Files."""
    def __init__(self, input_list):
        self.input_list = input_list

    def create(self):
       """Creates a DSU file, and names the file after the -n command."""
       input_string = ' '.join(self.input_list)
       path_and_file = input_string.split(' -n ')
       try:
           path_name = path_and_file[0]
           file_name = path_and_file[1]
       except IndexError:
           print_error()
       else:
           full_pathway = path_name + '/' + file_name + '.dsu'
           create_file(full_pathway)
        
    def delete(self):
        """Deletes a DSU file."""
        file_path = ' '.join(self.input_list)
        path = Path(file_path)

        if path.is_file():
            if path.suffix != '.dsu':
                print_error()
            else:
                delete_file(path)

        else:
            print_error()

    def read(self):
        """Reads a DSU file."""
        file_path = ' '.join(self.input_list)
        path = Path(file_path)

        if path.is_file():
            if path.suffix != '.dsu':
                print_error()
            else:
                read_file(file_path)

        else:
            print_error()

def handle_list_command(input_list):
    """Given the command 'L', this function manipulates the input from the user to get the full
    path name (even if there are spaces in the file name) and the commands. It also lists the
    files and directories depending on the command given.
    -r -> prints all the files and subdirectories as well as the main directory (recursive)
    -f -> prints only files
    -s (file name) -> searches for the file name
    -e (extension) -> searches for files with the given extension
    -r -f -> prints files recursively
    -r -s (file name) -> searches through files recursively
    -r -e (extension) -> finds the extensions recursively
    """
    
    inp_mang = Input_Manager(input_list)
    path_name = inp_mang.get_path_name()

    if not inp_mang.cmds_used:
        inp_mang.empty_list()
    command_list = inp_mang.input_list

    path = Path(path_name)
    opt_list = Optional_Listing(path)

    if command_list:
        # If the user added any optional input after the path
        opt_list.go_through_commands(command_list)
        if command_list:
            string_input = command_list
            
    else:
        content_list = get_content(path)


    if opt_list.file_only:
            opt_list.get_files(path)

    elif opt_list.searching:
        opt_list.search(' '.join(string_input), path)

    elif opt_list.extension:
        opt_list.find_extension(command_list[-1], path)

    elif opt_list.recursion:  # Has to be recursion list only (-r)
        opt_list.get_recursive_content(path)


    if opt_list.lst:  # If the class list isn't empty
        # (No optional commands were used)
        content_list = opt_list.lst


    if path_name:
        # This will print the list of files or files/directories GIVEN that the path name was entered in the input
        try:
            print_list(content_list)
        except UnboundLocalError:  # content_list is never assigned (file was not found when searching
            print_error()
        
    else:  # Only the first command was entered, such as 'L'
        print_error()

def main(user_input):
    """Splits the input_list by spaces and goes through the first comamnd."""
    # Change the names to make it more clear like command_list to optional_input
    input_list = user_input.split(' ')
    command = input_list.pop(0) # Delete COMMAND from input_list
    dsu_file = Dsu_File_Manager(input_list)
    
    if command == 'L':
        handle_list_command(input_list)

    elif command == 'C':
        dsu_file.create()

    elif command == 'D':
        dsu_file.delete()

    elif command == 'R':
        dsu_file.read()
        
    else:
        print_error()


def user_loop():
    """Runs a loop that enables the user to either enter input or to quit."""
    while True:
        user_input = str(input())
        try:
            if user_input[0] == 'Q':
                end_program()
        except IndexError:  # If nothing is entered into the input
            print_error()
        else:
            main(user_input)


if __name__ == '__main__':
    user_loop()
