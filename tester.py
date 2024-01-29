from manuals import *


gen = CommandManualGenerator("commands.txt")
gen.make_groups()
manuals = gen.make_all_manuals()

for manual in manuals:
    print(manual)
    print("#"*50)
