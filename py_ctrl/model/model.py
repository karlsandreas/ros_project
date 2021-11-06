from dataclasses import dataclass
from typing import List, Optional, Dict
from model.operation import Operation, Transition
from predicates.state import State
import predicates.guards
import predicates.actions
from predicates.guards import AlwaysFalse, AlwaysTrue, Guard
from handlers_msgs.msg import CubeState

@dataclass
class Model(object):
    initial_state: State
    operations: Dict[str, Operation]

    def __post_init__(self):
        ops = {o: "i" for o in self.operations}
        self.initial_state = self.initial_state.next(**ops)


g = predicates.guards.from_str
a = predicates.actions.from_str

def the_model() -> Model:
    """
    Here you should create the variables and operations that can be used both for planning to reach the goal 
    and running the simulator. I have made some operations and some dummy examples to get you going. But you
    probably have to modify this and the dummy operations, you can remove.
    Observe: The name of a variable can not be the same as any value since we have the variable_or_value strings. 
    The initial state of the cubes are: poses = {"pos1": "red_cube", "pos2": "blue_cube", "pos3": "green_cube"}
    """
    poses = {}
    initial_state = State(
        # control variables
        r1_ref = "home",            #{home, pos1, pos2, pos3}
        r1_grip = False,
        r2_ref = "home",            #{home, pos1, pos2, pos3}
        r2_grip = False,

        # measured variables
        r1_act = "home",            #{home, pos1, pos2, pos3}
        r1_gripping = False,
        r2_act = "home",            #{home, pos1, pos2, pos3}
        r2_gripping = False,

        #estimators for cube in each position
        posb1 = "red_cube",    # 1 is red, 2 is blue, 3 is green
        posb2 = "blue_cube",
        posb3 = "green_cube",
        block_in_r1 = "empty",     
        block_in_r2 = "empty",



    )

    # we will store all operations in this dict that will be part of the model
    ops = {}

    # this is maybe the simplest operation, to make the r1 (the small UR3e) robot
    # to go home
    ops[f"r1_to_home"] = Operation(
        # the name of the robot must be unique and can not be the same as any other operation
        # ar any variable in the state. This name will be part of the state to track if the
        # operation is executing (r1_to_home == "e") or not (r1_to_home == "i"). The operations
        # do not have a finished state. Changing this state is already handled inside the operation
        # so you do not need to do it here
        name=f"r1_to_home", 

        # the precondition defined when the operation is allowed to start and in this case r1_to_home
        # can start when the robot is not at the home position. For other motions, read about the 
        # requirements in the in the assignment.
        # When the runner starts the operation, it will call start(state) on the operaiton that will
        # call next(state) on the precondition transition. This will set the command variable r1_ref
        # to home so that the robot will go home. You can also add more actions here if for example
        # you need to block other operation to pre-start. You will read more about pre-start in the assignment
        precondition=Transition("pre", g(f"(r1_ref != home)"), a(f"r1_ref <- home")),

        # the postcondition defines when the operation has completed by checking the measured variables. This 
        # will not be possible when we are planning, since we do not have the real system then, so when
        # planning, we just skip to check these guards. Therefore you should only have measured variables in the guard.
        # However, in the action of the postcondition you should update your estimated variables that you 
        # expect from the operation and that you did not change when you started the operation. For example, it
        # in these actions that you update where the cubes are. In this case, we do not have any actions.
        postcondition=Transition("post", g(f"r1_act == home"), ()),

        # The effect are only used while planning to change measured variables that will change when running 
        # the simulation. This is important if for example other operations have these as precondition guard.
        effects=a(f"r1_act <- home")
    )

    ops[f"r2_to_home"] = Operation(
        name=f"r2_to_home", 
        precondition=Transition("pre", g(f"(r2_ref != home)"), a(f"r2_ref <- home")),
        postcondition=Transition("post", g(f"r2_act == home"), ()),
        effects=a(f"r2_act <- home")
    )



    # no you can add all the other operations that you need to make the robots to move between the positions
    # and to pick and place the cubes. i have added one more so that the robots move when running, but you need 
    # to modify this one since the robot is not allowed to move to pos1 if the other robot is there or if carries 
    # a cube and there is a cube in pos1



    # here is another example of two dummy operations showing that you can use an iterator to 
    # create multiple operations at the same time

    #Operations for moving r1 and r2 arm to pos 1,2,3
    for i in [1,2]:
        for j in [1,2,3]:
            ops[f"r{i}_to_pos{j}"] = Operation(
                name=f"r{i}_to_pos{j}", 
                precondition=Transition("pre", g(f"r{i}_ref != pos{j} && r{3-i}_ref != pos{j} && ((r{i}_gripping == True && posb{j} == empty) || (r{i}_gripping == False && posb{j} != empty))"), a(f"r{i}_ref <- pos{j}")),
                postcondition=Transition("post", g(f"r{i}_act == pos{j}"), ()),
                effects=a(f"r{i}_act <- pos{j}"),
            )


    #Operations for gripping with r1 and r2 at pos 1,2,3
    for i in [1,2]:
        for j in [1,2,3]:
            ops[f"r{i}_grip_pos{j}"] = Operation(
                name=f"r{i}_grip_pos{j}", 
                precondition=Transition("pre", g(f"r{i}_ref == pos{j} && r{3-i}_ref != pos{j} && r{i}_gripping == False"), a(f"r{i}_grip <- True")),
                postcondition=Transition("post", g(f"r{i}_gripping == True"), a(f"block_in_r{i} = posb{j}, posb{j} = empty")),
                effects=a(f"r{i}_gripping = True")
            )
    #Operations for dropping with r1 and r2 at pos 1,2,3
    for i in [1,2]:
        for j in [1,2,3]:
            ops[f"r{i}_drop_pos{j}"] = Operation(
                name=f"r{i}_drop_pos{j}", 
                precondition=Transition("pre", g(f"r{i}_ref == pos{j} && r{i}_gripping == True && posb{j} == empty"), a(f"r{i}_grip <- False")),
                postcondition=Transition("post", g(f"r{i}_grip == False"), a(f"posb{j} = block_in_r{i}, block_in_r{i} = empty")),
                effects=a(f"r{i}_gripping = False")
            )
                
    return Model(initial_state, ops)





    
def from_goal_to_goal(cube_goal: CubeState) -> Guard:
    """
    Create a goal predicate based on where the cubes should be placed.
    CubeState is the message that is received from ros and it includes where we want the 
    cube colors to be. The possible colors are "red_cube", "blue_cube", 
    "green_cube"
    """
    pos1: str = cube_goal.pos1
    pos2: str = cube_goal.pos2
    pos3: str = cube_goal.pos3

    #Cubes starting pos
    #red: pos1
    #blue: pos2
    #green: pos3

    # update this goal by converting the cubestate to a goal that you model understands
    # you will have some kind of estimated variables keeping track of where the cubes are
    # and these estimated variables should have the correct color. use the guards from_string parser
    # to simplify this and the g(f"v1 == {pos1} && v2 == {pos2}") notation

    goal=g(f"posb1 == {pos1} && posb2 == {pos2} && posb3 == {pos3}")
    
    return goal





