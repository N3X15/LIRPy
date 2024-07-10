from typing import Callable, List, Tuple
from lirpy.cuboid import Cuboid
from lirpy.mask2d import Mask2D
from lirpy.vector3 import Vector3

__all__ = ["Mask3D"]


class Mask3D:
    def __init__(self, width: int, height: int, depth: int) -> None:
        self.width: int = width
        self.height: int = height
        self.depth: int = depth
        self.data: List[bool] = [False] * (self.height * self.width * self.depth)

    def xyz2idx(self, x: int, y: int, z: int) -> int:
        return x + (y * self.width) + (z * self.height * self.width)

    def idx2xyz(self, i: int) -> Tuple[int, int, int]:
        z, xy = divmod(i, self.height * self.depth)
        y, x = divmod(xy, self.height)
        return x, y, z

    def has_true_areas_left(self) -> bool:
        return any(self.data)

    def set(self, x: int, y: int, z: int, value: bool) -> None:
        while len(self.data) < (self.width * self.height * self.depth):
            self.data.append(False)
        self.data[self.xyz2idx(x, y, z)] = value

    def get(self, x: int, y: int, z: int) -> bool:
        return self.data[self.xyz2idx(x, y, z)]

    def setif(self, c: Callable[[int, int, int, bool], bool]) -> None:
        while len(self.data) < (self.width * self.height * self.depth):
            self.data.append(False)
        for i in range(len(self.data)):
            x, y, z = self.idx2xyz(i)
            self.data[i] = c(x, y, z, self.data[i])

    def flip(
        self, flip_x: bool = False, flip_y: bool = False, flip_z: bool = False
    ) -> None:
        data = self.data.copy()
        for _z in range(self.depth):
            z = (self.depth - _z - 1) if flip_z else _z
            # print(z)
            for _y in range(self.height):
                y = (self.height - _y - 1) if flip_y else _y
                for _x in range(self.width):
                    x = (self.width - _x - 1) if flip_x else _x
                    # print(f'{_x},{_y},{_z} -> {x},{y},{z}')
                    self.data[self.xyz2idx(x, y, z)] = data[self.xyz2idx(_x, _y, _z)]

    def append2D(self, m: Mask2D) -> None:
        assert self.width == m.width
        assert self.height == m.height
        self.depth += 1
        for z in range(self.depth):
            for x in range(m.width):
                self.set(x, self.depth - 1, z, m.get(x, y))

    def dump(self) -> None:
        # from rich import console
        for y in range(self.height):
            print(f"{y=}")
            for z in range(self.depth):
                for x in range(self.width):
                    print("█" if self.get(x, y, z) else " ", end="")
                print()

    def maskOffFromCuboid(self, cuboid: Cuboid) -> None:
        for y in range(self.height):
            for z in range(self.depth):
                for x in range(self.width):
                    if (
                        cuboid.min.x <= x <= cuboid.max.x
                        and cuboid.min.y <= y <= cuboid.max.y
                        and cuboid.min.z <= z <= cuboid.max.z
                    ):
                        self.data[self.xyz2idx(x, y, z)] = False
