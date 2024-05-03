from __future__ import annotations
from computer import Computer
from double_key_table import DoubleKeyTable
from algorithms.mergesort import mergesort

class ComputerManager:
    '''
    Acts as a store which tracks all computers 
    in a route and can be used to edit, add or remove
    computers.
    '''

    def __init__(self) -> None:
        '''
        A constructor which creates a ComputerManager 
        object (Initialisation).

        Time complexity (Best and Worst): O(1)
        '''
        self.manager_hash_table = DoubleKeyTable()
        self.group_by_difficulty_lst = []

    def add_computer(self, computer: Computer) -> None:
        '''
        Adds a computer to the manager.

        Time complexity (Best and Worst): O(1)
        '''
        self.manager_hash_table[str(computer.hacking_difficulty), str(computer.name)] = computer 

    def remove_computer(self, computer: Computer) -> None:
        '''
        Removes a computer from the manager

        Time complexity (Best and Worsr): O(1)
        '''
        del self.manager_hash_table[str(computer.hacking_difficulty), str(computer.name)]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        '''
        Removes the old computer and adds the new computer

        Time Complexity (Best and Worst): O(1)
        '''
        del self.manager_hash_table[str(old.hacking_difficulty), str(old.name)]
        self.manager_hash_table[str(new.hacking_difficulty), str(new.name)] = new

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        '''
        Returns a list of all computers with hacking difficulty 
        that is given by the input.

        Time Complexity (Best and Worst): O(1)
        '''
        try:
            computer_lst = self.manager_hash_table.values(str(diff))
        except KeyError: 
            return []
        else:
            return computer_lst

    def group_by_difficulty(self) -> list[list[Computer]]:
        '''
        Returns a list of lists of all computers, grouped by and
        sorted by asecnding hacking difficulty. 

        n: Total number of different hacking difficulties in the 
        hash table (DoubleKeyTable()) so far.

        Time Complexity (Best and Worst): O(nlog(n))
        '''
        self.group_by_difficulty_lst = []
        order = lambda diff : diff
        all_diff_lst = self.manager_hash_table.keys() # O(1)
        all_diff_lst = mergesort(all_diff_lst, order) # O(n log n)

        for hack_difficulty in all_diff_lst: # O(n)
            computers_with_same_diff = self.manager_hash_table.values(hack_difficulty) # O(1)
            self.group_by_difficulty_lst.append(computers_with_same_diff)
        return self.group_by_difficulty_lst

