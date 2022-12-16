import sys
from src.modules.logic.Pinger import Pinger
from src.modules.console.ArgParser import ArgParser


def get_args():
    """ Get arguments from command line """
    arg_parser = ArgParser(sys.argv[1:])
    try:
        args = arg_parser.parse()
    except ValueError as e:
        print(str(e))
        sys.exit()
    return args


def main():
    """ Main function """
    args = get_args()
    pinger = Pinger(args)
    pinger.start()


if __name__ == '__main__':
    main()
