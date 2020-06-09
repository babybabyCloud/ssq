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
	parser.add_argument('--db-file', help='sqlite db file position must be provided', dest='db_file', required=True)
	args, sub_args = parser.parse_args(sys.argv[1:])
	args.sub_command.execute(sub_args)


if __name__ == '__main__':
	sys.exit(main())
