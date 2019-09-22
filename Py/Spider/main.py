#! -*- encoding;utf-8 -*-

import sys
import argparse
import Spider.Manager


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--db-file', help='You must provide the sqlite file position', dest='db_file', required=True)
	Spider.Manager.main(**vars(parser.parse_args(sys.argv[1:])))


if __name__ == '__main__':
	sys.exit(main())
