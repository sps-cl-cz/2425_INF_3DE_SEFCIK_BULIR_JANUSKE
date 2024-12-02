import argparse
import hashlib
import glob
import os

#function for creating hash.check file
def init():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'hash.check')
    try:
        if os.path.exists(file_path):
            print(f"File 'hash.check' already exists in the directory: {script_dir}")
            remakeCom = input("Do you want to remake it? (y/n): ").strip().lower()
            if remakeCom == 'y':
                os.remove(file_path)
                with open(file_path, 'w') as file:
                    file.write("Welcome to hash.check")
                    file.write("\n")
                print(f"File 'hash.check' has been recreated in the directory: {script_dir}")
            elif remakeCom == 'n':
                print("File 'hash.check' was not modified.")
            else:
                print("Command not recognized.")
        else:
            with open(file_path, 'w') as file:
                file.write("Welcome to hash.check")
            print(f"File 'hash.check' has been created in the directory: {script_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")

#sha1 hash calculation
def sha1_calculation(pathspec):
    sha1_hash = hashlib.sha1()
    with open(pathspec, "rb") as f:
        for byteBlock in iter(lambda: f.read(4096), b""):
            sha1_hash.update(byteBlock)
    return sha1_hash.hexdigest()

#adding files for tracking
def add(pathspec):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'hash.check')

    prefixes = {
        1: "[OK]",
        2: "[CHANGED]",
        3: "[ERROR]"
    }

    try:
        fileHash = sha1_calculation(pathspec)
    except FileNotFoundError:
        error_message = f" {prefixes[3]} File not found: {pathspec}"
        print(error_message)
        with open(file_path, 'a') as file:
            file.write(f"\n{error_message}\n")
        return

    try:
        updated = False
        file_found = False
        lines = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

        with open(file_path, 'w') as file:
            for i, line in enumerate(lines):
                if pathspec in line:
                    file_found = True
                    old_hash = line.split()[1]
                    if old_hash != fileHash:
                        file.write(f"\n {prefixes[2]} {old_hash} : {pathspec}")
                        file.write(f"\n NEW HASH: {fileHash}\n")
                        updated = True
                    else:
                        file.write(line)
                        if i + 1 < len(lines) and "NEW HASH" in lines[i + 1]:
                            file.write(lines[i + 1])
                else:
                    file.write(line)
            if not file_found:
                file.write(f"\n {prefixes[1]} {fileHash} : {pathspec}\n")
        
        if updated:
            print(f"Updated file: {prefixes[2]} {fileHash} : {pathspec}")
        elif not file_found:
            print(f"Added (updated) file: {prefixes[1]} {fileHash} : {pathspec}")
    except Exception as e:
        print(f"An error occurred while adding the file: {e}")


#removing files from tracking
def remove(pathspec):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'hash.check')
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as file:
            skip_next = False
            for line in lines:
                if skip_next:
                    skip_next = False
                    continue
                if pathspec in line:
                    skip_next = True
                    continue
                file.write(line)
        
        print(f"Removed file entry: {pathspec}")
    except Exception as e:
        print(f"An error occurred while removing the file entry: {e}")

#display current status of tracked files
def status():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'hash.check')
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.read()
                print(lines)
            OK = 0
            CHA = 0
            ERR = 0
            with open(file_path, 'r') as file:
                for line in file:
                    OK += line.count('[OK]')
                    CHA += line.count('[CHANGED]')
                    ERR += line.count('[ERROR]')
            print(f"[OK]: {OK}, [CHANGED]: {CHA},[ERROR]: {ERR} ")
        else:
            print("File does not exist.")
    except Exception as e:
        print(f"An error occurred while printing the status: {e}")

#main function with console commands and help
def main():
    parser = argparse.ArgumentParser(description="File tracking script.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser('init', help="Initializes tracking (creates .check file).")
    
    parser_add = subparsers.add_parser('add', help="Adds (updates) files to tracking.")
    parser_add.add_argument('pathspec', type=str, help="Path to the files to add.")

    parser_remove = subparsers.add_parser('remove', help="Removes files from tracking.")
    parser_remove.add_argument('pathspec', type=str, help="Path to the files to remove.")

    subparsers.add_parser('status', help="Displays status of tracked files.")
    subparsers.add_parser('exit', help="Exits the program")
    

    while True:
        command = input("Enter command: ").split()
        try:
            args = parser.parse_args(command)
        except SystemExit:
            parser.print_help()
            continue

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
        elif args.command == 'exit':
            exit()
        else:
            print('Command not recognized')

if __name__ == "__main__":
    main()
