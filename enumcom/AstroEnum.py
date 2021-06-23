from enum import Enum, unique

@unique
class ConstellationEnum(Enum):
    def __new__(cls, chinese, num):
        obj = object.__new__(cls)
        obj.chinese = chinese
        obj.num = num
        return obj

    Aries = '白羊座', 1
    Taurus = '金牛座', 2
    Gemini = '双子座', 3
    Cancer = '巨蟹座', 4
    leo = '狮子座', 5
    Virgo = '处女座', 6
    Libra = '天秤座', 7
    Scorpio = '天蝎座', 8
    Sagittarius = '射手座', 9
    Capricorn = '魔羯座', 10
    Aquarius = '水瓶座', 11
    Pisces = '双鱼座', 12
