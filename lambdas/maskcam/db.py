"""
    Pothole Map
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
"""

import pytz
import psycopg2
from uuid import UUID
from datetime import datetime


def _utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)


DatabaseError = psycopg2.Error


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
        print(activity)
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO detections (
                id,
                device_name,
                created_on,
                recorded_on,
                min_confidence,
                people_in_frame,
                activity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(id),
                    device_name,
                    _utc_now(),
                    recorded_on,
                    min_confidence,
                    people_in_frame,
                    activity,
                )
            )
            self.connection.commit()

    def get_all_activities(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.id,
                       c.device_name,
                       d.device_serial,
                       d.created_on,
                       d.recorded_on,
                       d.min_confidence,
                       d.people_in_frame,
                       d.activity
                FROM detections AS d
                JOIN cameras AS c ON c.device_serial = d.device_serial
                WHERE is_confirmed = FALSE
                ORDER BY recorded_on;
                """
            )

            return [
                {
                    'id': a[0],
                    'device_name': a[1],
                    'created_on': a[2],
                    'recorded_on': a[3],
                    'min_confidence': a[4],
                    'people_in_frame': a[5],
                    'activity': a[6],
                }
                for a in cursor.fetchall()
            ]

    def confirm_activity(self, activity_id: UUID) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE detections
                SET is_confirmed = TRUE
                WHERE id = %s
                """,
                (
                    str(activity_id),
                )
            )
            self.connection.commit()
