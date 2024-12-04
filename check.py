import argparse  # Importing the argparse module for parsing command-line arguments
import hashlib  # Importing the hashlib module for creating hash functions
import os  # Importing the os module for interacting with the operating system

# Function for creating or recreating the 'hash.check' file
def init():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the 'hash.check' file in the script directory
    file_path = os.path.join(script_dir, 'hash.check')
    
    try:
        # Check if the 'hash.check' file already exists
        if os.path.exists(file_path):
            print(f"File 'hash.check' already exists in the directory: {script_dir}")
            # Ask the user if they want to remake the file
            remakeCom = input("Do you want to remake it? (y/n): ").strip().lower()
            
            if remakeCom == 'y':
                try:
                    # Remove the existing 'hash.check' file
                    os.remove(file_path)
                    # Create a new 'hash.check' file and write a welcome message
                    with open(file_path, 'w') as file:
                        file.write("Welcome to hash.check\n")
                    print(f"File 'hash.check' has been recreated in the directory: {script_dir}")
                except PermissionError:
                    # Handle the case where the file cannot be removed or created due to permission issues
                    print("Permission denied: Unable to remove or create the file.")
                except OSError as e:
                    # Handle other OS-related errors
                    print(f"OS error occurred: {e}")
            elif remakeCom == 'n':
                # If the user chooses not to remake the file
                print("File 'hash.check' was not modified.")
            else:
                # Handle unrecognized input
                print("Command not recognized. Please enter 'y' or 'n'.")
        else:
            try:
                # Create a new 'hash.check' file and write a welcome message
                with open(file_path, 'w') as file:
                    file.write("Welcome to hash.check\n")
                print(f"File 'hash.check' has been created in the directory: {script_dir}")
            except PermissionError:
                # Handle the case where the file cannot be created due to permission issues
                print("Permission denied: Unable to create the file.")
            except OSError as e:
                # Handle other OS-related errors
                print(f"OS error occurred: {e}")
    except ImportError:
        # Handle the case where the 'os' module is not available
        print("ImportError: The 'os' module is not available.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

# Function to calculate the SHA-1 hash of a file
def sha1_calculation(pathspec):
    # Create a new SHA-1 hash object
    sha1_hash = hashlib.sha1()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'hash.check')

    prefixes = {
        1: "[OK]",       # File is added or updated without changes
        2: "[CHANGED]",  # File hash has changed
        3: "[ERROR]"     # Error occurred (e.g., file not found)
    }
    
    try:
        # Check if the specified path is a file
        if not os.path.isfile(pathspec):
            # Raise an error if the file does not exist
            raise FileNotFoundError(f"The file {pathspec} does not exist.")
        
        # Open the file in binary read mode
        with open(pathspec, "rb") as f:
            # Read the file in chunks of 4096 bytes
            for byteBlock in iter(lambda: f.read(4096), b""):
                # Update the hash object with the current chunk of bytes
                sha1_hash.update(byteBlock)
        
        # Return the hexadecimal representation of the hash
        return sha1_hash.hexdigest()
    
    except FileNotFoundError as e:
        error_message = f"\n {prefixes[3]} File not found: {pathspec}\n"
        print(error_message)
        with open(file_path, 'a') as file:
            # Append the error message to the 'hash.check' file
            file.write(f"\n {prefixes[3]} File not found: {pathspec}\n")
    except PermissionError:
        # Handle the case where the file cannot be read due to permission issues
        print(f"Permission denied: Unable to read the file {pathspec}.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


# Function to add a file for tracking by calculating its SHA-1 hash and updating the 'hash.check' file
def add(pathspec):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the 'hash.check' file in the script directory
    file_path = os.path.join(script_dir, 'hash.check')

    # Define prefixes for different statuses
    prefixes = {
        1: "[OK]",       # File is added or updated without changes
        2: "[CHANGED]",  # File hash has changed
        3: "[ERROR]"     # Error occurred (e.g., file not found)
    }

    try:
        # Calculate the SHA-1 hash of the specified file
        fileHash = sha1_calculation(pathspec)
        if fileHash is None:
            return
    except FileNotFoundError:
        # Handle the case where the file is not found
        error_message = f" {prefixes[3]} File not found: {pathspec}"
        print(error_message)
        with open(file_path, 'w') as file:
            # Append the error message to the 'hash.check' file
            file.write(f"{prefixes[2]} {old_hash} : {pathspec}")
        return

    try:
        updated = False
        file_found = False
        lines = []
        # Check if the 'hash.check' file exists and read its contents
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

        # Open the 'hash.check' file for writing
        with open(file_path, 'w') as file:
            for i, line in enumerate(lines):
                if pathspec in line:
                    file_found = True
                    old_hash = line.split()[1]
                    if old_hash != fileHash:
                        # If the hash has changed, update the entry
                        file.write(f"\n {prefixes[2]} {old_hash} : {pathspec}")
                        file.write(f"\n NEW HASH: {fileHash}\n")
                        updated = True
                    else:
                        # If the hash has not changed, keep the existing entry
                        file.write(line)
                        if i + 1 < len(lines) and "NEW HASH" in lines[i + 1]:
                            file.write(lines[i + 1])
                else:
                    file.write(line)
            if not file_found:
                # If the file was not found in the 'hash.check' file, add a new entry
                file.write(f"\n {prefixes[1]} {fileHash} : {pathspec}\n")
        
        if updated:
            print(f"Updated file: {prefixes[2]} {fileHash} : {pathspec}")
        elif not file_found:
            print(f"Added (updated) file: {prefixes[1]} {fileHash} : {pathspec}")
    except PermissionError:
        # Handle the case where the file cannot be written due to permission issues
        print(f"Permission denied: Unable to write to the file {file_path}.")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred while adding the file: {e}")

# Function to remove a file from tracking by deleting its entry from the 'hash.check' file
def remove(pathspec):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the 'hash.check' file in the script directory
    file_path = os.path.join(script_dir, 'hash.check')
    
    try:
        # Read the contents of the 'hash.check' file
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Open the 'hash.check' file for writing
        with open(file_path, 'w') as file:
            skip_next = False
            for line in lines:
                if skip_next:
                    skip_next = False
                    continue
                if pathspec in line:
                    # Skip the next line if the current line contains the pathspec
                    skip_next = True
                    continue
                # Write the line to the file if it does not contain the pathspec
                file.write(line)
        
        print(f"Removed file entry: {pathspec}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred while removing the file entry: {e}")

# Function to display the current status of tracked files
def status():
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Define the path to the 'hash.check' file in the script directory
        file_path = os.path.join(script_dir, 'hash.check')
        
        if os.path.exists(file_path):
            # Read and print the contents of the 'hash.check' file
            with open(file_path, 'r') as file:
                lines = file.read()
                print(lines)
            
            # Initialize counters for different statuses
            OK = 0
            CHA = 0
            ERR = 0
            # Count the occurrences of each status in the 'hash.check' file
            with open(file_path, 'r') as file:
                for line in file:
                    OK += line.count('[OK]')
                    CHA += line.count('[CHANGED]')
                    ERR += line.count('[ERROR]')
            # Print the counts of each status
            print(f"[OK]: {OK}, [CHANGED]: {CHA}, [ERROR]: {ERR}")
        else:
            print("File does not exist.")
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred while printing the status: {e}")

# Main function to handle console commands and provide help
def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="\nFILE TRACKING SCRIPT\n")
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the 'init' command
    subparsers.add_parser('init', help="\nInitializes tracking (creates hash.check file).\n")
    
    # Subparser for the 'add' command
    parser_add = subparsers.add_parser('add', help="\nAdds (updates) files to tracking.\n")
    parser_add.add_argument('pathspec', type=str, help="\nPath to the files to add.\n")

    # Subparser for the 'remove' command
    parser_remove = subparsers.add_parser('remove', help="\nRemoves files from tracking.\n")
    parser_remove.add_argument('pathspec', type=str, help="\nPath to the files to remove.\n")

    # Subparser for the 'status' command
    subparsers.add_parser('status', help="\nDisplays status of tracked files.\n")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command == 'init':
        init()
    elif args.command == 'add':
        add(args.pathspec)
    elif args.command == 'remove':
        remove(args.pathspec)
    elif args.command == 'status':
        status()
    elif args.command == '-h':
        parser.print_help()
    else:
        print("Command not recognized")

# Entry point of the script
if __name__ == "__main__":
    main()
