import enum


class GenderEnum(enum.Enum):
    MALE = 'M'
    FEMALE = 'F'


class TimeTypeEnum(enum.Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
