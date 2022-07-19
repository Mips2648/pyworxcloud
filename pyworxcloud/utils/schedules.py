"""Defines schedule classes."""
from __future__ import annotations

import calendar
from datetime import datetime, timedelta
from enum import IntEnum

from ..day_map import DAY_MAP
from .landroid_class import LDict


class ScheduleType(IntEnum):
    """Schedule types."""

    PRIMARY = 0
    SECONDARY = 1


TYPE_TO_STRING = {ScheduleType.PRIMARY: "primary", ScheduleType.SECONDARY: "secondary"}


class WeekdaySettings(LDict):
    """Class representing a weekday setting."""

    def __init__(
        self,
        start: str = "00:00",
        end: str = "00:00",
        duration: int = 0,
        boundary: bool = False,
    ) -> None:
        """Initialize the settings."""
        super().__init__()
        self["start"] = start
        self["end"] = end
        self["duration"] = duration
        self["boundary"] = boundary


class Weekdays(LDict):
    """Represents all weekdays."""

    def __init__(self) -> dict:
        super().__init__()

        for day in list(calendar.day_name):
            self.update({day.lower(): WeekdaySettings()})


class ScheduleInfo:
    """Used for calculate the current schedule progress and show next schedule start."""

    def __init__(self, schedule: Schedule) -> None:
        """Initialize the ScheduleInfo object and set values."""
        self.__schedule = schedule
        self.__now = datetime.now()
        self.__today = datetime.now().strftime("%d/%m/%Y")

    def _get_schedules(
        self, date: datetime, next: bool = False, add_offset: bool = False
    ) -> WeekdaySettings | None:
        """Get primary and secondary schedule for today or tomorrow."""
        day = DAY_MAP[int(date.strftime("%w"))]

        primary = self.__schedule[TYPE_TO_STRING[ScheduleType.PRIMARY]][day]
        if primary["duration"] == 0:
            primary = None

        secondary = self.__schedule[TYPE_TO_STRING[ScheduleType.SECONDARY]][day]

        if primary["duration"] == 0:
            secondary = None

        return primary, secondary, date

    def calculate_progress(self) -> int:
        """Calculate and return current progress in percent."""
        primary, secondary, date = self._get_schedules(self.__now)

        start = datetime.strptime(
            f"{self.__today} {primary['start']}", "%d/%m/%Y %H:%M"
        )
        end = datetime.strptime(f"{self.__today} {primary['end']}", "%d/%m/%Y %H:%M")

        total_run = primary["duration"]
        has_run = 0

        if self.__now >= start and self.__now < end:
            has_run = (self.__now - start).total_seconds() / 60
        elif self.__now < start:
            has_run = 0
        else:
            has_run = primary["duration"]

        if (not isinstance(secondary, type(None))) and secondary["duration"] > 0:
            start = datetime.strptime(
                f"{self.__today} {secondary['start']}", "%d/%m/%Y %H:%M"
            )
            end = datetime.strptime(
                f"{self.__today} {secondary['end']}", "%d/%m/%Y %H:%M"
            )
            total_run += secondary["duration"]
            if self.__now >= start and self.__now < end:
                has_run += (self.__now - start).total_seconds() / 60
            elif self.__now < start:
                has_run += 0
            else:
                has_run += primary["duration"]

        pct = (has_run / total_run) * 100
        return int(round(pct))

    def next_schedule(self) -> datetime:
        """Find next schedule starting point."""
        primary, secondary, date = self._get_schedules(self.__now)
        next = None
        cnt = 0
        while isinstance(primary, type(None)):
            if cnt == 7:
                # No schedule active for any weekday, return None
                return None

            primary, secondary, date = self._get_schedules(date + timedelta(days=1))
            cnt += 1

        start = datetime.strptime(
            f"{date.strftime('%d/%m/%Y')} {primary['start']}", "%d/%m/%Y %H:%M"
        )

        if self.__now < start:
            next = start
        elif (
            (not isinstance(secondary, type(None)))
            and start
            < datetime.strptime(
                f"{date.strftime('%d/%m/%Y')} {secondary['start']}", "%d/%m/%Y %H:%M"
            )
            and secondary["duration"] > 0
        ):
            next = datetime.strptime(
                f"{date.strftime('%d/%m/%Y')} {secondary['start']}", "%d/%m/%Y %H:%M"
            )

        if isinstance(next, type(None)):
            primary, secondary, date = self._get_schedules(date + timedelta(days=1))
            while isinstance(primary, type(None)):
                primary, secondary, date = self._get_schedules(date + timedelta(days=1))
            next = datetime.strptime(
                f"{date.strftime('%d/%m/%Y')} {primary['start']}", "%d/%m/%Y %H:%M"
            )

        return next


class Schedule(LDict):
    """Represents a schedule."""

    def __init__(
        self,
        variation: int = 0,
        active: bool = True,
        auto_schedule_settings: dict = {},
        auto_schedule_enabled: bool | None = None,
    ) -> dict:
        """Initialize an empty primary or secondary schedule.

        Args:
            schedule_type (ScheduleType): Which ScheduleType to initialize.
        """
        super().__init__()

        self["daily_progress"] = None
        self["next_schedule_start"] = None
        self["time_extension"] = variation
        self["active"] = active
        self["auto_schedule"] = {
            "settings": auto_schedule_settings,
            "enabled": auto_schedule_enabled,
        }

    def update_progress_and_next(self) -> None:
        """Update progress and next scheduled start properties."""

        info = ScheduleInfo(self)
        self["daily_progress"] = info.calculate_progress()
        self["next_schedule_start"] = info.next_schedule()
