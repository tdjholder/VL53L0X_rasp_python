import mock
import time
import platform
import logging
import polyfiller
from simple_settings import settings
from models.measurements import Measurement
from models.sensor import Sensor
from storage.base import get_session

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

try:
    import VL53L0X
except ImportError as e:
    if platform.system() == 'Linux':
        raise e
    VL53L0X = polyfiller

try:
    import RPi.GPIO as GPIO
except ImportError:
    if platform.system() == 'Linux':
        raise e
    GPIO = mock.Mock()


def get_sensors():
    """Configure all of the GPIO settings."""
    GPIO.setwarnings(False)

    # Setup GPIO for shutdown pins on each VL53L0X
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor1_shutdown, GPIO.OUT)
    GPIO.setup(sensor2_shutdown, GPIO.OUT)

    # Set all shutdown pins low to turn off each VL53L0X
    GPIO.output(sensor1_shutdown, GPIO.LOW)
    GPIO.output(sensor2_shutdown, GPIO.LOW)

    # Keep all low for 500 ms or so to make sure they reset
    time.sleep(0.50)

    tof = VL53L0X.VL53L0X(address=0x2B)
    tof1 = VL53L0X.VL53L0X(address=0x2D)

    # Set shutdown pin high for the first VL53L0X then
    # call to start ranging
    GPIO.output(sensor1_shutdown, GPIO.HIGH)
    time.sleep(0.50)
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    log.info("Sensor 0 working")
    # Set shutdown pin high for the second VL53L0X then
    # call to start ranging
    GPIO.output(sensor2_shutdown, GPIO.HIGH)
    time.sleep(0.50)
    tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    log.info("Sensor 1 working")

    return tof, tof1


def record_distance(tof, idx):
    """Given a sensor, get the current distance and save it."""
    session = get_session()
    sensor = session.query(Sensor).get(idx)
    measurement = Measurement(distance=tof.get_distance(), sensor=sensor)
    session.add(measurement)
    session.commit()


def run(idx1, idx2):
    """Run the program."""
    tof, tof1 = get_sensors()
    count = 0
    while True:
        count += 1
        record_distance(tof, idx1)
        record_distance(tof1, idx2)
        time.sleep(settings.READING_INTERVAL)
        if settings.BREAK_COUNT and count > settings.BREAK_COUNT:
            break




