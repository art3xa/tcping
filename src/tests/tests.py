import io
import unittest
from socket import AddressFamily, SocketKind
from unittest import mock

from src.modules.console.ArgParser import ArgParser
from src.modules.console.DataArguments import DataArguments
from src.modules.icmp.EchoReply import EchoReply
from src.modules.icmp.EchoRequest import EchoRequest
from src.modules.icmp.Socket import Socket
from src.modules.helpers import print_statistics
from src.modules.logic.Pinger import Pinger
from tcping import main, get_args


class SocketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.echo_request = EchoRequest()
        self.socket_inf = (AddressFamily.AF_INET, SocketKind.SOCK_RAW, 1)
        self.port = 53
        self.ip = '8.8.8.8'
        self.recv_size = (4096,)
        self.none_timeout = (None,)
        self.reply = b'123'
        self.timeout = (3,)

    def test_icmp_socket(self) -> None:
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recvfrom.return_value \
                = self.reply
            icmp_socket = Socket()
            icmp_socket.send_and_recv(EchoRequest(), '8.8.8.8', 53)
            icmp_socket.close()

        self.assertEqual('', mock_socket.mock_calls[0][0])
        self.assertEqual(self.socket_inf, mock_socket.mock_calls[0][1])
        self.assertEqual('().settimeout', mock_socket.mock_calls[1][0])
        self.assertEqual(self.none_timeout, mock_socket.mock_calls[1][1])
        self.assertEqual('().sendto', mock_socket.mock_calls[2][0])
        self.assertTrue(isinstance(mock_socket.mock_calls[2][1][0], bytes))
        self.assertEqual((self.ip, self.port), mock_socket.mock_calls[2][1][1])
        self.assertEqual('().recvfrom', mock_socket.mock_calls[3][0])
        self.assertEqual(self.recv_size, mock_socket.mock_calls[3][1])
        self.assertEqual('().close', mock_socket.mock_calls[4][0])
        self.assertEqual(self.reply,
                         mock_socket.return_value.recvfrom.return_value)

    def test_icmp_socket_with_timeout_and_reply(self) -> None:
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recvfrom.return_value \
                = self.reply
            icmp_socket = Socket(3)
            icmp_socket.send_and_recv(EchoRequest(), '8.8.8.8', 53)
            icmp_socket.close()

        self.assertEqual('', mock_socket.mock_calls[0][0])
        self.assertEqual(self.socket_inf, mock_socket.mock_calls[0][1])
        self.assertEqual('().settimeout', mock_socket.mock_calls[1][0])
        self.assertEqual(self.timeout, mock_socket.mock_calls[1][1])
        self.assertEqual('().sendto', mock_socket.mock_calls[2][0])
        self.assertTrue(isinstance(mock_socket.mock_calls[2][1][0], bytes))
        self.assertEqual((self.ip, self.port), mock_socket.mock_calls[2][1][1])
        self.assertEqual('().recvfrom', mock_socket.mock_calls[3][0])
        self.assertEqual(self.recv_size, mock_socket.mock_calls[3][1])
        self.assertEqual('().close', mock_socket.mock_calls[4][0])
        self.assertEqual(self.reply,
                         mock_socket.return_value.recvfrom.return_value)


class StatisticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = '8.8.8.8'
        self.times_zero_losses = [34.0, 33.3, 33.6]
        self.times_one_loss = [34.0, 33.3, None]
        self.times_all_losses = [None, None, None]

        self.result_zero_losses = '''
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 100.9ms
rtt min/avg/max = 33.3/33.633/34.0 ms
'''
        self.result_one_loss = '''
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 2 received, 33% packet loss, time 67.3ms
rtt min/avg/max = 33.3/33.65/34.0 ms
'''
        self.result_all_losses = '''
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss
'''

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_stats_zero_loss(self, stdout) -> None:
        print_statistics(self.ip, self.times_zero_losses)
        self.assertEqual(stdout.getvalue(), self.result_zero_losses)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_stats_one_loss(self, stdout) -> None:
        print_statistics(self.ip, self.times_one_loss)
        self.assertEqual(stdout.getvalue(), self.result_one_loss)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_statistics_all_none(self, stdout) -> None:
        print_statistics(self.ip, self.times_all_losses)
        self.assertEqual(stdout.getvalue(), self.result_all_losses)


class EchoRequestTests(unittest.TestCase):

    def setUp(self) -> None:
        self.TEST_DATA = b'123'
        self.echo_request = EchoRequest(self.TEST_DATA)
        self.data = (
            b'\xa59\x0b\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17'
            b'\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567')
        self.encoded_data = 'b\'313233\''

    def test_echo_request(self):
        self.assertEqual(self.echo_request.data, self.data)
        self.assertEqual(self.echo_request.encoded_data, self.encoded_data)


class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = '8.8.8.8'
        self.port = 53
        self.timeout = 1
        self.count = 3
        self.interval = 0.1
        self.parser = ArgParser(['-c', str(self.count), '-t',
                                 str(self.timeout), self.ip, '-p',
                                 str(self.port), '-i', str(self.interval)])

    def test_parser(self):
        args = self.parser.parse()
        self.assertEqual(args.ip, self.ip)
        self.assertEqual(args.port, self.port)
        self.assertEqual(args.timeout, self.timeout)
        self.assertEqual(args.count, self.count)
        self.assertEqual(args.interval, self.interval)


# class MainTests(unittest.TestCase):
#     def setUp(self) -> None:
#         self.ip = '8.8.4.4'
#         self.port = 53
#         self.timeout = 1
#         self.count = 3
#         self.interval = 0.1
#         self.parser = ArgParser(['-c', str(self.count), '-t',
#                                  str(self.timeout), self.ip, '-p',
#                                  str(self.port), '-i', str(self.interval)])
#
#     # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
#     # def test_main(self, stdout) -> None:
#     #     args = self.parser.parse()
#     #     self.assertEqual(stdout.getvalue(), '''---''')
#

# class PingerTests(unittest.TestCase):
#     def setUp(self) -> None:
#         self.ip = '8.8.8.8'
#         self.port = 53
#         self.timeout = 1
#         self.count = 3
#         self.interval = 0.1
#         self.parser = ArgParser(
#             ['-c', str(self.count), '-t', str(self.timeout), self.ip, '-p',
#              str(self.port), '-i', str(self.interval)])
#         self.args = self.parser.parse()
#         self.pinger = Pinger(self.args)
#         self.pinger.start()
#         self.pinger.tcping(2)
#         self.pinger.ping()


class DataArgumentsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ip: str = '1.1.1.1'
        self.port: int = 53
        self.count: int = 3
        self.interval: float = 0.1
        self.timeout: float = 1

    def test_data_arguments(self):
        self.data_arguments = DataArguments(self.ip, self.port, self.count,
                                            self.interval, self.timeout)
        self.assertEqual(self.data_arguments.ip, self.ip)
        self.assertEqual(self.data_arguments.port, self.port)
        self.assertEqual(self.data_arguments.count, self.count)
        self.assertEqual(self.data_arguments.interval, self.interval)
        self.assertEqual(self.data_arguments.timeout, self.timeout)


class EchoReplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ip = '8.8.8.8'
        self.port = 53
        self.ttl = 55
        self.type = 0
        self.code = 0
        self.data = b"\x45\x40\x00\x4c\x00\x00\x00\x00\x37\x01\x0a\xdf" \
            b"\x8e\xfa\x96\x5b\xac\x1d\xa7\x1f\x00\x00\x06\xf3" \
            b"\x89\x00\x01\x00\xa5\x39\x0b\x00\x00\x00\x00\x00" \
            b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b" \
            b"\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27" \
            b"\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33" \
            b"\x34\x35\x36\x37"

    def test_echo_reply(self):
        self.echo_reply = EchoReply((self.data, (self.ip, self.port)))
        self.assertEqual(self.echo_reply.ttl, self.ttl)
        self.assertEqual(self.echo_reply.type, self.type)
        self.assertEqual(self.echo_reply.code, self.code)


if __name__ == '__main__':
    unittest.main()
