from dataclasses import dataclass

from parsec import optional
from model.model import Model
from typing import Counter, List, Optional
from model.operation import Operation, Transition
from predicates.state import State
from predicates.guards import Guard
from predicates.actions import Action

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
acount_time=True

def plan(state: State, goal: Guard, model: Model, max_depth: int = 20) -> Optional[List[str]]:
    stack = []
    state_op_weight = [state,[],0]
    stack.append(state_op_weight) #stack is a nested list with state and operations to that state

    visited = set()

    while stack:
        (current_state,operations,time) = stack.pop(0) 

        if len(operations)>max_depth:
            print("number of operations =", len(operations))
            return None
        
        if goal.eval(current_state):
            print("visited states, ", len(visited))
            return operations  #return list of operations

        if current_state not in visited:
            visited.add(current_state)
            
            for op in model.operations:
                if model.operations[op].eval(current_state):
                    next_state = model.operations[op].next_planning(current_state)
                    new_time = model.operations[op].time + float(time)
                    ops_copy = operations.copy()
                    ops_copy.append(op)
                        
                    state_ops_time = [next_state,ops_copy,new_time]
                    stack.append(state_ops_time)

            if acount_time:
                stack.sort(key=lambda x:x[2])


    print("Number of visited ", len(visited))
    print("Stack empty")
    return None
