from enum import Enum, unique


@unique
class GenderEnum(Enum):
    def __new__(cls, chinese, num):
        obj = object.__new__(cls)
        obj.chinese = chinese
        obj.num = num
        return obj

    MALE = "男", 1
    FEMALE = "女", 2