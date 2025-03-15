from enum import Enum


class API(str, Enum):
    LIVENESS = "/liveness"
    READINESS = "/readness"
