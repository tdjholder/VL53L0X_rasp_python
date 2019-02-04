
import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float

from storage.base import Base, engine
from sqlalchemy.orm import relationship


class Measurement(Base):
    """Represents a measurement taken by a sensor."""

    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    distance = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    sensor_id = Column(Integer, ForeignKey('sensor.id'), nullable=False)
    sensor = relationship("Sensor", back_populates="measurements")

    def __repr__(self):
        return "<Measurement(id='%d', distance='%d', time='%s')>" % (self.id, self.distance, self.created_date)


Base.metadata.create_all(engine)

