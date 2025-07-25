
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
    
