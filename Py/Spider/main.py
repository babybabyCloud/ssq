#! -*- encoding;utf-8 -*-

import argparse
import sys
import Spider
import Spider.downloader.Manager
import Spider.argumentsparser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sub_command', action=Spider.argumentsparser.SubCommandAction, 
        choices=[item.value for item in list(Spider.SubCommandType)])
    parser.add_argument('sub_args', nargs=argparse.REMAINDER)
    args = parser.parse_args(sys.argv[1:])
    args.sub_command.execute(args.sub_args)


if __name__ == '__main__':
    sys.exit(main())
