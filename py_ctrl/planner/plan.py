from dataclasses import dataclass

from parsec import optional
from model.model import Model
from typing import Counter, List, Optional
from model.operation import Operation, Transition
from predicates.state import State
from predicates.guards import Guard
from predicates.actions import Action
""" 

def plan(state: State, goal: Guard, model: Model, max_depth: int = 20) -> Optional[List[str]]:
"""
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
"""
    order=[]
    goal

    while not goal.eval(state):
        stack=[state]
        controled_stack=[state]
        while stack and len(stack)<max_depth:
            for i in stack:
                
                stack.pop(0)
                
                for op in model.operations:
                    if (model.operations[op].eval(i) and model.operations[op].next_planning(i) not in controled_stack):
                        
                        if goal.eval(model.operations[op].next_planning(i)):
                            order.insert(0,model.operations[op].name)
                            goal=model.operations[op].precondition.guard
                            break
                        stack.append(model.operations[op].next_planning(i))
                        controled_stack.append(model.operations[op].next_planning(i))
        if not order:
            return None

    return order

"""

def plan(state: State, goal: Guard, model: Model, max_depth: int = 20) -> Optional[List[str]]:
    stack = []
    state_op_weight = [state,[],0]
    stack.append(state_op_weight) #stack is a nested list with state and operations to that state

    visited = []
    while stack:
        current_state = stack.pop(0) 
        if len(current_state[1])>max_depth:
            print("number of operations =", len(current_state[1]))
            return None
        else:
            state_copy = current_state.copy()
            if goal.eval(state_copy[0]):
                return state_copy[1]
            
            for op in model.operations:
                next_state = model.operations[op].next_planning(state_copy[0])
                if model.operations[op].eval(state_copy[0]) and next_state not in visited:
                    w = state_copy[2]
                    weight = model.operations[op].weight + int(w)
                    ops_copy = state_copy[1].copy()
                    ops_copy.append(op)
                   
                    if goal.eval(next_state):
                        print("visited states, ", len(visited))
                        return ops_copy  #return list of operations

                    elif next_state not in stack:

                        state_ops_weights = [next_state,ops_copy,weight]
                        stack.append(state_ops_weights)
                    
                state_copy = current_state.copy()
            visited.append(current_state[0])
        stack = sorted(stack, key=lambda x:x[2])
    print("Number of visited ", len(visited))
    print("Stack empty")
    return None
