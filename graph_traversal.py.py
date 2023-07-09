class Node:
    #node class, stores the state of the puzzle, as well as children and parent nodes
    def __init__(self, peg1, peg2, peg3):
        self.peg1 = peg1
        self.peg2 = peg2
        self.peg3 = peg3 #'pegs' are lists of integers, representing the disks on each peg
        self.parent = None 
        self.children = [] #states that can be reached from the current state
        self.puzzle = [self.peg1, self.peg2, self.peg3] #contains the entire puzzle state
        self.g = 0 #depth of the node
        self.f = self.get_f_value() #heuristic value of the node
    
    def create_child(self, peg1, peg2, peg3): #represent a new state reachable from the current state
        child = Node(peg1, peg2, peg3) #create a new node
        child.parent = self #parent of node is current node
        self.children.append(child) #add child to children list
        child.g = self.g + 1 #depth of child is depth of parent + 1
    
    def get_f_value(self): #calculate the heuristic value of the node
        h = len(self.peg3) #number of disks on peg 3
        #heuristic value is the number of disks on peg 3
        return h + self.g #f = g + h
        
      
    def goal_test(self): #have we solved the puzzle?
        goal_state = [5, 4, 3, 2, 1] #define the goal state
        return self.peg3 == goal_state and not self.peg1 and not self.peg2
        #if peg3 is arranged in ascending order with all disks we have reached the goal state
    def print_puzzle(self): #display the state of the puzzle at each step
        print('Peg1:', self.peg1)
        print('Peg2:', self.peg2)
        print('Peg3:', self.peg3) #print 'peg' array
    
    def steps(self): 
        #the minimum number of steps to solve the tower of hanoi is 2^n - 1
        #where n is the number of disks
        #calculate the minimum solution
        disks = len(self.peg1)
        steps = 2**disks - 1
        return f"The minimum number of steps to solve this puzzle with {disks} disks is: {steps}"
    
    def generate_moves(self):
     if self.children == []: #only generate moves once ie. if the children list is empty
      for peg, inital_peg in enumerate(self.puzzle):  # for each peg
        if len(inital_peg) != 0:  # if the initial peg is not empty
            disk = inital_peg[-1]  # -1 index gives the top disk
            for index, target_peg in enumerate(self.puzzle):  # for each peg
                if peg != index:  # as long as the pegs are not the same
                    new_puzzle = [peg.copy() for peg in self.puzzle]  # make a copy of the puzzle
                    new_puzzle[peg].remove(disk)
                    new_puzzle[index].append(disk)
                    # in the new puzzle perform the move
                    if len(target_peg) == 0 or target_peg[-1] > disk:
                        self.create_child(*new_puzzle)  # form a new node from the new state if the move is safe
                        print(f"Safe move from {self.puzzle} to {new_puzzle} generated.") #generate safe state
                    else:
                        print(f"Unsafe move {self.puzzle} to {new_puzzle} marked as dead-end.") #mark unsafe states and do not explore them further



class Search:
    # class to perform searching

    def depth_first_search(self, root, depth_limit=31): #depth limit is 31 as the minimum solution is 2^n - 1
        stack = []  # initialize stack
        visited = set()  # initialize visited set
        stack.append(root)  # append root to stack
        visited.add(self.puzzle_to_tuple(root.puzzle))  # add root to stack

        while stack:  # while the stack is not empty
            current_Node = stack.pop(0)  # pop element 0
            # Print each node just after it's popped from the stack
            print(f"Searching node: {current_Node.puzzle}")

            if current_Node.goal_test():  # when goal_test evaluates true
                path_to_solution = self.path_trace(current_Node)  # call path_trace
                return path_to_solution  # return path_to_solution

            current_Node.generate_moves()
            # call generate_moves to explore state_space
            # generate legal moves from current state

            for current_child in current_Node.children:  # for child states
                child_puzzle_tuple = self.puzzle_to_tuple(current_child.puzzle)  # convert to tuple
                if child_puzzle_tuple not in visited and current_child.g <= depth_limit:  # if child state not in visited and depth limit not reached
                    stack.append(current_child)  # add child to stack
                    visited.add(child_puzzle_tuple)  # add child to visited

    def puzzle_to_tuple(self, puzzle):
        return tuple(tuple(peg) for peg in puzzle)
        """'TypeError: unhashable type: 'list' was thrown because elements added
        to a set must be hashable (immutable). Tuples are hashable, so this function returns
        a tuple of tuples, which is hashable and can be added to the set"""

    def path_trace(self, node):  # store the path from the root node to the goal node
        current = node  # store input node as current
        path = []  # initialize path list
        path.append(current)  # add current to path
        while current.parent != None:  # while the parent of the current node is not None
            current = current.parent  # set current to the parent of the current node
            path.append(current)  # add current to path
        return path  # return the path to the goal state

    def a_star_search(self, root):
        open_list = [] #similar to DFS implentation, initialize open list and visited set
        visited = set()

        open_list.append(root) #append root to open list
        visited.add(self.puzzle_to_tuple(root.puzzle)) #add root to visited set
        #the puzzle_to_tuple function is called again to avoid hashable error

        while True: 
            current_Node = open_list.pop(0) #pop element 0 from open list
            print(f"Searching node: {current_Node.puzzle}")

            if current_Node.goal_test() == True: #if we have reached the goal state
                path_to_solution = self.path_trace(current_Node) #return the path to the goal state
                return path_to_solution

            current_Node.generate_moves() #generate valid states/moves from current state

            for current_child in current_Node.children: #for each child state
                child_puzzle_tuple = self.puzzle_to_tuple(current_child.puzzle) #convert to tuple
                if child_puzzle_tuple not in visited: #if child state not in visited
                    open_list.append(current_child) #add child to open list
                    visited.add(child_puzzle_tuple) #add child to visited set
 
            open_list.sort(key=lambda x: x.f) #anonymous function to sort open list by f value of states


#main function - creates UI for user to select which algorithm to use
def main():
    print('Initial State of puzzle:')
    root.print_puzzle()
    print("Which algorithm would you like to use ro solve the Tower of Hanoi?")
    print("1. Depth First Search")
    print("2. A* Search")
    print("3. Exit")
    choice = input("Please enter 1, 2, or 3: ")
    if choice == "1":
        print("Solving with Depth First Search")
        search = Search()
        solution_path = search.depth_first_search(root)
        # Display the action plan for DFS
        solution_path.reverse()  # Reverse the path to display the solution
        print("Path to solution:")
        for i, node in enumerate(solution_path):
            print(f"Step {i}")  # Print the step we are up to in the puzzle solution
            node.print_puzzle()
    elif choice == "2":
        print("Solving with A* Search")
        search = Search()
        solution_path = search.a_star_search(root)
        # Display the action plan for DFS
        solution_path.reverse()  # Reverse the path to display the solution
        print("Path to solution:")
        for i, node in enumerate(solution_path):
            print(f"Step {i}")  # Print the step we are up to in the puzzle solution
            node.print_puzzle()
    elif choice == "3":
        print("Exiting...")
        exit()
    else:
        print("Invalid input, please enter 1, 2, or 3")
        main()


# Initialize the puzzle, and display minimum number of steps to solve
initial_state = [5, 4, 3, 2, 1], [], []
root = Node(*initial_state)
print(root.steps())
# To attempt the puzzle with a different number of disks, change the initial state array

# Call main function
main()
#note your IDE may not print the entire output, may need to adjust IDE settings to allow more output or run in terminal

