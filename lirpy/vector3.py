from typing import NamedTuple


class Vector3:

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        z: int = 0,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z
