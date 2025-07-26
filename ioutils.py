'''
This is the module that the I/O helper functions reside.
I wanted to ensure that the user was given options as to how they wanted their database files saved.
This is done either by a default timestamp, or by user input.
Everything was also refactored with the Entry class in mind.
'''

import utils, json, os, tui,re

from pathlib import Path
from datetime import date
from classes import Entry

d = date.today()
USYearMonth = d.strftime("%Y-%m")
currentDay = d.strftime("%A %d")
saveDir = (Path.cwd() / 'Saved Logs' / USYearMonth)

'''
Users can save their entries to a .JSON file type that can be read in browser or a text editor.
They are given the option of the default which is a simple timestamp, or they can name their files as they wish.
The files are saved into a path or folder that is labeled with the current year and month for organization.
Initially, these did not use the Entry class, but were later refactored.
'''

def saveLog(primaryDict, saveDir, currentDay, USYearMonth):

    utils.printLog(primaryDict)

    saveDir.mkdir(parents=True, exist_ok=True)

    tui.panelMake("Save your log so far?: \
                    \n[Y]es \
                    \n[N]o \
                    \n", title="Save Log")
    
    saveInput = input()

    if saveInput == 'y':
        tui.panelMake("Use the current day as the log name? \
                            \n[Y]es \
                            \n[N]o \
                            \n", title="Choose Name")
        
        chooseName = input()
        
        if chooseName == 'y':
            fileName = currentDay
        elif chooseName == 'n':
            tui.panelMake("What would you like to name your file? \
                                \n", title="Choose Name") 
            fileName = tui.safeInput("Enter your name here:").strip()
            if not fileName:
                tui.safePrint("File name cannot be empty, returning you to the main screen.", style="err")
                return
        #WinAPI uses specific naming conventions that differ from systems that use POSIX. This prevents crashes/corrupted files from user input.
        fileName = re.sub(r'[\\/*?:"<>|]', '_', fileName)
        filePath = Path(saveDir / f"{fileName}.json")
        try:
            saveDict = {k: v.save() for k, v in primaryDict.items()}
#The file is opened, info from the primary dictionary is written, and user is given feedback. If any operating system issue arises, then it is handled
            with filePath.open('w') as lf:
                json.dump(saveDict, lf, indent=4)
            utils.log.debug(f"User saved file {fileName}.json")
            tui.safePrint(f"Log saved as {fileName}.json in {saveDir}.", style="goodFeedback")
        except (OSError, TypeError) as err:
            utils.log.critical(f"Failed to save log {fileName}. Reason: {err}")
    elif saveInput == 'n':
        return
    else:
        tui.safePrint("Invalid choice. Returning you to main menu", style="err")
        return
    
    return saveDir, fileName, filePath


'''
Users can load their previously saved files to print in terminal or make amendments to.
They are presented with the files they have already saved to reduce any confusion.
The printed files are sorted by modified date.
'''
def loadLog(primaryDict, saveDir):
    
    filePath = list(saveDir.glob("*.json"))
    sortedFiles = sorted(filePath, key=os.path.getmtime)

    if not filePath:
        tui.safePrint("No logs found", style="prompt")
        return

    while True:
        for index, file, in enumerate(sortedFiles, 1):
            tui.safePrint(f"[{index}] {file.name}", style="goodFeedback")

        try:
            tui.safePrint("Enter the corresponding number of the log you would like to load: ", style="prompt")
            loadInput = int(input())
            loadedFile = sortedFiles[loadInput - 1]
            with loadedFile.open('r') as lf:
                data = json.load(lf)
                #This single line is one of the most important lines in this block as it ensures that the user isn't unintentionally concatenating a previously loaded log onto their newly loaded log.
                primaryDict.clear()
                for k, v in data.items():
                    primaryDict[k] = Entry(k, v["Amount Logged"], v["Measurement Unit"])
            tui.safePrint(f"{loadedFile.name} loaded", style="goodFeedback")
            utils.log.debug(f"User loaded file {loadedFile}.json")
        except (ValueError, IndexError):
            utils.log.warning("Log not found. Please try again")
            continue

        return