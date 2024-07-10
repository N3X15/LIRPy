import argparse
import json
from pathlib import Path
import random
from typing import Callable, Dict, Dict, List, Tuple

from lirpy.cubinator import Cubinator
from lirpy.cuboid import Cuboid
from lirpy.lp_reader import LPReader
from lirpy.mask2d import Mask2D
from lirpy.mask3d import Mask3D
from lirpy.point import Point, dist_points
from lirpy.rect import Rect
from lirpy.rectangulator import Rectangulator

RECT = Tuple[int, int, int, int]
CUBOID = Tuple[int, int, int, int, int, int]
VECTOR3 = Tuple[int, int, int]

dirchoices = []
for axis in "XYZ":
    for plusmin in "+-":
        dirchoices.append(f"{plusmin}{axis}")


def main() -> None:
    argp = argparse.ArgumentParser()
    subp = argp.add_subparsers()
    _register_cylinder(subp)
    _register_file(subp)
    args = argp.parse_args()
    if not hasattr(args, "cmd"):
        argp.print_help()
    else:
        args.cmd(args)


def _register_file(subp: argparse._SubParsersAction) -> None:
    p = subp.add_parser("file", aliases=["file", "f"])
    p.add_argument("x", type=int)
    p.add_argument("y", type=int)
    p.add_argument("z", type=int)
    p.add_argument("--file", type=Path, default=1)
    p.add_argument("--axis", choices=dirchoices, default="-Y")
    p.add_argument("--dump-steps", action="store_true", default=False)
    p.set_defaults(cmd=_cmd_file)

X_WEST=-1
X_EAST=1
Z_NORTH=-1
Z_SOUTH=1
Y_UP=1
Y_DOWN=-1
def _cmd_file(args: argparse.Namespace) -> None:
    filename: Path = args.file
    dump_steps: bool = args.dump_steps
    x:int=args.x
    y:int=args.y
    z:int=args.z
    assert filename.is_file(), f"--file={filename} does not exist"

    rdr=LPReader(filename)
    rdr.read()
    mask=rdr.asMask3D()
    print("/*")
    print(f"Size:   {mask.width=} {mask.height=} {mask.depth=}")
    print(f"Origin: {rdr._origin.x} {rdr._origin.y} {rdr._origin.z}")
    print(f"Offset: {x} {y} {z}")
    print(f"Along axis: {args.axis}")
    print("*/")
    x: int = args.x
    y: int = args.y
    z: int = args.z

    oox: int
    ooy: int
    ooz: int
    oox, ooy, ooz = rdr._origin.x, rdr._origin.y, rdr._origin.z

    cuboids = []
    # for yo, m in masks.items():

    #     def cuboid_from_rect(rect: RECT) -> Tuple[VECTOR3, VECTOR3]:
    #         print(yo)
    #         minx, minz, maxx, maxz = rect
    #         p1 = (x - oox + minx, y - ooy + yo, z - ooz - minz)
    #         p2 = (x - oox + maxx, y - ooy + yo, z - ooz - maxz)
    #         return p1, p2

    #     cuboids += get_rects_from_mask(
    #         m, dump_steps=dump_steps, cuboid_from_rect=cuboid_from_rect
    #     )
    def cuboid_from_t6(t6: CUBOID) -> Tuple[VECTOR3, VECTOR3]:
        minx, miny, minz, maxx, maxy, maxz = t6
        # miny, minz = minz, miny
        # maxy, maxz = maxz, maxy
        # case "-Y":
        #     p1 = (minx - r + x, y, miny - r + z)
        #     p2 = (maxx - r + x, y - d, maxy - r + z)
        # MC:
        # MC:
        # right positive x
        # south positive z
        p1 = (minx - oox + x, miny - ooy + y, minz - ooz + z)
        p2 = (maxx - oox + x, maxy - ooy + y, maxz - ooz + z)
        return p1, p2

    cuboids = get_cuboids_from_mask(
        mask, dump_steps=dump_steps, cuboid_from_cuboid=cuboid_from_t6
    )

    print_baritone_selections(cuboids)


def _register_cylinder(subp: argparse._SubParsersAction) -> None:
    p:argparse.ArgumentParser = subp.add_parser("cylinder", aliases=["cylinder", "c"])

    pe = p.add_argument_group('Origin', description="Describe an ellipsoid cross-section")
    pe.add_argument("x", type=int)
    pe.add_argument("y", type=int)
    pe.add_argument("z", type=int)
    
    pe = p.add_argument_group('Ellipsoid', description="Describe an ellipsoid cross-section")
    pe.add_argument("--semi-axis-a", "-a", type=int, help="Length of semi-axis A")
    pe.add_argument("--semi-axis-b", "-b", type=int, help="Length of semi-axis B")

    pe = p.add_argument_group('Circular', description="Describe a circular cross-section by radius")
    pe.add_argument("--radius", "-r", type=int)

    p.add_argument("--depth", "-d", type=int, default=1)
    p.add_argument("--axis", choices=dirchoices, default="-Y")
    p.add_argument("--dump-steps", action="store_true", default=False)
    p.set_defaults(cmd=_cmd_cylinder)


def _cmd_cylinder(args: argparse.Namespace) -> None:
    x: int = args.x
    y: int = args.y
    z: int = args.z
    a: int = args.semi_axis_a
    b: int = args.semi_axis_b
    d: int = args.depth - 1
    assert d >= 0
    c = Point(x=a / 2, y=b / 2)
    print(f"Center: {x} {y} {z}")
    print(f"Semi-Axes:")
    print(f"  a: {a}")
    print(f"  b: {b}")
    print(f"Depth: {d}")
    print(f"Along axis: {args.axis}")
    m = Mask2D(height=b, width=a)

    def setmasktoellipse(x: int, y: int, v: bool) -> bool:
        return ((x - c.x) / a) ** 2 + ((y - c.y) / b) <= 1

    m.setif(setmasktoellipse)
    do_rectangulate(
        x,
        y,
        z,
        d,
        m,
        xo=-(a / 2),
        yo=-(b / 2),
        args=args,
    )


def do_rectangulate(
    x: int, y: int, z: int, d: int, m: Mask2D, xo: int, yo: int, args: argparse.Namespace
) -> None:
    dump_steps: bool = args.dump_steps
    assert d >= 0
    c = Point(x=r, y=r)
    print(f"Center: {x} {y} {z}")
    print(f"Radius: {r}")
    print(f"Depth: {d}")
    print(f"Along axis: {args.axis}")
    m = Mask2D(height=r * 2 + 1, width=r * 2 + 1)
    m.setif(lambda x, y, v: dist_points(Point(x, y), c) <= r)

    def cuboid_from_rect(rect: RECT) -> Tuple[VECTOR3, VECTOR3]:
        minx, miny, maxx, maxy = rect
        p1 = (0, 0, 0)
        p2 = (0, 0, 0)
        match args.axis:
            case "+X":
                p1 = (x, minx + xo + y, miny + yo + z)
                p2 = (x + d, maxx + xo + y, maxy + yo + z)
            case "-X":
                p1 = (x, minx + xo + y, miny + yo + z)
                p2 = (x - d, maxx + xo + y, maxy + yo + z)
            case "+Y":
                p1 = (minx + xo + x, y, miny + yo + z)
                p2 = (maxx + xo + x, y + d, maxy + yo + z)
            case "-Y":
                p1 = (minx + xo + x, y, miny + yo + z)
                p2 = (maxx + xo + x, y - d, maxy + yo + z)
            case "+Z":
                p1 = (minx + xo + x, miny + yo + y, z)
                p2 = (maxx + xo + x, maxy + yo + y, z + d)
            case "-Z":
                p1 = (minx - r + x, miny - r + y, z)
                p2 = (maxx - r + x, maxy - r + y, z - d)
        return p1, p2

    cuboids = get_rects_from_mask(
        m, dump_steps=dump_steps, cuboid_from_rect=cuboid_from_rect
    )
    print_baritone_selections(cuboids)


def get_rects_from_mask(
    m: Mask2D,
    dump_steps: bool = False,
    cuboid_from_rect: Callable[[RECT], Tuple[VECTOR3, VECTOR3]] = None,
) -> List[Tuple[VECTOR3, VECTOR3]]:
    rt = Rectangulator(m)
    rect: Rect
    written = set()
    cuboids: List[Tuple[VECTOR3, VECTOR3]] = []
    for rect in rt.findAll(verbose=dump_steps):
        minx = rect.min.x
        miny = rect.min.y
        maxx = rect.max.x
        maxy = rect.max.y
        k = (minx, miny, maxx, maxy)
        if k in written:
            continue
        written.add(k)
        p1, p2 = cuboid_from_rect(k)
        cuboids.append((p1, p2))
    return cuboids


def get_cuboids_from_mask(
    m: Mask3D,
    dump_steps: bool = False,
    cuboid_from_cuboid: Callable[[CUBOID], Tuple[VECTOR3, VECTOR3]] = None,
) -> List[Tuple[VECTOR3, VECTOR3]]:
    rt = Cubinator(m)
    cuboid: Cuboid
    written = set()
    cuboids: List[Tuple[VECTOR3, VECTOR3]] = []
    for cuboid in rt.findAll(verbose=dump_steps):
        minx = cuboid.min.x
        miny = cuboid.min.y
        minz = cuboid.min.z
        maxx = cuboid.max.x
        maxy = cuboid.max.y
        maxz = cuboid.max.z
        k = (minx, miny, minz, maxx, maxy, maxz)
        if k in written:
            continue
        written.add(k)
        p1, p2 = cuboid_from_cuboid(k)
        cuboids.append((p1, p2))
    return cuboids


def output_baritone_selections(cuboids: List[Tuple[VECTOR3, VECTOR3]]) -> List[str]:
    output: List[str] = []
    output.append("#sel clear")
    for p1, p2 in cuboids:
        p1 = " ".join(list(map(str, p1)))
        p2 = " ".join(list(map(str, p2)))
        output.append(f"#sel 1 {p1}")
        output.append(f"#sel 2 {p2}")
    return output


def print_baritone_selections(cuboids: List[Tuple[VECTOR3, VECTOR3]]) -> List[str]:
    for l in output_baritone_selections(cuboids):
        print(f"Chat.say({json.dumps(l)});")


if __name__ == "__main__":
    main()
