'''
INF360 - Programming in Python

Final Project

I, Rory Blair , affirm that the work submitted for this assignment is entirely my own. I have not engaged in any form of academic dishonesty, including but not limited to cheating, plagiarism, or the use of unauthorized materials. This includes, but is not limited to, the use of resources such as Chegg, MyCourseHero, StackOverflow, ChatGPT, or other AI assistants, except where explicitly permitted by the instructor. I have neither provided nor received unauthorized assistance and have accurately cited all sources in adherence to academic standards. I understand that failing to comply with this integrity statement may result in consequences, including disciplinary actions as determined by my course instructor and outlined in institutional policies. By signing this statement, I acknowledge my commitment to upholding the principles of academic integrity.
'''

'''
This is yet another CRUD. Very barebones and for broad usage.
It's generic scheme allows for future modification to something more specific.
This solves my own personal problem of wanting a lightweight CRUD to use for inventory management in my household.
These inventory changes are then pushed to my Raspberry Pi Zero 2 W based Magic Mirror
I have added a save and load feature that allows the user to load and save data into .JSON file type.
I chose .JSON because it works well with my MagicMirror and allows true data manipulation.
I have also added a terminal user interface for a more polish.
'''

'''
The only external package that is not included is the rich module.
It will be need to be installed via pip.
I have included a requirements text file as I am trying to maintain system agnosticism.
This is a challenge I faced as I use Linux distribution and must use a Python virtual environment for packages not provided by my distro repository.
Python version should also be 3.11 as well.
I only mention this as my Linux repo defaults to the most recent, version 3.15.
'''

'''
System environment when writing code and debugged:
Operating system: Arch Linux
Terminal emulator: Kitty
Terminal support: ANSI character escape code, 256 color
Debugging environment: Kitty terminal
'''

import sys, os, json, utils, ioutils, tui

###Global###
from pathlib import Path
from datetime import date
from classes import Entry

d = date.today()
USYearMonth = d.strftime("%Y-%m")
currentDay = d.strftime("%A %d")
saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)

primaryDict = {}

'''
This is the selection screen where the user can choose from the 5 currently available features.
I took care to ensure that the input from the user is case-insensitive.
Throughout the project, you will notice that many prints and inputs are replaced by helper functions.
This was done to ensure that the program would not crash if the user's terminal would support ANSI color escape sequences.
'''

def selection_Screen():

    while True:
        tui.panelMake("Welcome to your personal logging program! \
                    \nYou are welcome to log whatever you desire! \
                    \n \
                    \n[A]dd new entry \
                    \n[D]elete entry \
                    \n[P]rint entries \
                    \n[S]ave entries \
                    \n[L]oad entries \
                    \n[Q]uit",
                    title="Main Menu")

        choice = tui.safeInput("Enter your choice here:").lower()

        if choice == 'a':
            createData(primaryDict)
        elif choice == 'd':
            deleteData(primaryDict)
        elif choice == 'p':
            utils.printLog(primaryDict)
        elif choice == 's':
            ioutils.saveLog(primaryDict, saveDir, USYearMonth, currentDay)
        elif choice == 'l':
            ioutils.loadLog(primaryDict, saveDir)
        elif choice == 'q':
            sys.exit("Goodbye! See you next time!")
        else:
            tui.safePrint("Please select a valid response.", style="err")

'''
This is where the user creates the dictionary.
They are offered 2 mandatory and 1 optional value to input into a dictionary.
These user dictionaries are then nested into a parent dictionary.
The duplicate validation handler was moved to the utils.py module to reduce clutter.
I abandoned the nested dictionary data structure as I realized it was not beneficial.
'''

def createData(primaryDict):

    #This now accepts multiple words, and as a precaution, trailing whitespace is removed for database clarity and polish.
    while True:
        tui.panelMake("Please enter what you would like to log. \
                    \nThis needs to be a word or phrase.",
                    title="Create Data // Enter an Item")
        name = tui.safeInput("Enter an item to log here:").strip()
        if all(word.isalpha() for word in name.split()):
            break
        else:
            utils.log.warning(f"Invalid item entered in createData function: {name}")
            tui.safePrint(f"{name} is not a valid word", style="err")
            continue

    while True:
        tui.panelMake("\nPlease enter the amount for the item you are logging. \
                                \nThis needs to be a valid numerical digit",
                                title="Create Data // Enter an Amount")
        amount = tui.safeInput("Enter the amount for the item:").strip()
        try:
            amount = int(amount)
            break
        except ValueError:
            utils.log.critical(f"Invalid input in createData function: {amount}")
            tui.safePrint(f"{amount} is not a valid number.", style="err")
    
    while True:
        tui.panelMake("Enter the unit of measurement if applicable. \
                                            \nExample: oz, miles, inches, etc. \
                                            \nThis input must be a word. \
                                            \nIf not applicable, press enter/return to skip \
                                            \n",
                                            title="Create Data // Enter the Unit of Measurement")
        unit = tui.safeInput("Enter your unit of measurement here:").strip()

        if unit == '' or unit.isalpha():
            break
        else:
            utils.log.warning(f"Invalid input in createData function: {unit}")
            tui.safePrint(f"{unit} is not a valid unit of measurement.", style="err")
            continue

    entry = Entry(name, amount, unit)

    #Same logic applies to the duplicateCheck function and has been refactored for the Entry class. The function is now in the utils.py module.
    utils.duplicateCheck(name, entry, primaryDict)
    utils.log.info(f" - Log entry: {entry.name}: {entry.amount} {entry.unit} stored in database")

    return entry, name, primaryDict

'''
This is where users can delete their entries if they'd like.
Printing the log is imperative as I'm keeping good HCI practices in mind and I do not know if the user remembers every entry or not.
Users can also back out of data deletion before it's completed.
'''

def deleteData(primaryDict):

    utils.printLog(primaryDict)

    while True:
        tui.panelMake("What entry would you like to delete?", title="Entry Deletion")
        choice = tui.safeInput("Enter the entry to delete or enter \[b]ack to return to selection screen:")

        if choice == 'b':
            return
        elif choice in primaryDict.keys():
            while True:
                tui.panelMake(f"Are you sure you want to delete {choice} \
                                \n[Y]es \
                                \n[N]o \
                                \n", title="Deletion Confirmation")

                delConfirm = input()

                if delConfirm == 'y':
                    del primaryDict[choice]
                    tui.safePrint(f"{choice} deleted", style="warn")
                    utils.log.info(f"{choice} deleted from the database")
                    break
                elif delConfirm == 'n':
                    tui.safePrint(f"You did not delete {choice}", style="goodFeedback")
                    break
        else:
            utils.log.warning(f"Invalid input in the deleteData function: {choice}")
            continue


selection_Screen()
