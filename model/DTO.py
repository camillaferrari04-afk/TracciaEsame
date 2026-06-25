import datetime
from dataclasses import dataclass

@dataclass
class DTO:
    id:str
    height:int
    date_of_birth:datetime

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id