from batch.main import get_readings_by_date, build_csv, run
from test.fixtures import BaseTest
from run import run as main_run
import datetime


class TestBatch(BaseTest):
    """Test the batch functionality."""

    def setUp(self):
        """Setup the sensors and run the sensors."""
        super().setUp()
        main_run(self.sensor1.id, self.sensor2.id)
        self.cob_date = datetime.datetime.utcnow().date()

    def test_get_readings(self):
        readings = get_readings_by_date(self.sensor1.id, self.sensor2.id, cob_date=self.cob_date)
        self.assertEqual(6, len(readings))
        self.assertTrue(readings[0].created_date > readings[5].created_date)

        readings = get_readings_by_date(self.sensor1.id, self.sensor2.id, cob_date=datetime.date(1970, 1, 1))
        self.assertEqual(0, len(readings))

    def test_build_csv(self):
        readings = get_readings_by_date(self.sensor1.id, self.sensor2.id, cob_date=self.cob_date)
        self.assertEqual(7, len(build_csv(readings).getvalue().splitlines()))

    def test_send_email(self):
        run(self.sensor1.id, self.sensor2.id, cob_date=self.cob_date)
