from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float

    def __gt__(self, other_computer: Computer):
        '''
        Magic method for comparing which computer 
        is greater given 2 computers:

        1. Compare both computers with hacking diffculty.
        2. If both of them have the same value, compare them 
        with risk factor.
        3. If both still have the same value, compare them 
        with lexicographical order (Assume all computer names
        in the list are unique). 

        self.name: String name of the computer itself.
        other.name: Srting name of other computer.

        Time Complexity:
        Best: O(1), when both computers have different hacking difficulty 
        or risk factor.
        Worst: O(min(self.name, other.name)), when both computers only 
        have different names.
        '''
        if self.hacking_difficulty == other_computer.hacking_difficulty:
            if self.risk_factor == other_computer.risk_factor:
                return self.name > other_computer.name 
            return self.risk_factor > other_computer.risk_factor
        return self.hacking_difficulty > other_computer.hacking_difficulty
    
    def __lt__(self, other_computer: Computer):
        '''
        Magic method for comparing which computer 
        is lesser given 2 computers:

        1. Compare both computers with hacking diffculty.
        2. If both of them have the same value, compare them 
        with risk factor.
        3. If both still have the same value, compare them 
        with lexicographical order (Assume all computer names
        in the list are unique). 

        self.name: String name of the computer itself.
        other.name: Srting name of other computer.

        Time Complexity:
        Best: O(1), when both computers have different hacking difficulty 
        or risk factor.
        Worst: O(min(self.name, other.name)), when both computers only 
        have different names.
        '''
        if self.hacking_difficulty == other_computer.hacking_difficulty:
            if self.risk_factor == other_computer.risk_factor:
                return self.name < other_computer.name 
            return self.risk_factor < other_computer.risk_factor
        return self.hacking_difficulty < other_computer.hacking_difficulty
    
    def __eq__(self, other_computer):
        '''
        Checks whether it founds the computer

        Time Complexity (Best and Worst): O(1)
        '''
        return self is other_computer
    

