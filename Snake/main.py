import argparse

from common.Game import Game
from console.ConsoleInterface import ConsoleInterface
from graphical.GraphicalInterface import GraphicalInterface


def init_argparse() -> argparse.ArgumentParser:
    parser_new = argparse.ArgumentParser(description="Snake game. Use 'wasd' or arrows to move snake")
    parser_new.add_argument("-S", "--size", help='set field size (default: 10)', default=10, type=int)
    group = parser_new.add_mutually_exclusive_group(required=True)
    group.add_argument('--cli', action='store_true', help='Command line interface')
    group.add_argument('--gui', action='store_true', help='Graphical user interface')
    guigroup = group.add_argument_group()
    guigroup.add_argument('-B', '--block-size', help='block size in px (default: 50)', default=50, type=int)
    guigroup.add_argument('-F', '--fun', action='store_true', help='fun game')
    guigroup.add_argument('-C', '--cheat-mode', action='store_true', help='cheat mode')
    return parser_new


def check_args(args):
    if args.size <= 3 or args.size > 20:
        raise RuntimeError('Use size in range from 4 to 20!')
    if args.block_size < 25 or args.block_size > 200:
        raise RuntimeError('Use block_size in range from 25 to 200!')
    if args.gui and args.size < 10:
        raise RuntimeError('Use size in range from 10 to 20!')


def initialize_game(parser: argparse.ArgumentParser) -> Game:
    args = parser.parse_args()
    check_args(args)
    if args.cli:
        return Game(ConsoleInterface(args.size, cheat=args.cheat_mode))
    elif args.gui:
        return Game(GraphicalInterface(args.size, fun=args.fun, block_size=args.block_size, cheat=args.cheat_mode))


if __name__ == '__main__':
    try:
        parser = init_argparse()
        game = initialize_game(parser)
        game.start()
    except RuntimeError as err:
        print(err.args[0])
