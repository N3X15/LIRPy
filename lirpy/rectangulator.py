from typing import List, Optional

from lirpy.mask2d import Mask2D
from lirpy.rect import Rect


class _SzRect:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def asRect(self) -> Rect:
        return Rect(
            xmin=self.x,
            ymin=self.y,
            xmax=self.x + self.width - 1,
            ymax=self.y + self.height - 1,
        )

    @property
    def area(self) -> int:
        return self.height * self.width


class Rectangulator:
    def __init__(self, m: Mask2D) -> None:
        self.mask: Mask2D = m
        self.found: List[Rect] = []

    def findAll(self, verbose: bool = False) -> List[Rect]:
        o: List[Rect] = []
        step:int=0
        if verbose:
            print(f'Step {step}:')
            self.mask.dump()
        while self.mask.has_true_areas_left():
            step+=1
            r = self.findBiggest()
            if r is not None:
                self.mask.maskOffFromRect(r)
                if verbose:
                    print(f'Step {step}:')
                    self.mask.dump()
                o.append(r)
        return o

    def findBiggest(self) -> Optional[Rect]:
        possible: List[_SzRect] = []
        for y in range(self.mask.height):
            for x in range(self.mask.width):
                if self.mask.get(x, y):
                    if (lb := self.getLargestBoxStartingAt(x, y)) is not None:
                        possible.append(lb)
                    else:
                        possible.append(_SzRect(x, y, 1, 1))
        if len(possible) == 0:
            return None
        # random.shuffle(possible)
        possible.sort(key=lambda b: b.area, reverse=True)
        # print([a.area for a in possible])
        # print(f"possible[0].area={possible[0].area}")
        return possible[0].asRect()

    def isProposedBoxAcceptable(self, box: _SzRect) -> bool:
        for y in range(box.y, box.y + box.height):
            for x in range(box.x, box.x + box.width):
                if not self.mask.get(x, y):
                    return False
        return True

    def getLargestBoxStartingAt(self, start_x: int, start_y: int) -> Optional[_SzRect]:
        maxw = 1
        maxh = 1
        boxes: List[_SzRect] = []

        for y in range(start_y, self.mask.height):
            if self.mask.get(start_x, y):
                maxh += 1
            else:
                break
        for x in range(start_x, self.mask.width):
            if self.mask.get(x, start_y):
                maxw += 1
            else:
                break
        # print(maxh,maxw)
        for szy in range(maxh):
            for szx in range(maxw):
                sr = _SzRect(start_x, start_y, szx, szy)
                if self.isProposedBoxAcceptable(sr):
                    boxes.append(sr)
        if len(boxes) == 0:
            return None
        boxes.sort(key=lambda b: b.area, reverse=True)
        return boxes[0]
