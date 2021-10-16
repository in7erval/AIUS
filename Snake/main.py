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
    innergroup = group.add_argument_group()
    innergroup.add_argument('-B', '--block-size', help='block size in px (default: 50)', default=50, type=int)
    innergroup.add_argument('-F', '--fun', action='store_true', help='fun game')
    return parser_new


def parse_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if args.size <= 3 or args.size > 20:
        print('Use size in range from 4 to 20!')
        return
    if args.block_size < 25 or args.block_size > 200:
        print('Use block_size in range from 25 to 200!')
        return
    try:
        game = None
        if args.cli:
            game = Game(ConsoleInterface(args.size))
        elif args.gui:
            if args.size < 10:
                print('Use size in range from 10 to 20!')
                return
            game = Game(GraphicalInterface(args.size, fun=args.fun, block_size=args.block_size))
        game.start()
    except RuntimeError as err:
        print(err.args[0])


if __name__ == '__main__':
    parser = init_argparse()
    parse_args(parser)
