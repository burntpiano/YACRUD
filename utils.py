'''
This is where the various utility function reside.
I needed the user to have a full log of all file I/O modifications that are stored in *.log file format.
This is done in the case of catastrophic events, and the user loses their database.
They can then rebuild the database from the "Full Log.log file" if needed.
System agnosticism was kept in mind, as WatchedFileHandler is used for systems that use Posix, but not Windows.
This was not tested with Windows as I do not know anyone with a Windows machine.
'''

import logging, logging.handlers, os, tui

from logging.handlers import WatchedFileHandler
from logging import FileHandler

dateFormat = logging.Formatter("[%(levelname)s] "
                            "[%(asctime)s] "
                            "%(message)s", 
                            datefmt="%Y-%m-%d %H:%M:%S"
                            )

ttyFormat = logging.Formatter('[%(levelname)s] '
                            '%(message)s'
                            )

'''
The program is system agnostic and runs checks on if the machine is running Windows or a Unix-like operating system.
POSIX systems handle paths differently than WinAPI, and as such, both have been taken into consideration.
This ensures system agnosticism and portability among commonly used systems.
'''

if os.name == 'posix':
    logFile = WatchedFileHandler("Full Log.log")
else:
    logFile = FileHandler("Full Log.log")

#Logging is established here
log = logging.getLogger("YACRUD")
log.setLevel(logging.DEBUG)
log.addHandler(logFile)
logFile.setFormatter(dateFormat)

#Force fallback if the program is ran in an incompatible environment
if not tui.FORCE_PLAIN:
    from rich.logging import RichHandler
    richConsole = RichHandler(
                    level=logging.WARNING,
                    show_level=True,
                    show_time=False,
                    rich_tracebacks=True,
                    show_path=False,
                    markup=True
                    )
    log.addHandler(richConsole)
else:
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(ttyFormat)
    log.addHandler(consoleHandler)

#Errors are printed in color for feedback


#Same logic of duplicate check from previous revisions refactored for the Entry class
def duplicateCheck(name, entry, primaryDict):

    duplicateCounter = 2
    key = name

    while key in primaryDict:
        key = (f"{name} - {duplicateCounter}")
        duplicateCounter += 1
        log.debug(f"Duplicate {name} resolved.")
    primaryDict[key] = entry

#Refactored for Entry class
def printLog(primaryDict):
    entries = []
    for key, value in primaryDict.items():
        line = (f"[bold bright_yellow]{key} // {value.display()}[/bold bright_yellow]")
        entries.append(line)
    allEntries = "\n".join(entries)
    tui.panelMake(f"Here are your entries so far: \n{allEntries}", title="Printed Entries")
    return