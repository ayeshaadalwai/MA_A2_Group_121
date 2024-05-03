from __future__ import annotations
from dataclasses import dataclass

from computer import Computer

from typing import TYPE_CHECKING, Union


# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType

from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack

@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """Removes the branch, should just leave the remaining following route."""
        return self.following.store

@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.
        """
        return self.following.store

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        return RouteSeries(computer, Route(RouteSeries(self.computer, self.following)))

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        return RouteSeries(self.computer, following= Route(RouteSeries(computer, self.following)))

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """
        return RouteSplit(Route(), Route(), Route(RouteSeries(self.computer, self.following)))

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        return RouteSeries(self.computer, following = Route(
            store=RouteSplit(
                top = Route(store= None), 
                bottom = Route(store= None), 
                following = self.following)))


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """
        return Route(RouteSeries(computer, Route(self.store)))

    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        return Route(store=RouteSplit( \
            top = Route(store = None), \
            bottom = Route(store = None), \
            following = Route(store = None) \
            ))

    def follow_path(self, virus: VirusType) -> None:
        """Follow a path and add computers according to a virus_type.
        
        n: Total number of branches due to RouteSplits.
        m: Total number of computers
        isinstance: Comparsion operator to check the object matches to its 
        data type or class.
        
        Time Complexity:
        Best: O(isinstance), when there is only one RouteSeries and no branches on the route..
        Worst: O(n*m*isinstance), when the path decided by the virus (via "select_branch" method)
        encounters a large amount of RouteSplits and computers on the route.
        """
        path = self
        stop = False
        following_items_stack = LinkedStack()

        # Infinite loop is used to traverse the Route.
        while True:
            if isinstance(path.store, RouteSplit):
                path = path.store
                branch_decision = virus.select_branch(path.top, path.bottom)

                if isinstance(path.following.store, RouteSeries) and isinstance(path.following.store.computer, Computer):
                    following_route = path.following
                    reversed_stack = LinkedStack()
                    
                    # A loop is used to add all computers in the following branch
                    while following_route.store != None:
                        reversed_stack.push(following_route.store.computer)
                        following_route = following_route.store.following

                    while not reversed_stack.is_empty():
                        following_items_stack.push(reversed_stack.pop())
                
                if branch_decision == BranchDecision.TOP:
                    if isinstance(path.top.store, RouteSeries):
                        if isinstance(path.top.store.computer, Computer):
                            virus.add_computer(path.top.store.computer) 
                        path = path.top.store.following
                    elif isinstance(path.top.store, RouteSplit):
                        path = path.top
                    
                    # Checks if it reaches the end of the top branch.
                    elif path.top.store == None: 
                        break

                elif branch_decision == BranchDecision.BOTTOM:
                    if isinstance(path.bottom.store, RouteSeries):
                        if isinstance(path.bottom.store.computer, Computer):
                            virus.add_computer(path.bottom.store.computer) 
                        path = path.bottom.store.following
                        
                    elif isinstance(path.bottom.store, RouteSplit):
                        path = path.bottom 
                    
                    # Checks if it reaches the end of the bottom branch.
                    elif path.bottom.store == None: 
                        break

                elif branch_decision == BranchDecision.STOP:
                    stop = True 
                    break 
            
            elif isinstance(path.store, RouteSeries):
                virus.add_computer(path.store.computer)
                path = path.store.following
                    
            # Checks if it reaches the end of the route
            else:
                break
        
        # A loop is used to add computers in the following branch
        # into the computer list that are transmitted by the virus.
        while not following_items_stack.is_empty() and not stop:
            virus.add_computer(following_items_stack.pop())


    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route.
        
        n: Total number of computers and branches combined.
        
        Time Complexity (Best and Worst): O(n)
        """
        return self.add_all_computers_aux(self, [])

    def add_all_computers_aux(self, route:Route, computer_list:list[Computer]):
        """
        Auxiliary method for add_all_computers 

        n: Total number of computers and branches combined.
        
        Time Complexity (Best and Worst): O(n)
        """
        
        # Checks whether reaches the end of the route
        if route.store == None:
            return 
        
        # Checks whether reaches the RouteSeries which
        # stores the computer
        elif isinstance(route.store, RouteSeries):
            computer_list.append(route.store.computer) 
            route = route.store.following
            self.add_all_computers_aux(route, computer_list) 
        
        # Checks whether it reaches RouteSplit which separates
        # into 3 branches (top, bottom, following)
        elif isinstance(route.store, RouteSplit):
            self.add_all_computers_aux(route.store.top, computer_list) # Top branch
            self.add_all_computers_aux(route.store.bottom, computer_list)  # Bottom branch
            self.add_all_computers_aux(route.store.following, computer_list)  # Following branch

        return computer_list