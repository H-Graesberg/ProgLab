"""
File containing the sensob class for interface between sensor(s) and behaviour
"""
from camera import Camera
from irproximity_sensor import IRProximitySensor
from reflectance_sensors import ReflectanceSensors
from ultrasonic import Ultrasonic
import time


class Sensob:
    """
    Interface between sensors and the bbcon's behaviors
    """

    def __init__(self, *sensors):
        # The sensors are "sensor-value"-mappings
        self.sensors = {}

        # Initialize with sensors
        for sensor in sensors:
            # Each sensor is added along with its value
            self.add_sensor(sensor)

        # Set current values
        self.update()

    def add_sensor(self, sensor):
        """
        Adds a sensor and immediatly updates its value
        :param sensor: New sensor to be added
        :return:
        """
        self.sensors[sensor] = sensor.update()

    def remove_sensor(self, sensor):
        """
        Remove sensor (if this is ever necessary?)
        Does nothing if sensor does not exist
        :param sensor: Sensor to remove
        :return:
        """
        self.sensors.pop(sensor)

    def update(self):
        """
        Fetches all current values from sensors and saves them in the sensor map.
        Calls update on all sensors
        :return:
        """
        for sensor in self.sensors.keys():
            self.sensors[sensor] = sensor.update()

    def reset(self):
        """
        Resets the sensob by resetting all associated sensors
        :return:
        """
        for sensor in self.sensors.keys():
            sensor.reset()

    def get_camera(self):
        """
        Gets the camera if it exists
        :return: Camera or None
        """
        return self.get_sensor(Camera)

    def get_camera_values(self):
        """
        Gets the values from the camera
        :return: Camera values in form of an array
        """
        return self.get_sensor_values(Camera)

    def get_ir_proximity_sensor(self):
        """
        Gets the proximity sensor if it exists
        :return: Proximity sensor or None
        """
        return self.get_sensor(IRProximitySensor)

    def get_ir_proximity_values(self):
        """
        Gets the values from the camera
        :return: Camera values in form of an array
        """
        return self.get_sensor_values(IRProximitySensor)

    def get_reflectance_sensor(self):
        """
        Gets the reflectance sensor if it exists
        :return: Reflectance sensor or None
        """
        return self.get_sensor(ReflectanceSensors)

    def get_reflectance_values(self):
        """
        Gets the values from the camera
        :return: Camera values in form of an array
        """
        ret = self.get_sensor_values(ReflectanceSensors)
        return ret

    def get_ultrasonic_sensor(self):
        """
        Gets the ultrasonic sensor if it exists
        :return: Ultrasonic sensor or None
        """
        return self.get_sensor(Ultrasonic)

    def get_ultrasonic_values(self):
        """
        Gets the values from the camera
        :return: Camera values in form of an array
        """
        return self.get_sensor_values(Ultrasonic)

    def get_sensor(self, sensor_class):
        """
        Helper function for fetching a specific sensor if it exists
        :param sensor_class: Class of the sensor
        :return: Sensor or None
        """

        for sensor in self.sensors.keys():
            if isinstance(sensor, sensor_class):
                return sensor

        # If sensor doesn't exist, return None
        return None

    def get_sensor_values(self, sensor_class):
        """
        Helper function to get values afflicted with a sensor
        :param sensor_class: Class of the sensor
        :return: Values or None
        """
        ultra = Ultrasonic()
        ultra.update()

        sensor = self.get_sensor(sensor_class)

        if sensor is not None:
            return self.sensors[sensor]

        else:
            return None


def main():
    ultra = Ultrasonic()
    while True:
        ultra.update()
        ultra.get_value()
        time.sleep(0.001)
# main()
