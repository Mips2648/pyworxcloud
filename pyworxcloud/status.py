"""Status and error codes."""
from __future__ import annotations
from enum import IntEnum


class WorxStatus(IntEnum):
    STOPPED = 0
    HOME = 1
    START_SEQUENCE = 2
    LEAVING_HOME = 3
    GOING_HOME = 5
    SEARCHING_FOR_BORDER = 6
    CUTTING_GRASS = 7
    LIFTED_RECOVERY = 8
    TRAPPED_RECOVERY = 9
    BLADE_BLOCKED = 10
    OUTSIDE_FENCE = 13
    FOLLOW_BORDER_HOME = 30
    FOLLOW_BORDER_TRAINING = 31
    FOLLOW_BORDER_CUTTING = 32
    FOLLOW_BORDER_GOING_TO_ZONE = 33
    PAUSE = 34


class WorxError(IntEnum):
    NO_ERROR = 0
    TRAPPED = 1
    LIFTED = 2
    WIRE_MISSING = 3
    OUTSIDE_BOUNDARY = 4
    RAINING = 5
    CLOSE_DOOR_TO_CUT = 6
    CLOSE_DOOR_TO_GO_HOME = 7
    BLADE_MOTOR_ERROR = 8
    WHEEL_MOTOR_ERROR = 9
    TRAPPED_TIMEOUT = 10
    UPSIDE_DOWN = 11
    BATTERY_LOW = 12
    BOUNDARY_WIRE_REVERSED = 13
    BATTERY_CHARGE_ERRPR = 14
    HOME_SEARCH_TIMEOUT = 15
    WIFI_LOCKED = 16
    BATTERY_TEMPERETURE = 17
    DOOR_OPEN_TIMEOUT = 19
    BOUNDARY_WIRE_OUT_OF_SYNC = 20
