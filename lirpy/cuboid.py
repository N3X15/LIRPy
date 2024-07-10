from typing import NamedTuple
from lirpy.vector3 import Vector3


class Cuboid(NamedTuple):
    min: Vector3
    max: Vector3

    def normalize(self) -> "Cuboid":
        return Cuboid(
            Vector3(
                min(self.min.x, self.max.x),
                min(self.min.y, self.max.y),
                min(self.min.z, self.max.z),
            ),
            Vector3(
                max(self.min.x, self.max.x),
                max(self.min.y, self.max.y),
                max(self.min.z, self.max.z),
            ),
        )

    @property
    def width(self) -> int:
        return self.max.x - self.min.x

    @property
    def height(self) -> int:
        return self.max.y - self.min.y

    @property
    def depth(self) -> int:
        return self.max.z - self.min.z
