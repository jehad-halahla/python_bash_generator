from manuals import *
from verification import *
import os

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def search(command):
    res= ""
    if os.path.exists(f'./manuals/{command}.xml'):
        try:
            file = open(f'./manuals/{command}.xml', 'r')
            res = file.read()
            file.close()
            return res

        except IOError:
            print(f"{RED}Error: File does not appear to exist.{RED}")
            return None
    else:
        print(f'{RED}{command}.xml not found{RESET}, you can generate it by choosing option 2')
        return None

    


generator = CommandManualGenerator("commands.txt") #will be used alot
generator.make_groups()

commands = generator.read_file() #will be used alot
while True:
    print("\nPlease choose an option:")
    print("1. Batch generate all manuals")
    print("2. Generate for a single command")
    print("3. Search for a specific command")
    print("4. Verify command")
    print("5. Exit")

    choice = input("\nEnter your choice: ")

    if choice == '1':
        # Call the function to batch generate all manuals
        manuals = generator.make_all_manuals()
        generator.write_to_file(manuals)# generates all xml files
        #print green text that says "All manuals generated successfully"
        print(GREEN + "All manuals generated successfully" + RESET)


    elif choice == '2':
        command = input("Enter the command: ")
        # Call the function to generate for a single command
        if command not in commands:
            print(RED + "Command not found" + RESET)
        else:
            generator.make_single_xml(command)
            #print green text that says "Manual generated successfully"
            print(GREEN + "Manual generated successfully" + RESET)

    elif choice == '3':
        command = input("Enter the command: ")
        # Call the function to search for a specific command
        if command not in commands:
            print(RED + "Command not found" + RESET)
        else:
            res = search(command)
            if res != None:
                print(res)
                recommended = generator.obtain_recommendation(command)
                print(f"{GREEN}Recommended commands: {RESET}")
                for comm in recommended:
                    print(comm)
                #also show commands that have the command as a substring
                print(f"{GREEN}Commands that have {command} as a substring: {RESET}")
                for comm in commands:
                    if comm.find(command) != -1 and command != comm:
                        print(comm)


    elif choice == '4':
        command = input("Enter the command: ")
        # Call the function to verify command
        if command not in commands:
            print(RED + "Command not found" + RESET)
        else:
            verifier = Verifier(command)
            verifier.verify(command)
            

    elif choice == '5':
        print("Exiting...")
        break
    else:
        print(f"{RED}ERROR: Invalid choice. Please enter a number between 1 and 5.{RESET}")   