import datetime

import pandas as pd
import pytest
import pytz
from shapely.geometry import Point
from shapely.wkt import loads
from sqlalchemy import alias, func
from sqlalchemy.exc import StatementError

from .models import Trips


def test_simple_insert(session):
    session.add(
        Trips(
            car_id=1,
            trip_id=1,
            trip=pd.DataFrame(
                [
                    {
                        "geometry": Point(0, 0),
                        "t": datetime.datetime(2012, 1, 1, 8, 0, 0),
                    },
                    {
                        "geometry": Point(2, 0),
                        "t": datetime.datetime(2012, 1, 1, 8, 10, 0),
                    },
                    {
                        "geometry": Point(2, -1.98),
                        "t": datetime.datetime(2012, 1, 1, 8, 15, 0),
                    },
                ]
            ).set_index("t"),
        )
    )
    session.commit()

    sql = session.query(Trips).filter(Trips.trip_id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.car_id == 1
        assert result.trip_id == 1
        assert result.trip.size == 3
        assert result.trip.iloc[0].geometry == Point(0, 0)
        assert result.trip.iloc[1].geometry == Point(2, 0)
        assert result.trip.iloc[2].geometry == Point(2, -1.98)


def test_wkt_values_are_valid(session):
    with pytest.raises(StatementError):
        session.add(
            Trips(
                car_id=1,
                trip_id=1,
                trip=pd.DataFrame(
                    [
                        {
                            "geometry": "Point(-3.1 4.7770)",
                            "t": datetime.datetime(2012, 1, 1, 12, 0, 0),
                        },
                    ]
                ).set_index("t"),
            )
        )
        session.commit()


def test_str_values_are_invalid(session):
    with pytest.raises(StatementError):
        session.add(
            Trips(
                car_id=1,
                trip_id=1,
                trip=pd.DataFrame(
                    [
                        {"geometry": 0, "t": datetime.datetime(2012, 1, 1, 12, 0, 0)},
                        {"geometry": "8", "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},
                    ]
                ).set_index("t"),
            )
        )
        session.commit()


def test_float_values_are_invalid(session):
    with pytest.raises(StatementError):
        session.add(
            Trips(
                car_id=1,
                trip_id=1,
                trip=pd.DataFrame(
                    [{"geometry": 8.1, "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},]
                ).set_index("t"),
            )
        )
        session.commit()


def test_mobility_functions(session):
    session.add(
        Trips(
            car_id=10,
            trip_id=1,
            trip=pd.DataFrame(
                [
                    {
                        "geometry": Point(0, 0),
                        "t": datetime.datetime(2012, 1, 1, 8, 0, 0),
                    },
                    {
                        "geometry": Point(2, 0),
                        "t": datetime.datetime(2012, 1, 1, 8, 10, 0),
                    },
                    {
                        "geometry": Point(2, 1),
                        "t": datetime.datetime(2012, 1, 1, 8, 15, 0),
                    },
                ]
            ).set_index("t"),
        )
    )

    session.commit()

    session.add(
        Trips(
            car_id=20,
            trip_id=1,
            trip=pd.DataFrame(
                [
                    {
                        "geometry": Point(0, 0),
                        "t": datetime.datetime(2012, 1, 1, 8, 5, 0),
                    },
                    {
                        "geometry": Point(1, 1),
                        "t": datetime.datetime(2012, 1, 1, 8, 10, 0),
                    },
                    {
                        "geometry": Point(3, 3),
                        "t": datetime.datetime(2012, 1, 1, 8, 20, 0),
                    },
                ]
            ).set_index("t"),
        )
    )

    session.commit()

    # Value at a given timestamp
    trips = session.query(
        Trips.car_id,
        func.asText(
            func.valueAtTimestamp(Trips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0))
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert loads(trips[0][1]) == Point(2, 0)
    assert trips[1][0] == 20
    assert loads(trips[1][1]) == Point(1, 1)

    # Restriction to a given value
    trips = session.query(
        Trips.car_id, func.asText(func.atValue(Trips.trip, Point(2, 0).wkt)),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert trips[0][1] == r"{[POINT(2 0)@2012-01-01 08:10:00+00]}"
    assert trips[1][0] == 20
    assert trips[1][1] is None

    # Restriction to a period
    trips = session.query(
        Trips.car_id,
        func.asText(
            func.atPeriod(Trips.trip, "[2012-01-01 08:05:00,2012-01-01 08:10:00]")
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert (
        trips[0][1]
        == r"[POINT(1 0)@2012-01-01 08:05:00+00, POINT(2 0)@2012-01-01 08:10:00+00]"
    )
    assert trips[1][0] == 20
    assert (
        trips[1][1]
        == r"[POINT(0 0)@2012-01-01 08:05:00+00, POINT(1 1)@2012-01-01 08:10:00+00]"
    )

    # Temporal distance
    T1 = alias(Trips)
    T2 = alias(Trips)
    trips = (
        session.query(T1.c.car_id, T2.c.car_id, T1.c.trip.distance(T2.c.trip),)
        .filter(T1.c.car_id < T2.c.car_id,)
        .all()
    )

    assert len(trips) == 1
    assert trips[0][0] == 10
    assert trips[0][1] == 20
    assert trips[0][2].iloc[0].value == 1
    assert trips[0][2].iloc[0].name == datetime.datetime(
        2012, 1, 1, 8, 5, 0, tzinfo=pytz.utc
    )
    assert trips[0][2].iloc[1].value == 1.4142135623731
    assert trips[0][2].iloc[1].name == datetime.datetime(
        2012, 1, 1, 8, 10, 0, tzinfo=pytz.utc
    )
    assert trips[0][2].iloc[2].value == 1
    assert trips[0][2].iloc[2].name == datetime.datetime(
        2012, 1, 1, 8, 15, 0, tzinfo=pytz.utc
    )