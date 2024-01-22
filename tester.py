from mans import CommandManual, CommandManualGenerator, XmlSerializer

command1 = CommandManual("")

res = command1.generate_manual()

s = XmlSerializer(command_manual=command1)

print(s.generate_xml())