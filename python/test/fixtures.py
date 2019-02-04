from unittest import TestCase

from models.device import Device
from models.sensor import Sensor
from storage.base import get_session


class BaseTest(TestCase):
    """Convenience class for creating simple test cases."""

    def create_fixtures(self):
        """Create a device with two sensors."""
        self.device1 = Device(name="ToF-1")
        self.sensor1 = Sensor(name="S-1", device=self.device1)
        self.sensor2 = Sensor(name="S-2", device=self.device1)
        self.session.add_all([self.device1, self.sensor1, self.sensor2])
        self.session.commit()

    def setUp(self):
        """"Create a session and fixtures."""
        self.session = get_session()
        self.create_fixtures()

    def test_init(self):
        self.assertTrue(True)
