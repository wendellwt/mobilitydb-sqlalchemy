from sqlalchemy import (
    Column,
    DateTime,
    String,
    Integer,
    func,
)
from sqlalchemy.ext.declarative import declarative_base


from mobilitydb_sqlalchemy import TBool, TGeomPoint, TGeogPoint, TFloat, TInt

Base = declarative_base()


class TemporalBools(Base):
    __tablename__ = "tbool_test_001"
    id = Column(Integer, primary_key=True)
    tdata = Column(TBool)


class TemporalFloats(Base):
    __tablename__ = "tfloat_test_002"
    id = Column(Integer, primary_key=True)
    tdata = Column(TFloat(True, False))


class TemporalInts(Base):
    __tablename__ = "tint_test_003"
    id = Column(Integer, primary_key=True)
    tdata = Column(TInt)


class Trips(Base):
    __tablename__ = "trips_test_004"
    car_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, primary_key=True)
    trip = Column(TGeomPoint)


class TripsWithMovingPandas(Base):
    __tablename__ = "trips_mp_test_005"
    car_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, primary_key=True)
    trip = Column(TGeomPoint(use_movingpandas=True))


class GeogTrips(Base):
    __tablename__ = "trips_geog_test_006"
    car_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, primary_key=True)
    trip = Column(TGeogPoint)


class GeogTripsWithMovingPandas(Base):
    __tablename__ = "trips_geog_test_007"
    car_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, primary_key=True)
    trip = Column(TGeogPoint(use_movingpandas=True))
