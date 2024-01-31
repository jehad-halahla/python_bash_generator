#a file that contains the CommandManual class, the CommandManualGenerator class, and the XmlSerializer class
import subprocess
import re
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


class CommandManual:
    "a record class that represents a command manual"
    def __init__(self, command="", description="", version="", example="", example_output="", related_commands=None):
        self.command = command
        self.description = description
        self.version = version
        self.example = example
        self.example_output = example_output
        self.related_commands = related_commands
        try:
            if related_commands is None and not isinstance(related_commands, list) and not isinstance(related_commands, str):
                self.related_commands = []
            elif isinstance(related_commands, str):
                self.related_commands = list(related_commands.split(","))
                self.related_commands = related_commands
        except TypeError:
            print("Related commands must be a list")
            print("Setting related commands to an empty list")
            self.related_commands = []

    def get_command(self):
        "returns the name of the command"
        return self.command
    
    def get_description(self):
        "returns the description of the command"
        return self.description
    
    def get_version(self):
        "returns the version of the command"
        return self.version
    
    def get_example(self):
        "returns the example of the command"
        return self.example
    
    def get_example_output(self):
        "returns the example output of the command"
        return self.example_output
    
    def get_related_commands(self):
        "returns the related commands of the command"
        return self.related_commands.copy()
    
    def __str__(self):
        "returns a string representation of the command manual"
        return f"Command: {self.command}\nDescription: {self.description}\nVersion: {self.version}\nExample: {self.example}\nExample Output:\n{self.example_output}\nRelated Commands: {self.related_commands}"
    
class CommandManualGenerator:
    "a record class that represents a command manual generator"

    def __init__(self, file_path):
        self.file_path = file_path
        self.keys = {
        "display":[],
        "file":[],
        "change":[],
        "directory":[],
        "user":[],
        "dest": []
        }
    
    def get_file_path(self):
        "returns the file path of the command manual generator"
        return self.file_path
    
    def read_file(self):
        "returns the contents of the file"
        try:
            with open(self.file_path, 'r') as file:
                lst =  file.read().splitlines()
                for comm in lst:
                    if not self.check_valid_command(comm):
                        lst.remove(comm)
                return lst
        except FileNotFoundError:
            print("File not found")
            return []
        
    def make_all_manuals(self):
        "makes all the manuals"
        comms = self.read_file()
        manuals = []
        for command in comms:
            desc = self.extract_description(command)
            version = self.extract_version(command)
            example,example_out = self.generate_example(command)
            related_commands = self.extract_related_commands(command)
            command = CommandManual(command, desc, version, example, example_out, related_commands)
            manuals.append(command)
        return manuals
    
    def make_manual(self,command):
        "makes a manual for a specific command"
        desc = self.extract_description(command)
        version = self.extract_version(command)
        example,example_out = self.generate_example(command)
        related_commands = self.extract_related_commands(command)
        command = CommandManual(command, desc, version, example, example_out, related_commands)
        return command
    
    def check_valid_command(self,command):
        "checks if the command given is valid or not"
        try:
            res = subprocess.run("man " +command, shell=True, capture_output=True, text=True)
            return res.returncode == 0
        except subprocess.CalledProcessError:
            return False
        
    def run_command(self, command):
        "runs the command given and returns the result as a completed process"
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result
        except subprocess.CalledProcessError:
            return None

    def get_original_manual(self, command):
        "a function that returns the original manual"
        if self.check_valid_command(command):
            res = subprocess.run("man " + command, shell=True,text=True, capture_output=True)
            return res.stdout
        else:
            print("Command not found")
            return None

    def extract_description(self, command):
        "extracts a clean description of the command given"
        man_command = "man " + command
        result = self.run_command(man_command) #obtain the whole manual
        match = re.search(r'(?<=DESCRIPTION\n)(.*?)(?=\n\n)', result.stdout, re.DOTALL)#use regex to get the description
        description = match.group(1) if match else "No description available"
        description = "\n".join([line.strip() for line in description.splitlines()])#remove whitespace
        return description
    
    def extract_version(self, command):
        "extracts the version of the command given"
        version_command = command + " --version"
        result = self.run_command(version_command)
        if command == "pwd":
            result = self.run_command("/bin/pwd --version")
            return result.stdout.split('\n')[0] if result.returncode == 0 else "No version information available"
        return result.stdout.split('\n')[0] if result.returncode == 0 else "No version information available"
    
    def extract_related_commands(self, command):
        "extracts a list of related commands of the command given"
        result = subprocess.run(f"bash -c 'apropos {command}'", shell=True, capture_output=True, text=True)
    
        # we will only take the first part of the output (before the "(") 
        commands = [cmd.split('(')[0].strip() for cmd in result.stdout.split('\n') if result.returncode == 0 and cmd and cmd != command and len(cmd) <= 10]
    
        # now we will check the see also section of the manual
        block = self.get_original_manual(command)
        res = re.search(r'(?<=SEE ALSO\n)(.*?)(?=\n\n)', block, re.DOTALL)
        
        # now we will clean the result
        res = [line.strip().split('(')[0] for line in res.group(1).split(',') if re.search(r'[a-zA-Z]+\([0-9]+\)', line)] if res else []
        
        final_res = list(set(res + commands[0:3]))
        # if the list is still empty, add some commands from compgen -c {command}
        if not final_res:
            compgen_result = subprocess.run(f"bash -c 'compgen -c {command}'", shell=True, capture_output=True, text=True)
            compgen_commands = [cmd for cmd in compgen_result.stdout.split('\n') if compgen_result.returncode == 0 and cmd and cmd != command]
            final_res += compgen_commands
        
        # remove the command itself and the empty string
        final_res = [i for i in final_res if i and i != command]

        #brute force the remaining commands
        if not final_res:
            if command == "whoami":
                final_res += ["who","id"]
            elif command == "chmod":
                final_res += ["chown","chgrp"]
            elif command == "chown":
                final_res += ["chmod","chgrp"]
            elif command == "date":
                final_res += ["cal","hwclock"]

        return final_res
        
    def generate_example(self, command):
        "generates an example of the command given"
        example = command
        result = self.run_command(example)
        if result:
            return example,'\n'.join(result.stdout.split('\n')[:10])
        else:#case for cp,mv,chgrp,chmod,chown
            if command == "chmod":
                example = "chmod 777 file.txt && ls -l file.txt"
                result = self.run_command(example)
                
            elif command == "chgrp":
                example = "chgrp jehad file.txt && ls -l file.txt"
                result = self.run_command(example)
               
            elif command == "chown":
                example = "chown jehad file.txt && ls -l file.txt"
                result = self.run_command(example)
               
            elif command == "mv":
                #create a directory using the os module
                if not os.path.exists("temp"):
                    os.mkdir("temp")
                #now we will make a file1.txt if it doesn't exist
                if not os.path.exists("mv1.txt"):
                    with open("mv1.txt", 'w') as file:
                        file.write("Hello World")
                example = "mv mv1.txt temp/mv2.txt && ls -l temp/mv2.txt"
                result = self.run_command(example)
    
            elif command == "cp":
                #create a directory using the os module
                if not os.path.exists("temp"):
                    os.mkdir("temp")
                #now we will make a cp1.txt if it doesn't exist
                if not os.path.exists("cp1.txt"):
                    with open("cp1.txt", 'w') as file:
                        file.write("Hello World")
                example = "cp cp1.txt temp/cp2.txt && ls -l temp/cp2.txt"
                result = self.run_command(example)

            return example,result.stdout if result else "No example available"
                

    def obtain_recommendation(self,command):
        "a function that obtains a recommendation for the command given"
        #first we will check if the command is in the keys dictionary
        matching = []
        for key in self.keys:
            if command in self.keys[key]:
                matching += self.keys[key]
        relatedSet = set(matching)
        relatedSet.remove(command)
        return list(relatedSet)

    def make_groups(self):
        "a function that makes a group of commands"
        comms = self.read_file()
        for key in self.keys:
            for command in comms:
                desc = self.extract_description(command)
                if re.search(fr'{key}', desc, re.IGNORECASE):
                    self.keys[key].append(command)
        #uname,ifconfig, lscpu still don't have groups, just add them manually
        self.keys["display"].append("uname")
        self.keys["display"].append("ifconfig")
        self.keys["display"].append("lscpu")
    
    def write_to_file(self, manuals):
        "a function that writes the manuals xml string to xml docs"
        if not os.path.exists("manuals"):
            os.mkdir("manuals")
        for manual in manuals:
            serializer = XmlSerializer()
            xml_string = serializer.serialize(manual)
            with open(f"manuals/{manual.command}.xml", 'w') as file:
                file.write(xml_string)
        
    def make_single_xml(self, command):
        "a function that makes a single xml file for a command"
        if not os.path.exists("manuals"):
            os.mkdir("manuals")
        serializer = XmlSerializer()
        manual = self.make_manual(command)
        xml_string = serializer.serialize(manual)
        with open(f"manuals/{manual.command}.xml", 'w') as file:
            file.write(xml_string)
            
class XmlSerializer:
    "a class that serializes CommandManual objects to XML strings"
    def serialize(self, command_manual):
        if not isinstance(command_manual, CommandManual):
            raise TypeError("CommandManual object expected")
        
        root = ET.Element("CommandManual")

        command = ET.SubElement(root, "command")
        command.text = command_manual.command

        description = ET.SubElement(root, "description")
        description.text = command_manual.description

        version = ET.SubElement(root, "version")
        version.text = command_manual.version

        example = ET.SubElement(root, "example")
        example.text = command_manual.example

        example_output = ET.SubElement(root, "example_output")
        example_output.text = '\n' + command_manual.example_output

        related_commands = ET.SubElement(root, "related_commands")
        if command_manual.related_commands:
            related_commands.text = ', '.join(command_manual.related_commands)

        xml_string = ET.tostring(root, encoding='unicode')
        dom = parseString(xml_string)
        pretty_xml = dom.toprettyxml()

        return pretty_xml