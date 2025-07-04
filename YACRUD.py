'''
INF360 - Programming in Python

Final Project

I, Rory Blair , affirm that the work submitted for this assignment is entirely my own. I have not engaged in any form of academic dishonesty, including but not limited to cheating, plagiarism, or the use of unauthorized materials. This includes, but is not limited to, the use of resources such as Chegg, MyCourseHero, StackOverflow, ChatGPT, or other AI assistants, except where explicitly permitted by the instructor. I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence to academic standards. I understand that failing to comply with this integrity statement may result in consequences, including disciplinary actions as determined by my course instructor and outlined in institutional policies. By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.
'''

'''
This is Yet Another CRUD or YACRUD. A very barebones CRUD program for broad use cases.
It's generic scheme allows for future modification to something more specific.
This solves my own personal problem of wanting a lightweight CRUD to use for inventory management in my household.
These inventory changes are then pushed to my Raspberry Pi Zero 2 W based Magic Mirror
Currently it only stores in memory but the entries can be copied to the clipboard and pasted elsewhere for long term storage.
'''

import sys, shutil, os, json, pprint

###Global###
from pathlib import Path
# parentDir = Path.cwd()
# subDir = os.mkdir(parentDir)
# saveDir = Path(f"{parentDir}/'Saved Logs'")
from datetime import date
d = date.today()
USYearMonth = d.strftime("%Y-%m")
currentDay = d.strftime("%A %d")
saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)

# logList = list(saveDir.glob('*.json'))
# logFile = Path(saveDir / r"*.json")
# try:
#     with open(f"{logFile}.json", 'r') as file:
#         primaryDict = json.load(file)
# except FileNotFoundError:
primaryDict = {}

'''
This is the selection screen where the user can choose from the 3 currently available features.
I took care to ensure that the input from the user is case-insensitive
'''

def selectionScreen():

    print("Welcome to your personal logging program! \
        \nYou are welcome to log whatever you desire!")

    while True:

        choice = input("[A]dd new entry  \
                        \n[D]elete entry \
                        \n[P]rint entries \
                        \n[S]ave log \
                        \n[L]oad Log \
                        \n[Q]uit \
                        \nEnter your choice here:\
                        \n"
                       ).lower()

        if choice == 'a':
            createData()
        elif choice == 'd':
            deleteData(primaryDict)
        elif choice == 'p':
            printLog(primaryDict)
        elif choice == 's':
            saveLog()
        elif choice == 'l':
            loadLog(primaryDict)
        elif choice == 'q':
            sys.exit("Goodbye! See you next time!")
        else:
            print("Please select a valid response.")

'''
This is where the user creates the dictionary.
They are offered 2 mandatory and 1 optional value to input into a dictionary.
These user dictionaries are then nested into a parent dictionary.
This is done to ensure that duplicate entries are not overwritten.
Each nested dictionary's key is based off of the overall entry, and the amount and optional units are values.
'''

def createData():

        logDict = {}

        while True:

            logDict["Entry"] = input("Please enter what you would like to log. \
                                    \nThis needs to be a word or phrase. \
                                    \nEnter an item to log here: \
                                    \n"
                                    ).title()

            logEntry = logDict["Entry"]

            if logEntry.isalpha():
                logDict["Entry"] = logEntry
                break
            else:
                print(f"{logEntry} is invalid. \
                    \nPlease enter a valid word. \
                    \n")
            continue

        while True:

            logAmount = input("\nPlease enter the amount for the item you are logging. \
                                \nThis needs to be a valid numerical digit \
                                \nEnter the amount for the item: \
                                \n"
                            )
            ###I took into consideration keeping the amounts as integers for potential functions that can tabulate###
            ###Exceptions from incorrect entries are handled and users are then guided back to reentry of the amount value###
            try:
                logDict["Amount Logged"] = int(logAmount)
                break
            except ValueError as badInput:
                    print(f"{badInput} is not a valid number. \
                        \nPlease enter a valid number: ")

        while True:

            logDict["Measurement Unit"] = input("Enter the unit of measurement if applicable. \
                                            \nExample: oz, miles, inches, etc. \
                                            \nThis input must be a word. \
                                            \nIf not applicable, press enter/return to skip \
                                            \nEnter your unit of measurement here: \
                                            \n"
                                                )

            logUnit = logDict["Measurement Unit"]

            if logUnit == '':
                break
            ###"Psuedo exception handling" for incorrect input###
            ###I couldn't think of a scenario where a unit of measurement was only a digit###
            if logUnit.isalpha():
                logDict["Measurement Unit"] = logUnit
                break
            else:
                print(f"{logUnit} is invalid. \
                    \nPlease enter a valid word or phrase. \
                    \nAlternatively, press enter to skip entering a unit of measurement. \
                    \n")
                continue


        ###The user is then given feedback about their entry###
        ###It unfortunately won't always be grammatically sound, but I think it still gets the message across###
        if logUnit == '':
            print(f"{logDict['Amount Logged']} {logDict['Entry']} have been added to the log!")
        else:
            print(f"{logDict['Entry']}: {logDict['Amount Logged']} {logDict['Measurement Unit']} have been added to the log!")



        duplicateCheck(primaryDict, logDict)

        return logDict, primaryDict

'''
This is where the duplicate entries are handled via a counter starting at 2.
The unique key is checked in primaryDict. If it already exists, it's given a digit from the counter.
If it doesn't exist, it's just entered as normal.
I decided on this specific data structure for future features, primarily tabulation and consolidation of duplicate entries.
'''

def duplicateCheck(primaryDict, logDict):

    uniqueEntry = logDict['Entry']

    if uniqueEntry in primaryDict:
        duplicateCounter = 2

        while f"{uniqueEntry} - {duplicateCounter}" in primaryDict:
                duplicateCounter += 1
        duplicateKey = f"{uniqueEntry} - {duplicateCounter}"
        primaryDict[duplicateKey] = {
            'Amount Logged': logDict['Amount Logged'],
            'Measurement Unit': logDict['Measurement Unit']
        }
    
    else:
        primaryDict[uniqueEntry] = {
        'Amount Logged': logDict['Amount Logged'],
        'Measurement Unit': logDict['Measurement Unit']
    }
    
    return primaryDict, logDict


def printLog(primaryDict):
###This was perhaps overly complicated for what it accomplishes, but I did not aesthetically like the way a "normal" print or pretty print looked###
    print("Here are your entries so far:")
    for key, value in primaryDict.items():
        sep = " // "
        print(f"{key}{sep}{value}")
        global printedLog
        printedLog = f"{key}{sep}{value}"
    return

'''
This is where users can delete their entries if they'd like.
Printing the log is imperative as I'm keeping good HCI practices in mind and I do not know if the user remembers every entry or not.
Users can also back out of data deletion before it's completed.
'''

def deleteData(primaryDict):

    printLog(primaryDict)
    print(printedLog)

    while True:

        choice = input("What entry would you like to delete? \
                    \nEnter the entry to delete or enter [b]ack to return to selection screen: \
                    \n"
                       ).title()

        if choice == 'B':
            selectionScreen()
        elif choice in primaryDict.keys():

            while True:

                delConfirm = input(f"Are you sure you want to delete {choice} \
                                \n[Y]es \
                                \n[N]o \
                                \n"
                                ).lower()
                
                if delConfirm == 'y':
                    del primaryDict[choice]
                    print(f"{choice} deleted")
                    break
                elif delConfirm == 'n':
                    print(f"You did not delete {choice}")
                    break
        
        else:
            print("Invalid choice.")
            continue

def saveLog():
###check this one. new function###

    printLog(primaryDict)

    from pathlib import Path
    saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)
    saveDir.mkdir(parents=True, exist_ok=True)

    saveInput = input("Save your log so far?: \
                      \n[Y]es \
                      \n[N]o \
                      \n").lower()


    try:
        if saveInput == 'y':
            userLogName = input ("Use current day as the log name? \
                                \n[Y]es \
                                \n[N]o \
                                \n").lower()
            if userLogName == 'y':
                fileName = currentDay
                logFile = Path(saveDir / f"{fileName}.json")
                with logFile.open('w') as ldf:
                    json.dump(primaryDict, ldf, indent=4)
                    pprint.pprint("Log saved as " f"{fileName} in {saveDir}"".")
                if isinstance(logFile, dict):
                    logFile.append(primaryDict)
            if userLogName == 'n':
                userLogInput = input("Type what you would like to save this log as: \
                            \n")
                fileName = userLogInput
                logFile = Path(saveDir / f"{fileName}.json")
                with logFile.open('w') as lnf:
                        json.dump(primaryDict, lnf, indent=4)
                        print(f"Log saved as {userLogInput} in {saveDir}.")
                #     userLogFile = Path(saveDir / f"{userLogInput}.log")
                #     if not os.path.exists(userLogFile):
                #         userLogFile.write_text(printedLog)
                #         print(f"Log saved as {userLogInput} in {saveDir}.")
                #     if os.path.exists(userLogFile):
                #         with userLogFile.open('a', encoding="utf-8") as ufl:
                #             ufl.write(f"\n{printedLog}")
                #             print(f"Log ammended and saved as {userLogInput} in {saveDir}")
                #             ufl.close()
                #             break
            if saveInput == 'n':
                print("Returning you to the selection screen.")
                return
    except FileNotFoundError:
        print("Lemme figure this one out real quick.")

        fileName = userLogInput, currentDay
        logFile = Path(saveDir / f"{fileName}.json")
            
    return saveDir, logFile

def loadLog(primaryDict):

    saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)
    logList = list(saveDir.glob('*.json'))
    logFile = r"*.json"

    print("Available logs to load.")
    for index, logFile in enumerate(logList, 1):
        print(f"[{index}] {logFile}")
        loadFile = f"{index[logFile]}"

    while True:
        try:
            loadInput = input("Enter the attached number of the list you would like to load: \
                            \n")
            if loadInput == index in loadFile:
                with open(logFile, 'r') as lf:
                    primaryDict = json.load(lf)
            print(f"SANITY CHECK: {primaryDict}, {logFile}")
        except FileNotFoundError:
            print("Log not found. Please try again.")
    
        return primaryDict

# def loadLog():
        
#     saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)
#     logList = list(saveDir.glob('*.json'))

#     print("Available logs to load.")
#     for index, logFile in enumerate(logList, 1):
#         print(f"[{index}] {logFile}")

#     while True:
#         try:
#             if logFile.exists():
#                 loadInput = int(input("Enter the attached number of the list you would like to load: \
#                                 \n"))
#                 with open(loadInput, 'r') as lf:
#                     logFile.read()
#         except FileNotFoundError:
#             print("Log not found. Please try again.")

#     while True:
#         if logFile in saveDir:
#             break
#         else:
#             print("You do not have any entries to load.")
#             return
    
#     loadInput = input("Select a log to load or go [b]ack to the selection screen: \
#                       \n")
    
#     saveDir.glob('*.log')
#     logContents = list(saveDir.glob('*.log'))
#     print(logContents)
#     print(logFile)
# def loadLog(saveDir, logFile):
# ###check this one###
 
#     loadInput = input("Select a log to load or go [b]ack to selection screen: \
#                       \n").lower()
    
#     from pathlib import Path

#     saveDir = Path(f"./Saved Logs/{logFile}")
#     saveDir.glob('*.log')
#     list(saveDir.glob('*.log'))
#     logContents = logFile.read()

#     while True:
#         if loadInput == logFile:
#             if logFile in saveDir:
#                 confirm = input("Is this the correct log?: \
#                                 \n[Y]es \
#                                 \n[N]o \
#                                 \n[B]ack \
#                                 \n").lower()
#                 ###maybe only print 5 at a time for long lists?###
#                 # for i in logContents:
#                 #     i = range(len(logContents)0, 5)
#                 print(logContents)
#                 if confirm == 'y':
#                     open(logFile, 'a')
#                     return logFile
#                 if confirm == 'n':
#                     break
#                 if confirm == 'b':
#                     return
#                 else:
#                     print("Invalid choice")
#                     continue
#             if logFile not in saveDir:
#                 print(f"{loadInput} not found.")
#                 break
#         if loadInput == 'b':
#             return
#         else:
#             print("Invalid choice")
'''
Finally, it all executes from a single function.
I went through several different revisions of differing complexity before deciding on this.
Deciding on how I wanted to structure my database was difficult as it is leveraged everywhere else and integral for functionality.
'''

selectionScreen()
