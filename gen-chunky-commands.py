import argparse
import json

from lirpy.vector3 import Vector3


def main() -> None:
    argp = argparse.ArgumentParser()
    argp.add_argument("world", type=str, default="world")
    spawnloc = argp.add_argument_group("spawn location")
    spawnloc.add_argument("spawn_x", type=int)
    spawnloc.add_argument("spawn_y", type=int)
    spawnloc.add_argument("spawn_z", type=int)

    subp = argp.add_subparsers()
    _register_circle(subp)
    _register_diamond(subp)
    _register_hexagon(subp)
    _register_pentagon(subp)
    _register_square(subp)
    _register_star(subp)
    _register_triangle(subp)

    args = argp.parse_args()

    if not hasattr(args, "cmd"):
        argp.print_help()
    else:
        args.cmd(args)


def chatsay(s: str) -> None:
    s = f"/{s}"
    print(f"Chat.say({json.dumps(s)});")


def _args2center(args: argparse.Namespace) -> Vector3:
    return Vector3(args.spawn_x, args.spawn_y, args.spawn_z)


def handle_radius_shape(shape: str, args: argparse.Namespace) -> None:
    center = _args2center(args)
    full_world = args.world
    simple_world = full_world.split(":", 1)[1]
    chatsay(f"bluemap freeze {simple_world}")
    chatsay(f"bluemap purge {simple_world}")
    chatsay(f"chunky border remove {simple_world}")
    chatsay(f"chunky cancel")
    chatsay(f"chunky confirm")
    chatsay(f"chunky world {full_world}")
    chatsay(f"chunky shape {shape}")
    chatsay(f"chunky center {center.x} {center.z}")
    chatsay(f"chunky radius {args.radius}")
    chatsay(f"chunky border add {simple_world}")
    chatsay(f"chunky start")
    # chatsay(f"bluemap start {args.world}")


def _register_square(subp: argparse._SubParsersAction) -> None:
    squareargs: argparse.ArgumentParser = subp.add_parser("square")
    squareargs.add_argument("--radius", "-r", type=int, required=True)
    squareargs.set_defaults(cmd=_cmd_square)


def _cmd_square(args: argparse.Namespace) -> None:
    handle_radius_shape("square", args)


def _register_circle(subp: argparse._SubParsersAction) -> None:
    circleargs: argparse.ArgumentParser = subp.add_parser("circle")
    circleargs.add_argument("--radius", "-r", type=int, required=True)
    circleargs.set_defaults(cmd=_cmd_circle)


def _cmd_circle(args: argparse.Namespace) -> None:
    handle_radius_shape("circle", args)


def _register_triangle(subp: argparse._SubParsersAction) -> None:
    triangleargs: argparse.ArgumentParser = subp.add_parser("triangle")
    triangleargs.add_argument("--radius", "-r", type=int, required=True)
    triangleargs.set_defaults(cmd=_cmd_triangle)


def _cmd_triangle(args: argparse.Namespace) -> None:
    handle_radius_shape("triangle", args)


def _register_diamond(subp: argparse._SubParsersAction) -> None:
    diamond: argparse.ArgumentParser = subp.add_parser("diamond")
    diamond.add_argument("--radius", "-r", type=int, required=True)
    diamond.set_defaults(cmd=_cmd_diamond)


def _cmd_diamond(args: argparse.Namespace) -> None:
    handle_radius_shape("diamond", args)


def _register_pentagon(subp: argparse._SubParsersAction) -> None:
    pentagon: argparse.ArgumentParser = subp.add_parser("pentagon")
    pentagon.add_argument("--radius", "-r", type=int, required=True)
    pentagon.set_defaults(cmd=_cmd_pentagon)


def _cmd_pentagon(args: argparse.Namespace) -> None:
    handle_radius_shape("pentagon", args)


def _register_hexagon(subp: argparse._SubParsersAction) -> None:
    hexagon: argparse.ArgumentParser = subp.add_parser("hexagon")
    hexagon.add_argument("--radius", "-r", type=int, required=True)
    hexagon.set_defaults(cmd=_cmd_hexagon)


def _cmd_hexagon(args: argparse.Namespace) -> None:
    handle_radius_shape("hexagon", args)


def _register_star(subp: argparse._SubParsersAction) -> None:
    star: argparse.ArgumentParser = subp.add_parser("star")
    star.add_argument("--radius", "-r", type=int, required=True)
    star.set_defaults(cmd=_cmd_star)


def _cmd_star(args: argparse.Namespace) -> None:
    handle_radius_shape("star", args)


if __name__ == "__main__":
    main()
