"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import pytz
import psycopg2
import geohash2

from typing import (
    Callable,
    List,
    Optional,
    Tuple,
)

from uuid import UUID
from datetime import datetime


def _utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


DatabaseError = psycopg2.Error


class Pothole:
    id: Optional[str]
    device_name: str
    timestamp: datetime
    confidence: float
    coordinates: Tuple[float, float]
    photo_url: Optional[str]

    def __init__(self, id: Optional[str], device_name: str, timestamp: datetime,
                 confidence: float, coordinates: Tuple[float, float], photo_url: Optional[str]):
        self.id = id
        self.device_name = device_name
        self.timestamp = timestamp
        self.confidence = confidence
        self.coordinates = coordinates
        self.photo_url = photo_url


class Repo:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
        )

    def insert_record(self, id: UUID, device_name: str, recorded_on: datetime, min_confidence: float,
                      people_in_frame: int, activity: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO maskcam (
                id,
                device_name,
                created_on,
                recorded_on,
                min_confidence,
                people_in_frame,
                override
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                {
                    str(id),
                    device_name,
                    _utc_now(),
                    recorded_on,
                    min_confidence,
                    people_in_frame,
                    activity

                }
            )
            self.connection.commit()

    def get_items_for_device(self, device_name: str, min_time: datetime):
        raise NotImplementedError

    def get_all_item(self, min_time: datetime):
        raise NotImplementedError
