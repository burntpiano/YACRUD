
'''
This program is a generic logger. 
The user will enter whatever they would like to log followed by the quantity and (if applicable).
This program solves the problem of having to log things to later export to spreadsheets or even a simple text document, while simultaneously being incredibly lightweight.
This includes, but is certainly not limited to: inventory, logging hours spent doing something, water drank, or logging work miles.
The user will then be able to search through their log entries, print the log in it's entirety or by entry then copy it to their clipboard for exporting, or tabulate the total entries by the amount.
This program solves my own personal problem of trying to keep inventory of pre-prepped food items or ingredients in my freezer to then later display on my Raspberry Pi Zero 2 W based Magic Mirror while maintaining a lightweight profile.
'''
import sys, pprint

'''
This function greets the user and begins the entire program
It allows the program to branch to other functions
'''

logDict = {}

def selectionScreen():
     
    print("Welcome to your personal logging program!\
        \nYou are welcome to log whatever you desire!")
    
###have choiceLabel print back user choice for both user confirmation and error handling
 #   choiceLabel = 
    while True:

        choice = input("[A]dd new entry  \
                    \n[S]earch log entries \
                    \n[C]ount log entries \
                    \n[P]rint log to terminal \
                    \n[E]xport log \
                    \n[Q]uit \
                    \nEnter your choice here:\
                    \n").lower()

        try: 
            if choice == 'a':
                createDict(logDict)
            elif choice == 's':
                if logDict.isinstance():
                    searchLog(logDict)
            elif choice == 'c':
                if logDict.isinstance():
                    countLog(logDict)
            elif choice == 'p':
                if logDict.isinstance():
                    printLog(logDict)
            elif choice == 'e':
                if logDict.isinstance():
                    exportLog(logDict)
            elif choice == 'q':
                sys.exit("Goodbye! See you next time!")
            elif choice == '':
                print("Please select a valid response.")
                choice
            elif choice == 'd':
                return
        except AttributeError:
            print(f"Your choice does not exist yet! Come back later!")

'''
This function will take user input to create a dictionary. 
Each entry is then assigned a key, and value while maintaining a generic labeling scheme.
The Amount Logged will handle an exception if the user inputs a string as it's for later tabulation.
The Measurement Unit has a "pseudo execption handling" if the user inputs an integer.
Each added entry will be printed to the user afterwards for good HCI
'''

###fix quit in this function###

def createDict(logDict):

        logEntry = {}
        logEntry["Entry"] = input("Please enter what you would like to log in a list. \
                        \nWhen you are finished, press enter/return twice to continue to the next portion. \
                        \nYou can always quit by entering Q \
                        \nEnter Entry to log here: \
                        \n"
                                ).lower().title()
        
        if logEntry == ('Q'):
            sys.exit("Goodbye! See you next time!")

        while True:

            logAmount = input("\nEnter the amount of the Entry(s) you are logging. \
                    \nThis needs to be a valid numerical digit \
                    \nEnter the amount of the Entry(s):"
                    "\n"
                            )
            
            try: 
                logEntry["Amount Logged"] = int(logAmount)
                break
            except ValueError as badInput:
                    print(f"{badInput} is not a valid number. \
                        \nPlease enter a valid number: ")

        while True:
            
            logEntry["Measurement Unit"] = input("Enter the unit measurement if applicable. \
        \nExample: oz, miles, inches, etc. \
        \nThis entry must be a word. \
        \nIf not applicable, press enter/return to skip \
        \nEnter your measurement here: \
        \n"
            )

            logUnit = logEntry["Measurement Unit"]

            if logUnit == '':
                break
            
            if logUnit.isalpha():
                logEntry["Measurement Unit"] = logUnit
                break
            else:
                print(f"{logUnit} is invalid. \
                    \nPlease enter a valid unit measurement \
                    \n")
                continue


        logDict.update(logEntry)

        if logUnit == '':
            print(f"{logEntry['Amount Logged']} {logEntry['Entry']} have been added to the log!")
        else:
            print(f"{logEntry['Entry']}: {logEntry['Amount Logged']} {logEntry['Measurement Unit']} have been added to the log!")



        return logDict


##sanity check for createDict function##
#logDict = {}
#createDict(logDict)
# pprint.pprint(logDict)

def searchLog(logDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return

def countLog(logDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return

##actually do this one##
def printLog(logDict):
    
    logList = []
    if not logDict:
        return logList
    for keys, values in logDict.items():
        keys = keys.get
        dictAmounts = list(logDict.items())
        logList = list(dictEntries,dictAmounts)

    return logList

logList = []
debugPrintLog = printLog(logDict)
print(logList)

def exportLog(logDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return



selectionScreen()
###debug section###
##printLog sanity check##
logList = []
debugPrintLog = printLog(logDict)
print(logList)