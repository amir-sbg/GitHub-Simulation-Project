def printHelp():
    helpStr = "-help:  To show the help list\n\n"
    helpStr = helpStr + "push:   push –m “commit message” –f “./dir/file”"
    print(helpStr)


def parseInput(command):

    messageToSend = ""
    command = str(command)
    if command.startswith("-help"):
        printHelp()
        return

    if command.startswith("signup"):
        name = input("Enter your name: ")
        password1 = input("Enter you password: ")
        password2 = input("Renter you password: ")
        if password1 == password2:
            messageToSend = messageToSend + "1$"
            messageToSend = messageToSend + name + "$"
            messageToSend = messageToSend + password1 + "$"
        else:
            print("Password doesn't match\n\n")

    if command.startswith("signin"):
        name = input("Enter your name: ")
        password = input("Enter you password: ")
        messageToSend = messageToSend + "2$"
        messageToSend = messageToSend + name + "$"
        messageToSend = messageToSend + password + "$"

    if command.startswith("mkdir"):
        parts = command.split()
        messageToSend = messageToSend + "3$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("list"):
        messageToSend = messageToSend + "4$"

    if command.startswith("choose"):
        parts = command.split()
        messageToSend = messageToSend + "5$"
        messageToSend = messageToSend + parts[1] + "$"

    if command.startswith("push"):
        parts = command.split()
        commitMessage = command.split("\"")[1]
        # TODO: uncomment next line and delete the line after that
        # data = amirFunction(parts[-2], parts[-1])
        data = "101010101011111100000011111111110"
        messageToSend = messageToSend + "6$"
        messageToSend = messageToSend + commitMessage + "$"
        messageToSend = messageToSend + data + "$"

    if command.startswith("pull"):
        parts = command.split()
        messageToSend = messageToSend + "7$"
        messageToSend = messageToSend + parts[-1] + "$"

    return messageToSend


