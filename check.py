import argparse  # Imports argparse to handle command-line arguments
import hashlib  # Imports hashlib for generating hash values (SHA1 in this case)
import os  # Imports os for handling file and directory operations

# Function to create a hash.check file if it doesn't exist
def init():
    # Get the current directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the path to the hash.check file in the same directory as the script
    file_path = os.path.join(script_dir, 'hash.check')

    try:
        # If hash.check already exists, ask if the user wants to recreate it
        if os.path.exists(file_path):
            print(f"File 'hash.check' already exists in the directory: {script_dir}")
            remakeCom = input("Do you want to remake it? (y/n): ").strip().lower()
            # If the user wants to remake it, remove the old file and create a new one
            if remakeCom == 'y':
                os.remove(file_path)
                with open(file_path, 'w') as file:
                    file.write("Welcome to hash.check")
                    file.write("\n")
                print(f"File 'hash.check' has been recreated in the directory: {script_dir}")
            # If the user doesn't want to remake, leave the file unchanged
            elif remakeCom == 'n':
                print("File 'hash.check' was not modified.")
            else:
                print("Command not recognized.")
        else:
            # If the file doesn't exist, create it and write a welcome message
            with open(file_path, 'w') as file:
                file.write("Welcome to hash.check")
            print(f"File 'hash.check' has been created in the directory: {script_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to calculate the SHA1 hash of a file
def sha1_calculation(pathspec):
    sha1_hash = hashlib.sha1()  # Create a new SHA1 hash object
    with open(pathspec, "rb") as f:  # Open the file in binary mode
        for byteBlock in iter(lambda: f.read(4096), b""):  # Read file in 4k chunks
            sha1_hash.update(byteBlock)  # Update the hash object with the chunk of data
    return sha1_hash.hexdigest()  # Return the hexadecimal hash

# Function to add a file to the tracking list or update its hash if it already exists
def add(pathspec):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    file_path = os.path.join(script_dir, 'hash.check')  # Path to the hash.check file

    # Define prefixes for the different statuses of a file
    prefixes = {
        1: "[OK]",        # File is intact and hasn't changed
        2: "[CHANGED]",   # File's hash has changed
        3: "[ERROR]"      # Error occurred while processing the file
    }

    try:
        # Calculate the SHA1 hash of the file to be added
        fileHash = sha1_calculation(pathspec)
    except FileNotFoundError:
        # If file not found, write an error message to hash.check
        error_message = f" {prefixes[3]} File not found: {pathspec}"
        print(error_message)
        with open(file_path, 'a') as file:
            file.write(f"\n{error_message}\n")
        return

    try:
        updated = False  # Flag to track if the file was updated
        file_found = False  # Flag to track if the file was already in the hash.check file
        lines = []  # List to hold the file lines from hash.check
        # If hash.check exists, read its lines
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

        with open(file_path, 'w') as file:
            for i, line in enumerate(lines):
                # Check if the file is already tracked in the hash.check file
                if pathspec in line:
                    file_found = True
                    old_hash = line.split()[1]  # Extract the old hash from the line
                    # If the hash has changed, update the file with the new hash
                    if old_hash != fileHash:
                        file.write(f"\n {prefixes[2]} {old_hash} : {pathspec}")
                        file.write(f"\n NEW HASH: {fileHash}\n")
                        updated = True
                    else:
                        file.write(line)  # Keep the line unchanged if the hash is the same
                        if i + 1 < len(lines) and "NEW HASH" in lines[i + 1]:
                            file.write(lines[i + 1])  # Keep the new hash entry intact
                else:
                    file.write(line)
            # If the file wasn't found, add it as a new entry
            if not file_found:
                file.write(f"\n {prefixes[1]} {fileHash} : {pathspec}\n")
        
        # Print update or addition message
        if updated:
            print(f"Updated file: {prefixes[2]} {fileHash} : {pathspec}")
        elif not file_found:
            print(f"Added (updated) file: {prefixes[1]} {fileHash} : {pathspec}")
    except Exception as e:
        print(f"An error occurred while adding the file: {e}")

# Function to remove a file from tracking
def remove(pathspec):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    file_path = os.path.join(script_dir, 'hash.check')  # Path to the hash.check file
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()  # Read all lines from hash.check
        
        with open(file_path, 'w') as file:
            skip_next = False  # Flag to skip a line when removing an entry
            for line in lines:
                if skip_next:
                    skip_next = False
                    continue
                if pathspec in line:
                    skip_next = True  # Skip the next line (the one to be removed)
                    continue
                file.write(line)
        
        print(f"Removed file entry: {pathspec}")  # Print removal confirmation
    except Exception as e:
        print(f"An error occurred while removing the file entry: {e}")

# Function to display the current status of tracked files
def status():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
        file_path = os.path.join(script_dir, 'hash.check')  # Path to the hash.check file
        
        # If hash.check exists, read and print its contents
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.read()
                print(lines)
            # Counters for different statuses
            OK = 0
            CHA = 0
            ERR = 0
            with open(file_path, 'r') as file:
                for line in file:
                    OK += line.count('[OK]')  # Count '[OK]' entries
                    CHA += line.count('[CHANGED]')  # Count '[CHANGED]' entries
                    ERR += line.count('[ERROR]')  # Count '[ERROR]' entries
            print(f"[OK]: {OK}, [CHANGED]: {CHA},[ERROR]: {ERR} ")  # Print status summary
        else:
            print("File does not exist.")  # If the file doesn't exist
    except Exception as e:
        print(f"An error occurred while printing the status: {e}")

# Main function to handle command-line interface (CLI) commands
def main():
    parser = argparse.ArgumentParser(description="File tracking script.")  # Initialize argument parser
    subparsers = parser.add_subparsers(dest="command")  # Create subparsers for different commands

    subparsers.add_parser('init', help="Initializes tracking (creates .check file).")  # init command

    # Add subparser for the 'add' command to track files
    parser_add = subparsers.add_parser('add', help="Adds (updates) files to tracking.")
    parser_add.add_argument('pathspec', type=str, help="Path to the files to add.")  # Add argument for pathspec

    # Add subparser for the 'remove' command to remove files from tracking
    parser_remove = subparsers.add_parser('remove', help="Removes files from tracking.")
    parser_remove.add_argument('pathspec', type=str, help="Path to the files to remove.")  # Add argument for pathspec

    subparsers.add_parser('status', help="Displays status of tracked files.")  # status command
    subparsers.add_parser('exit', help="Exits the program")  # exit command
    

    # Infinite loop to prompt user for commands
    while True:
        command = input("Enter command: ").split()  # Prompt user for a command
        try:
            args = parser.parse_args(command)  # Parse the entered command
        except SystemExit:
            parser.print_help()  # Print help if arguments are invalid
            continue

        # Handle the different commands
        if args.command == 'init':
            init()  # Call init function
        elif args.command == 'add':
            add(args.pathspec)  # Call add function with the specified file path
