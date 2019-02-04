from models.sensor import Sensor
from run import run
from test.fixtures import BaseTest


class TestRun(BaseTest):

    def test_run(self):
        run(self.sensor1.id, self.sensor2.id)
        sensor1_measurements = self.session.query(Sensor).get(self.sensor1.id).measurements
        sensor2_measurements = self.session.query(Sensor).get(self.sensor2.id).measurements
        self.assertEqual(3, len(sensor1_measurements))
        self.assertEqual(3, len(sensor2_measurements))

        self.assertEqual(1.0, sensor1_measurements[0].distance)
        self.assertEqual(1.0, sensor2_measurements[0].distance)

        self.assertEqual(2.0, sensor1_measurements[1].distance)
        self.assertEqual(2.0, sensor2_measurements[1].distance)

        self.assertEqual(3.0, sensor1_measurements[2].distance)
        self.assertEqual(3.0, sensor2_measurements[2].distance)
