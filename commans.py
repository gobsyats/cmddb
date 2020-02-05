# File Name: Commons (All Project Methods)
# Date of Creation: 01/30/2020
# @Author: Govind Yatnalkar
import commans
import constants

#String Split for splitting the commands
def stringSplit(str):
    return str.split(" ")

#Method to validate if the 3rd argument is an integer
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#Method for "SET"
def setBlock(command, dataDict, keyWithValues, getKeysToPrint):
    context = stringSplit(command)
    # If 3 arguments not found in set command
    if len(context) != 3:
        printColored("Found invalid number of arguments. Please make sure the SET command has 2 arguments. Example: SET varname 10.", constants.CRED)
    else:
        key = context[1]
        value = context[2]
        #Check if third argument is an integer
        checkIntFlag = RepresentsInt(value)
        if checkIntFlag is False or value == " " or value == "" or value is None:
            printColored("Please enter a valid integer for the third argument. Example: SET varname 10.", constants.CRED)
        else:
            if key in dataDict:
                if dataDict[key] is constants.NONE and value is not constants.NONE:
                    keyWithValues += 1
            else:
                keyWithValues += 1
            #Set the value in dictionary
            dataDict[key] = int(value)
    return dataDict, keyWithValues

#Method for "GET", Print one variables at a time in a transaction
def getBlockOnePrint(dataDict, command, getKeysToPrint):
    context = stringSplit(command)
    if len(context) != 2:
        printColored("Found invalid number of arguments. Please make sure the GET command has 1 argument. Example: GET varname.", constants.CRED)
    else:
        key = context[1]
        if key in dataDict:
            value = dataDict[key]
            print(key, ":", value)
            if key in getKeysToPrint:
                ""
            else:
                if dataDict[key] is not constants.NONE:
                    getKeysToPrint.append(key)
        else:
            #Key not present in the dictionary
            printColored("Data not present for the stated key. Please retry GET command with another key.", constants.CRED)
    return getKeysToPrint

#Method for "GET", Print all variables after transaction end
def getBlockEndPrint(dataDict, command, getKeysToPrint):
    context = stringSplit(command)
    if len(context) != 2:
        printColored("Found invalid number of arguments. Please make sure the GET command has 1 argument. Example: GET varname.", constants.CRED)
    else:
        key = context[1]
        if key in dataDict:
            if key in getKeysToPrint:
                # Key already present in final key printing list
                ""
            else:
                if dataDict[key] is not constants.NONE:
                    getKeysToPrint.append(key)
        else:
            printColored("Data not present for the stated key. Please retry GET command with another key again.", constants.CRED)
    return getKeysToPrint

#Method for "UNSET"
def unsetBlock(command, dataDict, keyWithValues, getKeysToPrint):
    context = stringSplit(command)
    if len(context) != 2:
        printColored("Found invalid number of arguments. Please make sure the UNSET command has 1 argument. Example: UNSET varname.", constants.CRED)
    else:
        key = context[1]
        if key in dataDict:
            value = dataDict[key]
            if key in dataDict and value == None:
                printColored("The value for the key is already unset or not found.", constants.CYELLOW)
            elif key in dataDict and value != None:
                dataDict[key] = constants.NONE
                #if key in getKeysToPrint:
                #    getKeysToPrint.remove(key)
                #else:
                #    print("The value for the key is already unset or not found.")
                if keyWithValues < 1:
                    printColored("Number of Keys with Set Value is 0", constants.CYELLOW)
                else:
                   #decrease the counter for unsetting the value
                   keyWithValues = keyWithValues - 1
        else:
            printColored("Data not present for the stated key. Please try with another key again.", constants.CRED)
    return dataDict, keyWithValues, getKeysToPrint

#Method for "NUMWITHVALUE"
def numValuesBlock(dataDict):
    noOfKeysSet = 0
    for key, value in dataDict.items():
        if value != None:
            print(key, ":", value)
            noOfKeysSet += 1
    print("Number of Keys set with Values are ", noOfKeysSet)

#Method for "BEGIN"
def beginBlockAdv(transCommands, dataDict, keyWithValues, getKeysToPrint, oldKeyValDict, newKeyValDict, commandCount, commit_flag):
    context = stringSplit(transCommands)
    actualCommand = context[0]  # SET, UNSET, GET, NUMWITHVALUE

    #SET in a transaction
    if actualCommand == constants.SET or actualCommand == constants.set:
        if len(context) == 3:
            commandCount += 1
            key = context[1]  # ex, ey
            value = context[2]  # 10, 20
            if key in dataDict and key not in oldKeyValDict:
                oldValue = dataDict[key]
                oldKeyValDict[key] = oldValue
            elif key not in dataDict:
                newKeyValDict[key] = value
        dataDict, keyWithValues = setBlock(transCommands, dataDict, keyWithValues, getKeysToPrint)

    #GET in a transaction
    elif actualCommand == constants.GET or actualCommand == constants.get:
        getKeysToPrint = getBlockOnePrint(dataDict, transCommands, getKeysToPrint)

    #NUMWITHVALUE in a transaction
    elif actualCommand == constants.NUMWITHVALUES or actualCommand == constants.numwithvalues:
         numValuesBlock(dataDict)

    #UNSET in a transaction
    elif actualCommand == constants.UNSET or actualCommand == constants.unset:
        if len(context) == 2:
            commandCount += 1
            key = context[1]  # ex, ey
            if key in dataDict and key not in oldKeyValDict:
                oldValue = dataDict[key]
                oldKeyValDict[key] = oldValue
            dataDict, keyWithValues, getKeysToPrint = unsetBlock(transCommands, dataDict, keyWithValues, getKeysToPrint)

    #COMMIT in a transaction
    elif actualCommand == constants.COMMIT or actualCommand == constants.commit:
        if commit_flag is True:
            printColored("All previous transactions have been completed and closed. Please start a new transaction with BEGIN.", constants.CYELLOW)
        else:
            if commandCount < 1:
                print("No Transaction.")
            else:
                oldKeyValDict.clear()
                newKeyValDict.clear()
    elif actualCommand == constants.ROLLBACK or actualCommand == constants.rollback:
        if commit_flag is True:
            printColored(
                "All previous transactions have been completed and closed. Please start a new transaction with BEGIN.", constants.CYELLOW)
        else:
            if commandCount < 1:
                print("No Transaction.")
            else:
                for key, val in oldKeyValDict.items():
                    if key in dataDict:
                        dataDict[key] = val
                oldKeyValDict.clear()

                for key, val in newKeyValDict.items():
                    if key in dataDict:
                        dataDict.pop(key);
                newKeyValDict.clear()

    #Recursive Begin Method (Nested Transactions)
    elif actualCommand == constants.BEGIN or actualCommand == constants.begin:
        commandCount1 = 0
        newKeyValDict1 = {}
        oldKeyValDict1 = {}
        dataDict, keyWithValues1, getKeysToPrint1, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag = \
            beginStartBlock(dataDict, keyWithValues, getKeysToPrint, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag);
        return dataDict, keyWithValues, getKeysToPrint, oldKeyValDict, newKeyValDict, commandCount, commit_flag
    else:
        printColored("Command not recognized.", constants.CRED)
        printColored("END command cannot be utilized in a transaction. To comeplete a transaction, please use ROLLBACK or COMMIT.", constants.CRED)
        printColored("Please try operations like with SET, GET, UNSET, and NUMWITHVALUE within a transaction.", constants.CRED)

    return dataDict, keyWithValues, getKeysToPrint, oldKeyValDict, newKeyValDict, commandCount, commit_flag

#The recusrive call with arguments to beginMethodAdv
def beginStartBlock(dataDict1, keyWithValues1, getKeysToPrint1, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag):
    while commit_flag is False:
        switch1 = True
        while switch1 is True:
            transCommands1 = str(input(""))
            dataDict1, keyWithValues1, getKeysToPrint1, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag = \
                beginBlockAdv(transCommands1, dataDict1, keyWithValues1, getKeysToPrint1, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag)
            if transCommands1 == constants.COMMIT or transCommands1 == constants.commit:
                printColored("All open transactions committed. Please start a new transaction with BEGIN.", constants.CYELLOW)
                commit_flag = True
                switch1 = False

            if transCommands1 == constants.ROLLBACK or transCommands1 == constants.ROLLBACK:
                switch1 = False
    return dataDict1, keyWithValues1, getKeysToPrint1, oldKeyValDict1, newKeyValDict1, commandCount1, commit_flag

#Method for text coloring
def printColored (data, color):
    print(color + data + constants.CEND)