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
