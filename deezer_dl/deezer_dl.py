import argparse

from deezer_dl import logger
from deezer_dl.deezer import Deezer


def deezer_dl():
    parser = argparse.ArgumentParser(description='deezer_dl CLI')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument('-l', '--url', nargs='*', dest='url', required=True, help='URL to deezer playlist or song')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(level=10)

    if args.url:
        Deezer(args.url[0]).download()


if __name__ == '__main__':
    deezer_dl()
