"""
Behavior file containing Behaviour superclass and its variants
"""
from ultrasonic import Ultrasonic


class Behavior:
    """Superclass to different behaviours,
    analyse a subset of sensory information to determine a motor request"""

    def __init__(self, bbcon=None, sensobs=None, motor_recommendation=None, active_flag=True,

                 halt_request=False, priority=0, match_degree=0):

        if sensobs is None:
            sensobs = []

        self.bbcon = bbcon
        self.sensobs = sensobs

        self.motor_recommendation = motor_recommendation

        self.active_flag = active_flag  # False as default, if this is active or not
        self.halt_request = halt_request  # If true, stop everything!
        # Hard to define value for behavior, must try different values
        self.priority = priority
        # Read values from sensobs and calculate importantness [0.0,..1]
        self.match_degree = match_degree
        self.weight = self.match_degree * self.priority  # This is value arbitrator reads!

    def consider_activation(self):
        """Test if inactive and should be activated"""
        raise NotImplementedError

    def consider_deactivation(self):
        """
        Tests if we should deactivate the behavior
        :return:
        """
        raise NotImplementedError

    def sense_and_act(self):
        """core computer, use sensob readings to produce motor-recommendations(and halt_request)"""
        raise NotImplementedError

    def update(self):
        """consider if active, and if active update all values"""
        self.consider_activation()
        if self.active_flag:
            self.sense_and_act()

    def weight_update(self):
        self.weight = self.match_degree * self.priority


class TrackLine(Behavior):
    """Behavior to track a line on the floor"""

    def __init__(self, bbcon=None, sensobs=None, motor_recommendation=None, active_flag=True,
                 halt_request=False):
        super().__init__(
            bbcon,
            sensobs,

            motor_recommendation,
            active_flag,
            halt_request,
            4)

        self.activation_limit = 50

    def consider_activation(self):
        """Read the values, if a line -> activate"""

        reflectance_values = self.get_reflectance_values()
        max_value = max(reflectance_values)
        min_value = min(reflectance_values)

        self.active_flag = min_value < 0.2

    def consider_deactivation(self):
        """
        Should we stop trackline behaviour?
        :return:
        """
        self.consider_activation()

    def sense_and_act(self):
        """update motor_recommendation and match_degree"""

        values = self.get_reflectance_values()
        max_index = values.index(max(values))

        min_index = values.index(min(values))

        if min_index == 2 or min_index == 3:
            self.match_degree = 1
            moto_rec = "F"
        elif min_index == 1 or min_index == 4:
            self.match_degree = 1
            if min_index == 1:
                moto_rec = "L"
            else:
                moto_rec = "R"
            moto_rec += str(10)
        else:
            self.match_degree = 1
            if min_index == 0:
                moto_rec = "L"
            else:
                moto_rec = "R"
            moto_rec += str(20)
        self.motor_recommendation = moto_rec
        self.weight_update()

    def get_reflectance_values(self):
        """
        Shortcut for getting the values afflicted with this behaviours reflectance sensors
        :return: Reflectance values
        """
        return self.sensobs.get_reflectance_values()


class DistanceAdjust(Behavior):

    def __init__(self, bbcon=None, sensobs=None, motor_recommendation=None, active_flag=True,
                 halt_request=False):
        super().__init__(bbcon, sensobs, motor_recommendation, active_flag,
                         halt_request, 5)

        self.constant_distance = 30

    def consider_activation(self):
        distance = self.get_distance_value()

        self.active_flag = distance < 2 * self.constant_distance


    def consider_deactivation(self):
        self.consider_activation()

    def sense_and_act(self):
        """update motor_recommendation and match_degree"""
        distance = self.get_distance_value()

        if distance < self.constant_distance:
            moto_rec = "B"
        else:
            moto_rec = "F"


        self.match_degree = max(
            min((1 - (distance / self.constant_distance)), 1), 0)
        self.motor_recommendation = moto_rec
        self.weight_update()


    def get_distance_value(self):
        """
        Shortcut for getting distance
        :return: Distance
        """

        ultra = Ultrasonic()
        ultra.update()
        value = ultra.get_value()


        return value


class FollowRed(Behavior):
    """Most read up on cam how it works with value_output"""

    def __init__(self, bbcon=None, sensobs=None, motor_recommendation=None, active_flag=True,
                 halt_request=False):
        super().__init__(bbcon, sensobs, motor_recommendation, active_flag,
                         halt_request, 4)

        self.value_example_cam = 50
        self.value_example_distance = 30
        self.val_list = [self.value_example_cam, self.value_example_distance]
        # not sure how we should store this values...

        image_test = self.get_image_data()
        # I think this works?
        self.width = image_test.width
        self.height = image_test.height

        self.red = (255, 0, 0)

    def consider_activation(self):
        red_percentage_needed_for_activation = 0.1

        colors = self.get_image_data().getcolors(3)  # Should be only 3 colors
        red_count = self.get_red_count(self.get_image_data())

        self.active_flag = red_count >= self.width * \
            self.height * red_percentage_needed_for_activation


    def consider_deactivation(self):
        '''same as activate'''
        self.consider_activation()

    def sense_and_act(self):
        """update motor_recommendation, halt_request, match_degree"""
        directions = ("L", "F", "R")

        moto_rec = ""


        image = self.get_image_data()
        direction_index = self.get_dominant_red_area(image)
        moto_rec += directions[direction_index]
        if moto_rec == "R" or moto_rec == "L":
            moto_rec += "10"
        self.motor_recommendation = moto_rec
        self.match_degree = min((((2.5*self.get_red_count(image) / (image.height * image.width))**2), 1))

        self.weight_update()

    def get_dominant_red_area(self, image):
        """
        Looks for red pixels, and returns which part of the image has the most red
        :param image: Image to lo search for red in
        :return: Index 0 for left, 1 for middle, and 2 for right
        """
        interval_size = image.width / 3

        counts = [0, 0, 0]

        for r in range(image.height):
            for c in range(image.width):
                pixel = image.getpixel((c, r))
                if pixel[0] > 100:
                    counts[int(c / interval_size)] += 1

        return counts.index(max(counts))

    def get_image_data(self):
        """
        Shortcut to getting the camera values
        :return: Camera values as Image object
        """
        return self.sensobs.get_camera_values()

    def get_wta_image_data(self):
        """
        Shortcut for getting the "pure" colored version with only RGB values
        :return:  Camera output with only RGB values
        """
        return self.get_image_data().map_color_wta()

    def get_red_count(self, image):
        """
        Count the number of red pixels in an image
        :param image: Image
        :return: Count of red pixels
        """

        red_count = 0

        for h in range(image.height):
            for w in range(image.width):
                if image.getpixel((w, h))[0] > 100:
                    red_count += 1

        return red_count
