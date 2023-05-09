from fastapi_utils.enums import StrEnum


class UnicodeAge(StrEnum):
    V1_1 = "1.1"
    V2_0 = "2.0"
    V2_1 = "2.1"
    V3_0 = "3.0"
    V3_1 = "3.1"
    V3_2 = "3.2"
    V4_0 = "4.0"
    V4_1 = "4.1"
    V5_0 = "5.0"
    V5_1 = "5.1"
    V5_2 = "5.2"
    V6_0 = "6.0"
    V6_1 = "6.1"
    V6_2 = "6.2"
    V6_3 = "6.3"
    V7_0 = "7.0"
    V8_0 = "8.0"
    V9_0 = "9.0"
    V10_0 = "10.0"
    V11_0 = "11.0"
    V12_0 = "12.0"
    V12_1 = "12.1"
    V13_0 = "13.0"
    V14_0 = "14.0"
    V15_0 = "15.0"

    def __str__(self) -> str:
        return self.name.replace("_", ".")[1:]

    @property
    def code(self) -> str:
        return str(self)

    @classmethod
    def match_loosely(cls, age: str):
        age_map = {f"{e}": e for e in cls}
        return age_map.get(age)
