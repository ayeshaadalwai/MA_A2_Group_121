from __future__ import annotations

from computer import Computer

from data_structures.hash_table import LinearProbeTable

from algorithms.mergesort import merge, mergesort
from algorithms.binary_search import binary_search

class ComputerOrganiser:
    '''
    Determines the threat of the virus by ranking
    each potential virus by its hacking difficulty.
    '''

    def __init__(self) -> None:
        '''
        Constructor which creates an object.
        (Initialisation)
        
        Time Complexity (Best and Worst): O(1)
        '''

        self.computer_list = [] # A list that stores all 
                                # Computer objects.

    def cur_position(self, computer: Computer) -> int:
        '''
        Finds the rank of the provided computer given
        all computers included so far.

        n: Total number of Computer objects that
        are included in the list so far.

        :raises KeyError: When the computer input hasn't
        been added yet.

        Time Complexity:
        Best: O(1), when the input Computer Object is found in the
        middle of the computer list.
        Worst: O(log n), whem the input Computer Object is not 
        found in the computer list.
        '''
        position = binary_search(self.computer_list, computer) # O(log n)
        if len(self.computer_list) == 0 or self.computer_list[position] != computer:
            raise KeyError(computer.name)
        return position

    def add_computers(self, computers: list[Computer]) -> None:
        '''
        Adds a list of computers to the organiser

        m: Number of Computer objects in the input list.
        n: Total number of Computer objects that
        are included in the list so far.

        Time complexity (Best and Worst): O(mlog(m) + n)
        '''
        
        self.computer_rank = 0
        computers = mergesort(computers, lambda computer: computer.name)
        computers = mergesort(computers, lambda computer: computer.risk_factor)
        computers = mergesort(computers, lambda computer: computer.hacking_difficulty)
        self.computer_list = merge(self.computer_list, computers, lambda computer: computer.hacking_difficulty)