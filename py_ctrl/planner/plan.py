from dataclasses import dataclass
from model.model import Model
from typing import List, Optional
from model.operation import Operation, Transition
from predicates.state import State
from predicates.guards import Guard
from predicates.actions import Action
    

def plan(state: State, goal: Guard, model: Model, max_depth: int = 20) -> Optional[List[str]]:
    """
    Find a sequence of operations to reach the goal from the given state or
    return None if you can not find a plan. Use max_depth to stop searching when you have more than
    max_depth steps in the path. 

    In planning you should use the eval() method of the operation to check if it is enabled and 
    the next_planning() to execute both pre, post and effect actions. While planning, no operations
    will run in parallell so they complete directly. We are only interested in finding the minimum 
    number of operations to reach the goal, not the shortest time.

    In the runner, there is a mode to pre-start operations, but that should not be considered while planning
    """
    s = state
    stack = []
    stack.append(s)
    depth = max_depth
    current_path = []
    visited = []
    while stack:
        for op in model.operations:
            current_state = stack.pop()
            print('Current state ', current_state)
            print('Current operation ', model.operations[op].eval(current_state))
            if model.operations[op].eval(current_state):
                depth -= 1
                current_path.append(op)
                visited.append(current_state)
                t = model.operations[op].next_planning(current_state)
                #print('next state', t)
                if t not in stack:
                    stack.append(t)
                if not stack and not goal.eval(current_state):
                    print('hej')
        stack.append(visited.pop(0))

    

"""
V1: False, V2: 0
o1
V1: True, V2: 0
o2
V1: True, V2: 1



"""
            