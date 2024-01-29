import subprocess
import re

class CommandManual:
    "a class that just stores the command information"
    def __init__(self, command):
        self.command = command

    def run_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result

    def extract_description(self):
        man_command = "man " + self.command
        result = self.run_command(man_command)
        match = re.search(r'(?<=DESCRIPTION\n)(.*?)(?=\n\n)', result.stdout, re.DOTALL)
        return match.group(1).strip() if match else "No description available"

    def extract_version(self):
        version_command = self.command + " --version"
        result = self.run_command(version_command)
        return result.stdout.split('\n')[0] if result.returncode == 0 else "No version information available"

    def give_example(self):
        man_command = "man " + self.command
        result = self.run_command(man_command)
        match = re.search(r'(?<=EXAMPLES\n)(.*?)(?=\n\n)', result.stdout, re.DOTALL)
        return match.group(1).strip() if match else "No examples available"

    def related_commands(self):
        man_command = "man " + self.command
        result = self.run_command(man_command)
        match = re.search(r'(?<=SEE ALSO\n)(.*?)(?=\n\n)', result.stdout, re.DOTALL)
        return match.group(1).strip() if match else "No related commands available"

    def generate_manual(self):
        return {
            "description": self.extract_description(),
            "version": self.extract_version(),
            "example": self.give_example(),
            "related_commands": self.related_commands()
        }
    def __str__(self):
        "will return a string representation of the command description, version, example, and related commands"
        return f"Command: {self.command}\nDescription: {self.extract_description()}\nVersion: {self.extract_version()}\nExample: {self.give_example()}\nRelated Commands: {self.related_commands()}"


class CommandManualGenerator:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.commands = file.read().splitlines()

    def generate_manuals(self):
        manuals = {}
        for command in self.commands:
            manual = CommandManual(command)
            manuals[command] = manual.generate_manual()
        return manuals
   

class XmlSerializer(): # returns an xml string
    def __init__(self, command_manual):
        self.command_manual = command_manual

    def generate_xml(self):
        return f"""<command>
    <name>\n{self.command_manual.command}\n</name>
    <description>\n{self.command_manual.extract_description()}\n</description>
    <version>\n{self.command_manual.extract_version()}\n</version>
    <example>\n{self.command_manual.give_example()}\n</example>
    <related_commands>\n{self.command_manual.related_commands()}\n</related_commands>
</command>"""
    

    