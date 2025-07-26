'''
This is where the Entry class resides.
The decision to turn the user made database into a class allowed for more concise code, and easier readability.
Since class instances cannot be printed as strings, it needs to be "formatted" properly to be printed throughout the project.
The display function is used to print the newly "reformatted" string.
'''

class Entry:
    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

    def display(self):
        if self.unit:
            return (f"{self.name}: {self.amount} {self.unit}")
        return (f"{self.name}: {self.amount}")
    
    def __str__(self):
        return self.display()

    def save(self):
        return {"Amount Logged": self.amount, "Measurement Unit": self.unit}
    
