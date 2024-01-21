import subprocess,re

def run_command(command): # runs the command and captures output, error and return code
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result

def make_directory(directory_name):
    command = "mkdir " + directory_name
    result = run_command(command)
    return result

def check_directory_exists(directory_name):
    command = "ls " + directory_name
    result = run_command(command)
    return result.returncode == 0

def extract_version(command):
    result =  run_command(command+" --version")
    if result.returncode == 0:
        #we will pipe the result to head command to get the first line
        print(result.stdout.split('\n')[0])
    else:
        print(f"Error: {result.stderr}")

def extract_description(command):
    man_command = "man " + command 
    result = run_command(man_command)
    match = re.search(r'(?<=DESCRIPTION\n)(.*?)(?=\n\n)', result.stdout, re.DOTALL)
    if match:
        description = match.group(1)
        #we will strip all the new line characters
        description = '\n'.join(line.lstrip() for line in description.split('\n'))
        print(description)

        
    else:
        print(f'No description found for {command}')


# we will check of commands in the commands.txt file

# Reading the commands from the file
with open("commands.txt", "r") as file:
    commands = file.readlines()

for command in commands:
    command = command.strip() # removing the new line character
    
    #extracting the version
    print(command)
    extract_description(command)
    extract_version(command)
    
print("=========================================")
