from argparse import ArgumentParser
from src.modules.console.DataArguments import DataArguments


class ArgParser:
    """ Argument Parser"""

    def __init__(self, args):
        self._parser = ArgumentParser(prog="TCPing",
                                      description="An analog of the "
                                                  "ping command in Linux",
                                      )
        self._args = args
        self._add_arguments()

    def _add_arguments(self):
        """
        Add arguments to the parser
        """
        self._parser.add_argument("ip", type=str,  # required=True,
                                  help="IP address or domain name")
        self._parser.add_argument("-p", "--port", type=int, metavar='PORT',
                                  default=80,
                                  help="port (80 by default)")
        self._parser.add_argument("-t", "--timeout", type=float, default=2.0,
                                  help="timeout for requests (2s by default)")
        self._parser.add_argument("-c", "--count",
                                  type=int, default=None,
                                  help="amount of requests")
        self._parser.add_argument("-i", "--interval", type=float, default=1.0,
                                  help="interval between requests "
                                       "(1s by default)")

    def parse(self):
        """
        Parsing arguments
        """
        args = self._parser.parse_args(self._args)

        return DataArguments(args.ip, args.port, args.count,
                             args.interval, args.timeout)
