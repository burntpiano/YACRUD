
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

parentDict = {}
childDict = {}
entryCounter = 1

def selectionScreen():
     
    print("Welcome to your personal logging program!\
        \nYou are welcome to log whatever you desire!")
    
###have choiceLabel print back user choice for both user confirmation and error handling###
 #   choiceLabel = 
 ###refactor lengthy try statement. maybe 1,2,3,4,5?###
 ###could use or operators then###
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
                createDict(parentDict)
            elif choice == 's':
                if parentDict:
                    searchLog(parentDict)
            elif choice == 'c':
                if parentDict:
                    countLog(parentDict)
            elif choice == 'p':
                if parentDict:
                    printLog(parentDict)
            elif choice == 'e':
                if parentDict:
                    exportLog(parentDict)
            elif choice == 'q':
                sys.exit("Goodbye! See you next time!")
            elif choice == '':
                print("Please select a valid response.")
                choice
            elif choice == 'd':
                debug()
        except AttributeError:
            print(f"Your choice does not exist yet! Come back later!")


'''
This function will take user input to create a child dictionary which is then nested in a parent dictionary. 
Each entry is then assigned a key, and value while maintaining a generic labeling scheme.
The Amount Logged will handle an exception if the user inputs a string as it's for later tabulation.
The Measurement Unit has a "pseudo execption handling" if the user inputs an integer.
Each added entry will be printed to the user afterwards for good HCI
'''

###add quit in this function###

def createDict(parentDict):

        childDict = {}
  
        global entryCounter

        childDict["Entry"] = input("Please enter what you would like to log in a list. \
                        \nWhen you are finished, press enter/return twice to continue to the next portion. \
                        \nEnter Entry to log here: \
                        \n"
                                ).lower().title()

        while True:

            logAmount = input("\nEnter the amount for the item you are logging. \
                    \nThis needs to be a valid numerical digit \
                    \nEnter the amount for the entry:"
                    "\n"
                            )
            
            try: 
                childDict["Amount Logged"] = int(logAmount)
                break
            except ValueError as badInput:
                    print(f"{badInput} is not a valid number. \
                        \nPlease enter a valid number: ")

        while True:
            
            childDict["Measurement Unit"] = input("Enter the unit measurement if applicable. \
        \nExample: oz, miles, inches, etc. \
        \nThis entry must be a word. \
        \nIf not applicable, press enter/return to skip \
        \nEnter your measurement here: \
        \n"
            )

            logUnit = childDict["Measurement Unit"]

            if logUnit == '':
                break
            
            if logUnit.isalpha():
                childDict["Measurement Unit"] = logUnit
                break
            else:
                print(f"{logUnit} is invalid. \
                    \nPlease enter a valid unit measurement \
                    \n")
                continue

        if logUnit == '':
            print(f"{childDict['Amount Logged']} {childDict['Entry']} have been added to the log!")
        else:
            print(f"{childDict['Entry']}: {childDict['Amount Logged']} {childDict['Measurement Unit']} have been added to the log!")

        parentDict[entryCounter] = childDict
        entryCounter += 1

        return parentDict

def searchLog(parentDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return

def countLog(parentDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return

def mergeParent(parentDict):

    mergedDict = {}
    for innerDicts in parentDict:
        innerData = list(innerDicts.values())[0]
        fullLog = innerData["Full Log"]
        mergedDict[fullLog] = innerData
    return mergedDict



##actually do this one##
def printLog(parentDict):
    ###placeholder###
    print("broken")
    return

#     print("Welcome to the printing function! \
#           \nFrom here you can display on the terminal what you have logged thus far")
#     printChoice = input("Make your selection:  \
#                     \nPrint [E]ntries \
#                     \nMore to come!").lower
    
#     if printChoice == 'e':
#         pprint.pprint(parentDict["Entry"])

#     printEntry

def exportLog(parentDict):
    print("Feature not implemented! \
        \nCheck back later! \
        \nReturning you to the selection screen \
        \n")
    return

def debug():
###debug section###

###createDict sanity check###
    pprint.pprint(parentDict)

##mergeParent sanity check###
    mergedDict = {}
    pprint.pprint(mergedDict)

selectionScreen()