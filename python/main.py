
from models.device import Device
from models.sensor import Sensor
from models.utils import get_or_create
from run import run
from storage.base import get_session


import logging
logging.getLogger().setLevel(logging.INFO)

logging.info("***STARTING SYSTEM***")

if __name__ == '__main__':
    session = get_session()
    device = Device(name="ToF-1")
    sensor1, created1 = get_or_create(session, Sensor, id=1)
    sensor2, created2 = get_or_create(session, Sensor, id=2)
    if created1 or created2:
        session.commit()

    run(sensor1.id, sensor2.id)



