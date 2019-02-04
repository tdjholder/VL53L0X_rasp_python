
from sqlalchemy import Column, Integer, String

from storage.base import Base, engine
from sqlalchemy.orm import relationship


class Device(Base):
    """
    Represents the Pi Device
    """

    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sensors = relationship("Sensor", back_populates="device")

    def __repr__(self):
        return "<Device(id='%d', name='%s')>" % (self.id, self.name)


Base.metadata.create_all(engine)

