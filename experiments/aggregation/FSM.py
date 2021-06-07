from statemachine import StateMachine, State

class CockroachStateMAchine(StateMachine):
    wandering = State('Wandering', initial=True)
    joining = State('Join')
    still = State('Still')
    leaving = State('Leave')

    joining_start = wandering.to(joining)
    still_start = joining.to(still)
    leaving_start = still.to(leaving)
    wandering_start = leaving.to(wandering)