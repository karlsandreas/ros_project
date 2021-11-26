import pytest
from predicates.state import State
from predicates import guards, actions
from model.operation import Transition, Operation
from predicates.errors import NextException
from model.model import Model, the_model, from_goal_to_goal
from handlers_msgs.msg import CubeState

def test_model_creation():
    m = the_model()
    enabled_in_initial = [o for name, o in m.operations.items() if o.eval(m.initial_state)]
    assert len(enabled_in_initial) > 0


# write your own tests so that you know that the model you have created is the one you expected.
# for example, write a test for each operation so that it is enabled in the correct states and
# that it changes the state both when using next_planning and start and complete

def test_r1_to_home():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r1_ref = "pos1", r1_act = "pos1",r1_gripping = True)
    o = ops["r1_to_home"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r1_act = "home"))
    after_completed = o.complete(after_start.next(r1_act = "home"))

    assert o.eval(test_state)
    assert after_start == test_state.next(r1_ref = "home", r1_to_home = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r1_act = "home", r1_to_home = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r1_ref = "home", r1_act = "home")

def test_r1_to_pos1():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r1_ref = "pos2", r1_act = "pos2") #r1 from pos2 to pos1
    o = ops["r1_to_pos1"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r1_act = "pos1"))
    after_completed = o.complete(after_start.next(r1_act = "pos1"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r1_ref = "pos1", r1_to_pos1 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r1_act = "pos1", r1_to_pos1 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r1_ref = "pos1", r1_act = "pos1")


def test_r1_to_pos2():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r1_ref = "pos1", r1_act = "pos1") #r1 from pos1 to pos2
    o = ops["r1_to_pos2"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r1_act = "pos2"))
    after_completed = o.complete(after_start.next(r1_act = "pos2"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r1_ref = "pos2", r1_to_pos2 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r1_act = "pos2", r1_to_pos2 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r1_ref = "pos2", r1_act = "pos2")

def test_r1_to_pos3():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r1_ref = "pos1", r1_act = "pos1") #r1 from pos1 to pos3
    o = ops["r1_to_pos3"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r1_act = "pos3"))
    after_completed = o.complete(after_start.next(r1_act = "pos3"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r1_ref = "pos3", r1_to_pos3 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r1_act = "pos3", r1_to_pos3 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r1_ref = "pos3", r1_act = "pos3")


def test_r2_to_home():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r2_ref = "pos1", r2_act = "pos1", r2_gripping = True)
    o = ops["r2_to_home"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r2_act = "home"))
    after_completed = o.complete(after_start.next(r2_act = "home"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r2_ref = "home", r2_to_home = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r2_act = "home", r2_to_home = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r2_ref = "home", r2_act = "home")

def test_r2_to_pos3():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r2_ref = "pos1", r2_act = "pos1") #r2 start in pos1 and go to pos3
    o = ops["r2_to_pos3"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r2_act = "pos3"))
    after_completed = o.complete(after_start.next(r2_act = "pos3"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r2_ref = "pos3", r2_to_pos3 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r2_act = "pos3", r2_to_pos3 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r2_ref = "pos3", r2_act = "pos3")

def test_r2_to_pos2():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r2_ref = "pos1", r2_act = "pos1") #r2 start in pos1 and go to pos2
    o = ops["r2_to_pos2"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r2_act = "pos2"))
    after_completed = o.complete(after_start.next(r2_act = "pos2"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r2_ref = "pos2", r2_to_pos2 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r2_act = "pos2", r2_to_pos2 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r2_ref = "pos2", r2_act = "pos2")

def test_r2_to_pos1():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r2_ref = "pos2", r2_act = "pos2") #r2 start in pos2 and go to pos1
    o = ops["r2_to_pos1"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r2_act = "pos1"))
    after_completed = o.complete(after_start.next(r2_act = "pos1"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r2_ref = "pos1", r2_to_pos1 = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r2_act = "pos1", r2_to_pos1 = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r2_ref = "pos1", r2_act = "pos1")

def test_some_operations():
    m = the_model()
    s = m.initial_state
    at_p1 = m.operations["r1_to_pos1"].next_planning(s)
    assert guards.Eq("r1_act", "pos1").eval(at_p1)
"""
def test_r1_to_all_pos():
    positions = [2,3]

    for i in positions:
        m = the_model()
        ops = m.operations

        test_state = m.initial_state.next(r1_ref = f"pos{3-i}", r1_act = f"pos{i}")
        o = ops[f"r1_to_pos{i}"]
        
        after_start = o.start(test_state)
        not_completed = o.is_completed(after_start)
        completed = o.is_completed(after_start.next(r1_act = f"pos{i}"))
        after_completed = o.complete(after_start.next(r1_act = f"pos{i}"))
        
        assert o.eval(test_state)
        if i == 1:
            assert after_start == test_state.next(r1_ref = f"pos{i}", r1_to_pos1 = "e")
            assert after_completed == after_start.next(r1_act = f"pos{i}", r1_to_pos1 = "i")
        elif i == 2:
            assert after_start == test_state.next(r1_ref = f"pos{i}", r1_to_pos2 = "e")
            assert after_completed == after_start.next(r1_act = f"pos{i}", r1_to_pos2 = "i")
        elif i == 3:
            assert after_start == test_state.next(r1_ref = f"pos{i}", r1_to_pos3 = "e")
            assert after_completed == after_start.next(r1_act = f"pos{i}", r1_to_pos3 = "i")

        assert not not_completed
        assert completed
        
        after_planned = o.next_planning(test_state)
        assert after_planned == test_state.next(r1_ref = f"pos{i}", r1_act = f"pos{i}")
"""

def test_r1_to_all_pos():
    m = the_model()
    s = m.initial_state
    at_p1 = m.operations["r1_to_pos1"].next_planning(s)
    at_p2 = m.operations["r1_to_pos2"].next_planning(s)
    at_p3 = m.operations["r1_to_pos3"].next_planning(s)
    at_home = m.operations["r1_to_home"].next_planning(s)

    assert guards.Eq("r1_act", "pos1").eval(at_p1)
    assert guards.Eq("r1_act", "pos2").eval(at_p2)
    assert guards.Eq("r1_act", "pos3").eval(at_p3)
    assert guards.Eq("r1_act", "home").eval(at_home)

def test_r2_to_all_pos():
    m = the_model()
    s = m.initial_state
    at_p1 = m.operations["r2_to_pos1"].next_planning(s)
    at_p2 = m.operations["r2_to_pos2"].next_planning(s)
    at_p3 = m.operations["r2_to_pos3"].next_planning(s)
    at_home = m.operations["r2_to_home"].next_planning(s)

    assert guards.Eq("r2_act", "pos1").eval(at_p1)
    assert guards.Eq("r2_act", "pos2").eval(at_p2)
    assert guards.Eq("r2_act", "pos3").eval(at_p3)
    assert guards.Eq("r2_act", "home").eval(at_home)
# Write your own tests to check the all the operations 

def switch_pos1_pos2():
    m = the_model()
    s = m.initial_state
    grip_at_pos1 = m.operations["r1_grip_pos1"].next_planning(s)
    grip_at_pos2 = m.operations["r2_grip_pos2"].next_planning(s)
    drop_at_pos1 = m.operations["r1_drop_pos2"].next_planning(s)
    drop_at_pos2 = m.operations["r2_drop_pos1"].next_planning(s)
    print(grip_at_pos1)

def test_goal_to_goal():
    # you need to implement the translation from the goal message to your way of tracking the cubes
    cube_goal = CubeState()
    cube_goal.pos1 = "red_cube"
    cube_goal.pos2 = "blue_cube"
    cube_goal.pos3 = "green_cube"

    goal = from_goal_to_goal(cube_goal)
    m = the_model()
    assert goal.eval(m.initial_state)
