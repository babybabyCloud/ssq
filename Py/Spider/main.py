#! -*- encoding;utf-8 -*-

import argparse
import sys
from . import argumentsparser, SubCommandType


def main():
    args = parse_args()
    args.sub_command.execute(args.sub_args)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('sub_command', action=argumentsparser.SubCommandAction, 
        choices=[item.value for item in list(SubCommandType)])
    parser.add_argument('sub_args', nargs=argparse.REMAINDER)
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())
