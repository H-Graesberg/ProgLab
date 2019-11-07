"""
File containing the main BBCON Class
"""

from time import time

from arbitrator import Arbitrator
from behavior import DistanceAdjust, TrackLine, FollowRed
from camera import Camera
from motob import Motob
from reflectance_sensors import ReflectanceSensors
from sensob import Sensob
from ultrasonic import Ultrasonic
import pdb
from zumo_button import ZumoButton

WAITING_TIME = 0.1


class BBCON:
    """
    Behavior-based controller
    """

    # Arbitrator need a pointer to the BBCON
    def __init__(self, behaviors=None, active_behaviors=None,
                 sensobs=None, motobs=Motob(), arbitrator=Arbitrator()):
        # Make arguments non-mutable (because PyCharm says so)

        if sensobs is None:
            sensobs = []
        if active_behaviors is None:
            active_behaviors = []
        if behaviors is None:
            behaviors = []

        # Checks if bbcon pointer is initialized
        if arbitrator.bbcon is None:
            arbitrator.bbcon = self

        # Save arguments
        self.behaviors = behaviors
        self.active_behaviors = active_behaviors
        self.sensobs = sensobs
        self.motobs = motobs

        self.arbitrator = arbitrator

        # Save halt flag
        self.halt_request = False

    def add_behavior(self, behavior):
        """
        Adds a behavior to the bbcon
        :param behavior: Behavior to add
        :return:
        """
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        """
        Add a new sensob to bbcons sensob's
        :param sensob: Sensob to add
        :return:
        """
        self.sensobs.append(sensob)

    def add_motob(self, motob):
        """
        Add a new motob to bbcon's motobs
        :param motob:
        :return:
        """
        self.motobs.append(motob)

    def activate_behavior(self, behavior):
        """
        Adds an existing behavior from the list of behaviors to the active ones
        :param behavior:
        :return:
        """
        self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        """
        Removes an active behavior from the list of active ones
        :param behavior:
        :return:
        """
        self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        """
        Core activity for the bbcon! This is where robot logic happens
        :return:
        """

        # 1. Update all sensobs
        for sensob in self.sensobs:
            sensob.update()

        # 2. Update all behaviors
        for behavior in self.behaviors:
            behavior.update()

        # 3. Invoke the arbitrator
        motor_recommendation = self.arbitrator.choose_action()
        # Remember halt request

        #if motor_recommendation == "S":
        #    self.halt_request = False
        #else: self.halt_request = True

        #pdb.set_trace()
        self.motobs.update(motor_recommendation)
        # 4. Update motobs
       # for motob in self.motobs:
        #    motob.update(motor_recommendation)

        # 5. Wait
        start_of_wait = time()
        while time() <= start_of_wait + WAITING_TIME:
            # Wait, and let the motors do something
            pass

        # 6. Reset sensobs
        for sensob in self.sensobs:
            sensob.reset()


# Main function
def main():
    #pdb.set_trace()
    ZumoButton().wait_for_press()
    bbcon = BBCON()


    # Sensors:
    reflectance_sensor = ReflectanceSensors()
    ultrasonic_sensor = Ultrasonic()
    camera_sensor = Camera()

    # Sensobs
    reflectance_sensob = Sensob(reflectance_sensor)
    ultrasonic_sensob = Sensob(ultrasonic_sensor)
    camera_sensob = Sensob(camera_sensor)

    trackline_sensobs = reflectance_sensob
    distance_adjust_sensobs = ultrasonic_sensob

    follow_red_sensobs = camera_sensob

    # Add to bbcon:

    # Add sensobs
    bbcon.add_sensob(trackline_sensobs)
    bbcon.add_sensob(distance_adjust_sensobs)
    bbcon.add_sensob(follow_red_sensobs)

    # Add motobs:
    bbcon.motobs = Motob()

    # Add behaviors
    bbcon.add_behavior(TrackLine(bbcon, trackline_sensobs))
    bbcon.add_behavior(DistanceAdjust(bbcon, distance_adjust_sensobs))
    bbcon.add_behavior(FollowRed(bbcon, follow_red_sensobs))

    # Set all behaviors to active at start; disable if not needed
    for behavior in bbcon.behaviors:
        bbcon.activate_behavior(behavior)

    # Run as long as robot is not halted
    # not bbcon.halt_request
    #pdb.set_trace()
    while True:
        bbcon.run_one_timestep()



if __name__ == "__main__":
    main()
