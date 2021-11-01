from dataclasses import dataclass

from parsec import optional
from model.model import Model
from typing import List, Optional
from model.operation import Operation, Transition
from predicates.state import State
from  predicates.guards import Guard
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
    stack=[state]
    controled_stack=[state]
    while stack and len(stack)<max_depth:
        for i in stack:
            print(stack)
            stack.pop(0)
            #print("\t",stack)
            for op in model.operations:
                print (model.operations[op].precondition.guard.eval(i),":\n",model.operations[op].precondition.guard,"\t\t",i)
                if (model.operations[op].precondition.guard.eval(i) and model.operations[op].next_planning(i) not in controled_stack):
                    #print("test    ",model.operations[op].next_planning(state))
                    stack.append(model.operations[op].next_planning(i))
                    controled_stack.append(model.operations[op].next_planning(i))

                ##print(i,":\t",stack)
            print(stack)
            print("nytt test\n")

        


    raise NotImplementedError

