from typing import List, Optional

from lirpy.cuboid import Cuboid
from lirpy.mask3d import Mask3D
from lirpy.vector3 import Vector3


class _SzCuboid:
    def __init__(
        self, x: int, y: int, z: int, width: int, height: int, depth: int
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z
        self.width: int = width
        self.height: int = height
        self.depth: int = depth

    def asCuboid(self) -> Cuboid:
        return Cuboid(
            Vector3(self.x, self.y, self.z),
            Vector3(
                self.x + self.width - 1,
                self.y + self.height - 1,
                self.z + self.depth - 1,
            ),
        )

    @property
    def area(self) -> int:
        return self.height * self.width * self.depth


class Cubinator:
    def __init__(self, m: Mask3D) -> None:
        self.mask: Mask3D = m
        self.found: List[Cuboid] = []

    def findAll(self, verbose: bool = False) -> List[Cuboid]:
        o: List[Cuboid] = []
        step: int = 0
        if verbose:
            print(f"Step {step}:")
            self.mask.dump()
        while self.mask.has_true_areas_left():
            step += 1
            c = self.findBiggest()
            if c is not None:
                self.mask.maskOffFromCuboid(c)
                if verbose:
                    print(f"Step {step}:")
                    self.mask.dump()
                o.append(c)
        return o

    def findBiggest(self) -> Optional[Cuboid]:
        possible: List[_SzCuboid] = []
        for z in range(self.mask.depth):
            for y in range(self.mask.height):
                for x in range(self.mask.width):
                    if self.mask.get(x, y, z):
                        if (lb := self.getLargestBoxStartingAt(x, y, z)) is not None:
                            possible.append(lb)
                        else:
                            possible.append(_SzCuboid(x, y, z, 1, 1, 1))
        if len(possible) == 0:
            return None
        # random.shuffle(possible)
        possible.sort(key=lambda b: b.area, reverse=True)
        # print([a.area for a in possible])
        # print(f"possible[0].area={possible[0].area}")
        return possible[0].asCuboid()

    def isProposedBoxAcceptable(self, box: _SzCuboid) -> bool:
        for z in range(box.z, box.z + box.depth):
            for y in range(box.y, box.y + box.height):
                for x in range(box.x, box.x + box.width):
                    if not self.mask.get(x, y, z):
                        return False
        return True

    def getLargestBoxStartingAt(
        self, start_x: int, start_y: int, start_z: int
    ) -> Optional[_SzCuboid]:
        maxw = 1
        maxh = 1
        maxd = 1
        boxes: List[_SzCuboid] = []

        for z in range(start_z, self.mask.depth):
            if self.mask.get(start_x, start_y, z):
                maxd += 1
            else:
                break
        for y in range(start_y, self.mask.height):
            if self.mask.get(start_x, y, start_z):
                maxh += 1
            else:
                break
        for x in range(start_x, self.mask.width):
            if self.mask.get(x, start_y, start_z):
                maxw += 1
            else:
                break
        # print(maxh,maxw)
        for szz in range(maxd):
            for szy in range(maxh):
                for szx in range(maxw):
                    sr = _SzCuboid(start_x, start_y, start_z, szx, szy, szz)
                    if self.isProposedBoxAcceptable(sr):
                        boxes.append(sr)
        if len(boxes) == 0:
            return None
        boxes.sort(key=lambda b: b.area, reverse=True)
        return boxes[0]
