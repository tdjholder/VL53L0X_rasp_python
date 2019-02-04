
from sqlalchemy import Column, Integer, String, ForeignKey

from models.device import Device
from storage.base import Base, engine
from sqlalchemy.orm import relationship


class Sensor(Base):
    """Represents a ToF sensor."""

    __tablename__ = 'sensor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship("Device", back_populates="sensors")
    measurements = relationship("Measurement", back_populates="sensor")

    def __repr__(self):
        return "<Sensor(id='%d', name='%s')>" % (self.id, self.name)


Base.metadata.create_all(engine)

