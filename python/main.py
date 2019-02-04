
from models.device import Device
from models.sensor import Sensor
from run import run
from storage.base import get_session
import datetime

import logging
logging.getLogger().setLevel(logging.INFO)

logging.info("***STARTING SYSTEM***")

if __name__ == '__main__':
    session = get_session()
    device = Device(name="ToF-1")
    session.add(device)
    sensor1 = Sensor(name="Sensor 1", device=device)
    session.add(sensor1)
    sensor2 = Sensor(name="Sensor 2", device=device)
    session.commit()

    run(sensor1.id, sensor2.id)



