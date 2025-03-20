from enum import IntEnum, auto


class RequestType(IntEnum):
    NONE = auto()
    RATE_LIMITED_ALLOWED = auto()
    RATE_LIMITED_DENIED = auto()
    STATIC_RESOURCE = auto()
    INTERNAL_REQUEST = auto()
    TEST_REQUEST = auto()
    ERROR = auto()
