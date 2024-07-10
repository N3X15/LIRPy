from pathlib import Path
from typing import List, Tuple

from lirpy.mask3d import Mask3D
from lirpy.vector3 import Vector3

# This is the shittiest possible way of filling this niche I am so sorry
# I basically wanted to make a way to describe how to mine out an area 
# but in a way that was human-editable
# Behold, the result:
class LPReader:
    def __init__(self, file: Path) -> None:
        self.path: Path = file
        self._pos: Vector3 = Vector3(0, 0, 0)
        self._size: Vector3 = Vector3(0, 0, 0)
        self._origin: Vector3 = Vector3(0, 0, 0)

        self._setting_size_x:bool=True
        self._setting_size_y:bool=True
        self._setting_size_z:bool=True

        self.mdata: List[Tuple[int,int,int,bool]] = []

    def read(self) -> None:
        with self.path.open("r") as f:
            self._size.y =1
            for l in f:
                if l.strip('\r\n') == "": continue
                if l.strip() == "-":
                    self._pos.x = 0
                    self._pos.z = 0
                    self._pos.y += 1
                    self._size.y += 1
                    self._setting_size_z=False
                else:
                    self._readline(l)
            self._pos.x = 0
            self._pos.z = 0
            self._pos.y += 1
            # self._size.y += 1

    def asMask3D(self) -> Mask3D:
        m = Mask3D(self._size.x, self._size.y, self._size.z)
        print(f"Size: {self._size.x}w x {self._size.y}h x {self._size.z}d")
        for x,y,z,v in self.mdata:
            # print(x,y,z,v)
            m.set(x,y,z,v)
        m.dump()
        m.flip(flip_y=True)
        m.dump()
        return m

    def _readline(self, l: str) -> None:
        sz=0
        for c in l:
            if self._pos.x >= self._size.x:
                self._size.x = self._pos.x
            match c:
                case "\r" | "\n" | "\t":
                    continue
                case "O":
                    self._origin = Vector3(self._pos.x, self._pos.y, self._pos.z)
                    sz+=1
                    v = True
                case "X":
                    sz += 1
                    v = True
                case " ":
                    sz += 1
                    v = False
            self.mdata.append((self._pos.x,self._pos.y,self._pos.z,v))
            self._pos.x += 1
        if self._setting_size_x:
            self._size.x=sz
            self._setting_size_x=False
        # print(f'{self._size.x=}')
        self._pos.x = 0
        self._pos.z += 1
        if self._setting_size_z:
            self._size.z+=1
