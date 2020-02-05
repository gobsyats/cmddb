# File Name: Main File (Program Entry Point)
# Date of Creation: 01/30/2020
# @Author: Govind Yatnalkar

import commans
import constants

#Dictionary to handle integer setting, un-setting and getting
dataDict = dict()

#Dictionary to hold old variables for rollback
oldKeyValDict = dict()
newKeyValDict = dict()

#Counter for maching number of variables
keyWithValues = 0

#List to get the keys of values which are set
getKeysToPrint = []

#String variable to save and analyse user entered commands
command = ""

#A Variable to keep a track of number of transactions
transNo = 0

#Print help
print("**************************CMD BASED DATABASE****************************")
print("Welcome to the Integer Saving Program")
print("Commands include:")
print("SET or set - setting the value of an integer")
print("GET or get - getting the value of an integer which is set")
print("UNSET or unset - remove/ unset the value of an integer")
print("NUMWITHVALUE or numwithvalue - get the number of integers that have values")
print("BEGIN or begin - begin a transaction")
print("ROLLBACK or rollback - rollback a transaction or revert to previous changes")
print("COMMIT or commit - permanently save changes")
print("END or end - terminate the integer processing and get output")
print("Please start and specify your command...")
commans.printColored("Warnings are specified in yellow.", constants.CYELLOW)
commans.printColored("Errors are specified in red.", constants.CRED2)

loopState = True
while loopState == True:
    command = str(input(""))
    split_command = command.split(" ")

    #SET METHOD CALL
    if split_command[0] == constants.SET or split_command[0] == constants.set:
            dataDict, keyWithValues = commans.setBlock(command, dataDict, keyWithValues, getKeysToPrint)

    #GET METHOD CALL
    elif split_command[0] == constants.GET or split_command[0] == constants.get:
        getKeysToPrint = commans.getBlockOnePrint(dataDict, command, getKeysToPrint)

    #UNSET METHOD CALL
    elif split_command[0] == constants.UNSET or split_command == constants.unset:
        dataDict, keyWithValues, getKeysToPrint = commans.unsetBlock(command, dataDict, keyWithValues, getKeysToPrint)

    #NUMWITHVALUE METHOD CALL
    elif command == constants.numwithvalues or command == constants.NUMWITHVALUES:
        commans.numValuesBlock(dataDict)

    #END METHOD CALL
    elif command == constants.END or command[0] == constants.end:
        print.printColored("Thank you for visiting the CMD based Database Application.")
        print("Application Ended...")
        loopState = False

    #BEGIN, COMMIT and ROLLBACK
    elif command == constants.BEGIN or command == constants.begin:
        commandCount = 0
        transCommands = ""
        switch = True
        commit_flag = False
        while switch == True:
            transCommands = str(input(""))
            dataDict, keyWithValues, getKeysToPrint, oldKeyValDict, newKeyValDict, commandCount, commit_flag = \
                commans.beginBlockAdv(transCommands, dataDict, keyWithValues, getKeysToPrint, oldKeyValDict, newKeyValDict, commandCount, commit_flag)
            if transCommands == constants.COMMIT or transCommands == constants.ROLLBACK:
                switch = False
    #IF NO TRANSACTION IS IN PROCEDDING
    elif command == constants.COMMIT or command == constants.ROLLBACK or command == constants.commit or command == constants.rollback:
        commans.printColored("No Transactions to COMMIT or ROLLBACK. All previous transactions are closed.", constants.CYELLOW)
        commans.printColored("Please use BEGIN command to start a transaction followed by a COMMIT or ROLLBACK.", constants.CYELLOW)
    else:
        commans.printColored("The command did not match with any of our existing commands.", constants.CRED2)
        commans.printColored("Please try with SET, GET, UNSET, BEGIN, ROLLBACK, COMMIT, NUMWITHVALUE or END", constants.CRED2)

