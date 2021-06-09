from statemachine import StateMachine, State

class CockroachStateMAchine(StateMachine):
    wandering = State('Wandering', initial=True)
    joining = State('Joininig')
    still = State('Still')
    leaving = State('Leaving')

    joining_start = wandering.to(joining)
    still_start = joining.to(still)
    leaving_start = still.to(leaving)
    wandering_start = leaving.to(wandering)