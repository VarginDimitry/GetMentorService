import enum


class GenderEnum(enum.Enum):
    MALE = 'M'
    FEMALE = 'F'

    def __missing__(self, key):
        return GenderEnum.MALE


class TimeTypeEnum(enum.Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


class TokenType(enum.IntEnum):
    ACCESS = 0
    REFRESH = 1


class ErrorEnum(enum.IntEnum):
    SUCCESS = 200

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    UNKNOWN = 499

    @classmethod
    def _missing_(cls, value):
        return ErrorEnum.UNKNOWN
