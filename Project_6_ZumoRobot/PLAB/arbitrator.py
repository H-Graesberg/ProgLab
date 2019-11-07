import random


class Arbitrator:
    """Determines which behavior that wins thus getting its motor recomendations
    transferred to the agent's motobs"""

    def __init__(self, bbcon=None, stochastic=False):
        """ Stochastic indicates if the choice should be stochastic or not. (True/False)"""
        self.bbcon = bbcon
        self.stochastic = stochastic

    def choose_action(self):
        """ Checks all of the active behaviors and picks a winner."""
        active_behaviors = self.bbcon.active_behaviors

        chosen_behavior = active_behaviors[0]

        if self.stochastic:
            last_weight = 0
            weights = []
            for i in range(len(active_behaviors)):
                last_weight = active_behaviors[i].weight + last_weight
                weights.append(last_weight)

            random_number = random.randrange(0, last_weight)

            for current_weight in weights:
                if current_weight > random_number:

                    chosen_behavior = active_behaviors[weights.index(
                        current_weight)]  # This is weird, should

                    break

        else:
            for behavior in active_behaviors:
                #print(behavior, " vekt til denne ", behavior.weight)
                if behavior.weight > chosen_behavior.weight:
                    chosen_behavior = behavior

        """Return a tuple containing motor recommendations to move the robot and a boolean
        indicating whether or not the run should be halted"""

        if chosen_behavior.halt_request == True:
            return "F"
        if chosen_behavior.motor_recommendation is None:
            chosen_behavior.motor_recommendation = "F"
        print("Chosen behavior is: ", chosen_behavior)
        return chosen_behavior.motor_recommendation
        # return "F"


def main():
    arbitrator = Arbitrator()
    arbitrator.stochastic = False

    arbitrator.choose_action()
