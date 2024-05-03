from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR
from data_structures.linked_stack import LinkedStack

from algorithms.mergesort import mergesort

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
        self.location_lst = []
        self.str = ""
        self.sorted_lst = []
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        
        len(key): Length (size) of the key.
        hash: Hash function for giving expected position of the hash table
        at each level.
        isinstance: Type checking operator which checks the type of 
        an object.
        comp: Comparision operator for strings ('==' specifically).

        Time Complexity:
            Best: O(hash) when the item not found in the first (1st) 
            hash table.
            Worst: O(len(key)*(hash + comp + isinstance)) when the item is found or not found
            in the last hash table as there are many keys that are similar to the input key.
        """
        return self.get_item_aux(self, key, 0)
    
    def get_item_aux(self, hash_table:InfiniteHashTable, key:K, level: int):
        '''
        Auxillary method for __getitem__()

        len(key): Length (size) of the key.
        hash: Hash function for giving expected position of the hash table
        at each level.
        isinstance: Type checking operator which checks the type of 
        an object.
        comp: Comparision operator for strings ('==' specifically).

        Time Complexity:
            Best: O(hash) when the item is not found in the first (1st) 
            hash table.
            Worst: O(len(key)*(hash + comp + isinstance)) when the item is found or not found
            in the last hash table as there are many keys that are similar to the input key.
        '''
        position = hash_table.hash(key)

        # Checks whether the key is not found
        if hash_table.array[position] is None: 
            raise KeyError(key)
        
        # Checks whether the key is found
        elif isinstance(hash_table.array[position], tuple) and hash_table.array[position][0] == key:
            self.location_lst.append(position) # Adds a position of a hash table leading to an item into the list.
            if isinstance(hash_table.array[position][1], InfiniteHashTable):
                return self.get_item_aux(hash_table.array[position][1], key, level + 1)
            else:
                return hash_table.array[position][1] 
        
        # Checks whether there is any hash tables left.
        elif isinstance(hash_table.array[position], tuple) and hash_table.array[position][0] == key[:level + 1]:
            if isinstance(hash_table.array[position][1], InfiniteHashTable):
                self.location_lst.append(position)
                return self.get_item_aux(hash_table.array[position][1], key, level + 1)
            else:
                raise KeyError(key)
            
        else: 
            raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        len(key): Length (number of character of a key).
        isistance: Type checking operator which checks the type of 
        an object.
        comp: Comparison operator for strings ('==' specifically)
        hash: Hash fuction which gives out the expected postion of the key
        at each level.

        Time Complexity:
            Best: O(hash + isinstance + comp), when the array position of the first hash table is found.
            Worst: O(len(key)*(hash + isinstance + comp)), when the input key are nearly 
            identical to any one of the keys in the hash table.
        """
        return self.set_item_aux(self, key, value, 0)

    def set_item_aux(self, hash_table:InfiniteHashTable, key:K, value:V, level: int):
        '''
        Auxillary method for __setitem__()

        len(key): Length (number of character of a key).
        isistance: Type checking operator which checks the type of 
        an object.
        comp: Comparison operator for strings ('==' specifically)
        hash: Hash fuction which gives out the expected postion of the key
        at each level.

        Time Complexity:s
            Best: O(hash + isinstance + comp), when the array position of the first hash table is found.
            Worst: O(len(key)*(hash + isinstance + comp)), when the input key are nearly 
            identical to any one of the keys in the hash table.
        '''
        position = hash_table.hash(key) # Position set for next hash table.
        if hash_table.array[position] is None:
            hash_table.count += 1
            hash_table.array[position] = (key, value) 

            # O(isinstance)
        elif isinstance(hash_table.array[position], tuple) and hash_table.array[position][0] == key:
            hash_table.array[position] = (key, value) 
        
            # O(isinstance)
        elif isinstance(hash_table.array[position], tuple) and not isinstance(hash_table.array[position][1], InfiniteHashTable):
            first_item = hash_table.array[position]
            hash_table.array[position] = (first_item[0][:level + 1], InfiniteHashTable(level + 1))
            hash_table.count += 1
            self.set_item_aux(hash_table.array[position][1], first_item[0], first_item[1], level + 1)
            self.set_item_aux(hash_table.array[position][1], key, value, level + 1)

            # O(isinstance)
        elif isinstance(hash_table.array[position], tuple) and isinstance(hash_table.array[position][1], InfiniteHashTable):
            hash_table.count += 1
            self.set_item_aux(hash_table.array[position][1], key, value, level + 1)

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        hash: Hash function for giving expected position of the hash table at each level.
        location_list: A list which indicates a path to the item (sequence of 
        positions required to access the key) (self.get_location()). 
        array_size: The array size of the last hash table where the 
        item is located.

        Time Complexity:
            Best: O(hash) when the key is not found in the hash table.
            Worst: O(location_list + array_size) when the item is found and the hash table where the 
            item is located has only 1 item left which is located at the end of the array after 
            the deletion.
        """
        location_list = self.get_location(key) # Best: O(hash)
        list_len = len(location_list)
        self.delete_item_aux(self, location_list, 0, list_len - 1, list_len)

    def delete_item_aux(self, hash_table, location_list, locate_index, path_distance, list_len):
        '''
        Auxiliary method for __delitem__()

        location_list: A list which indicates a path to the item (sequence of positions required
        to access the key) (self.get_location()). 
        array_size: The array size of the last hash table where the 
        item is located.

        Time Complexity:
            Best: O(location_list) when the item is found in the hash table and there is more than 1 element left 
            after the deletion of a item (key value pairs).
            Worst: O(location_list + array_size) when the item is found and the hash table where the 
            item is located has only 1 item left which is located at the end of the array after 
            the deletion.
        '''
        table_index = location_list[locate_index]
        if path_distance == 0 and locate_index == list_len - 1:
            hash_table.array[table_index] = None
            hash_table.count -= 1
            
            # If there is only 1 item left in the hash table after deletion.
            if len(hash_table) <= 1:
                for i in range(len(hash_table.array)): # O(array_size)
                    if hash_table.array[i] is not None:
                        only_item_from_table = hash_table.array[i]
                        break
                if hash_table != self:
                    return only_item_from_table
            return 
            
        else:
            following_hash_table = hash_table.array[table_index][1]
            only_item_from_table = self.delete_item_aux(following_hash_table, location_list, locate_index + 1, path_distance - 1, list_len)
            hash_table.count -= 1
            
            # Checks if it does not return anything.
            if only_item_from_table == None:
                return 
            
            if len(hash_table) > 1 or hash_table == self:
                hash_table.array[table_index] = only_item_from_table
                return 
            
            hash_table.array[table_index] = None
            return only_item_from_table


    def __len__(self) -> int:
        # Time Complexity (Best and Worst): O(1)
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        len(key): Length (size) of the key.
        hash: Hash function for giving expected position of the hash table
        at each level.
        isinstance: Type checking operator which checks the type of 
        an object.
        comp: Comparision operator for strings ('==' specifically).

        Time Complexity:
            Best: O(hash) when the item is not found in the first (1st) 
            hash table.
            Worst: O(len(key)*(hash + comp + isinstance)) when the item is found or not found
            in the last hash table as there are many keys that are similar to the input key.
        """
        self.location_lst = []
        self.get_item_aux(self, key, 0)
        location_list = self.location_lst
        return location_list

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current = None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.

        n: Number of words inserted in the hash table.
        A: Size of the alphabet (A-Z) (a total of 26 letters).
        l: Length of the longest word.

        Time Complexity:
        Best: O(a), when all of the keys were stored in the first
        (or surface level) hash table as all the keys are completely
        different from each other.
        Worst: O(a*n*l), when the hash table has many keys and have similar alphabet 
        letters among them.
        """
        return self.sort_keys_aux()
    
    def sort_keys_aux(self, sorted_list : list = []):
        '''
        Auxiliary method for sort_keys

        n: Number of words inserted in the hash table.
        a: Size of the alphabet (A-Z) (a total of 26 letters).
        l: Length of the longest word.

        Time Complexity:
        Best: O(a), when all of the keys were stored in the first
        (or surface level) hash table as all the keys are completely
        different from each other.
        Worst: O(a*n*l), when the hash table has many keys and have similar alphabet 
        letters among them.
        '''

        if self.array[-1] is not None and self.level != 0:
            sorted_list.append(self.array[-1][0])
            
        # A loop is used to produce ASCII codes from lowercase a to z.
        for i in range(97, 123):
            position = ord(chr(i)) % (self.TABLE_SIZE - 1)
            if self.array[position] is not None:

                # Checks whether the tuple of the array has infinite hash
                # table in it.
                if isinstance(self.array[position][1], InfiniteHashTable):
                    # The array becomes the next hash table array.
                    self.array[position][1].sort_keys_aux(sorted_list)
                else:
                    sorted_list.append(self.array[position][0])
        return sorted_list