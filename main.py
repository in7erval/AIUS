from common.Game import Game
import argparse

from console.ConsoleInterface import ConsoleInterface
from graphical.GraphicalInterface import GraphicalInterface


def init_argparse() -> argparse.ArgumentParser:
    parser_new = argparse.ArgumentParser(description="Snake game. Use 'wasd' or arrows to move snake")
    parser_new.add_argument("-S", "--size", help='set field size (default: 10)', default=10, type=int, )
    group = parser_new.add_mutually_exclusive_group(required=True)
    group.add_argument('--cli', action='store_true', help='Command line interface')
    group.add_argument('--gui', action='store_true', help='Graphical user interface')
    return parser_new


def parse_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if args.size <= 3 or args.size > 20:
        print('Use size in range from 4 to 20!')
        return
    if args.cli:
        try:
            game = Game(ConsoleInterface(args.size))
            game.start()
        except RuntimeError as err:
            print(err.args[0])
    elif args.gui:
        game = Game(GraphicalInterface(args.size, fun=True))
        game.start()


if __name__ == '__main__':
    parser = init_argparse()
    parse_args(parser)

