#this file contains the verifier class, which checks the validity of the manuals generated in manuals directory
import os
from manuals import *

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

class Verifier:
    "This class verifies the validity of a single manual generated in manuals directory"
    def __init__(self, filename):
        self.generator = CommandManualGenerator(filename)
        self.filename = filename

    def verify(self,command):
        manual = ""
        "This method verifies the validity of a single manual generated in manuals directory"
        for file in os.listdir('./manuals'): 
            if file == f'{command}.xml':
                with open(f'./manuals/{file}', 'r') as f:
                    manual = f.read()
                break
        else:
            print(f'{command}.xml not found')
        #now with the manual, we can verify it
        #make a test
        test = self.generator.make_manual(command)
        serializer = XmlSerializer()
        test_xml = serializer.serialize(test)
        #compare the two
        test_lines = test_xml.splitlines()
        manual_lines = manual.splitlines()
        diff_lines = []

        # Iterate over both lists simultaneously
        for line_num, (test_line, manual_line) in enumerate(zip(test_lines, manual_lines), 1):
            if test_line != manual_line:
                diff_lines.append(f'{RED}- Line {line_num}: {test_line}{RESET}')
                diff_lines.append(f'{GREEN}+ Line {line_num}: {manual_line}{RESET}')

        # Join the diff_lines list into a string with newline characters between each line
        diff_string = '\n'.join(diff_lines)

        # Print the diff_string
        print(diff_string)

        if diff_string == "":
            print(f'{GREEN}Everything is Consistent!!{RESET}')
