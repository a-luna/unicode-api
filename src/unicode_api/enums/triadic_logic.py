from enum import IntEnum


class TriadicLogic(IntEnum):
    Y = 1
    N = 0
    M = -1

    def __str__(self):
        name_map = {
            "Y": "Yes",
            "N": "No",
            "M": "Maybe",
        }
        return name_map.get(self.name, "")

    @classmethod
    def from_code(cls, code: str) -> "TriadicLogic":  # pragma: no cover
        code_map = {
            "Y": cls.Y,
            "N": cls.N,
            "M": cls.M,
        }
        return code_map.get(code, cls.N)
