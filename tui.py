'''
This is where the TUI functions reside.
This was one of the largest refactors in my program as I needed to meticulously replace any of the builtin module functions if needed.
I could not import all of the submodules simultaneously hence the large block of import statements.
'''

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.style import Style
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

import sys, os

#Provides fallback for environments that support 256 color and ANSI escape code.
FORCE_PLAIN = os.getenv("YACRUD_PLAIN", "0") == "1" or not sys.stdout.isatty()

#The rich package uses a simulated HTML markup syntax in order to print in color. This fit well with my project as I just finished my HTML/CSS class.
styleDict = {
    "err": "bold red",
    "warn": "bold orange3",
    "goodFeedback": "bold green",
    "badFeedback": "dim red",
    "panel": "dim cyan1",
    "prompt": "dim green"
    }

yacrudTheme = Theme(styleDict)

#Since the interface is a TUI, rich uses a console object to display strings as classes within the rich package.
console = Console(color_system="auto",
                  force_terminal=None,
                  theme=yacrudTheme
                  )

#Both the safePrint and safeInput are used to leverage the rich module's use of ANSI escape character code to render colored text.
def safePrint(text, style=None):
    if FORCE_PLAIN:
        print(text)
    else:
        console.print(text, style=style)

def safeInput(promptText="", style="prompt"):
    if FORCE_PLAIN:
        return input(promptText).lower()
    else:
        console.print(promptText, style=style)
    return console.input().lower()

#The panelMake function renders the screen that the users can read clean and colorful text from
def panelMake(panelText, style="panel", title=None):
    if FORCE_PLAIN:
        print(panelText)
    else:
        panelText = Text.from_markup(panelText,
                        justify="center",
                        )
        panel = (Panel(panelText,
                        style="panel",
                        title=title, 
                        title_align="center",
                        subtitle="YACRUD",
                        subtitle_align="right",
                        box=box.HEAVY,
                        expand=False,
                        border_style="bold purple4",
                        padding=(1, 8)
                        ))
        console.print(Align.center(panel))
