import socket
from time import perf_counter
from src.modules.icmp.EchoReply import EchoReply
from src.modules.icmp.EchoRequest import EchoRequest
from src.modules.icmp.Socket import Socket
from src.modules.helpers import print_statistics
from time import sleep


class Pinger:
    def __init__(self, args):
        """ Initialize Pinger """
        try:
            self.ip_addr = socket.gethostbyname(args.ip)
        except socket.gaierror:
            print(f"Could not resolve {args.ip}")
            exit(1)
        self.ip = args.ip
        self.port = args.port
        self.count = args.count
        self.interval = args.interval
        self.timeout = args.timeout
        try:
            self.host = socket.gethostbyaddr(self.ip)[0]
        except socket.herror:
            self.host = self.ip

    def start(self):
        """ Start pinging """
        print(f"PING {self.ip} ({self.ip_addr}) "
              f"{EchoRequest().get_length()} bytes of data.")
        icmp_seq = 1
        times = []
        while True:
            try:
                time = self.tcping(icmp_seq)
                times.append(time)
                if self.count == icmp_seq:
                    break
                icmp_seq += 1
            except KeyboardInterrupt:
                print_statistics(self.ip, times)
                return

        print_statistics(self.ip, times)

    def tcping(self, icmp_seq):
        """ Send an ICMP echo echo_request and print the reply """
        try:
            reply, time = self.ping()
            if self.interval is not None:
                sleep(self.interval)
            if reply.type != 0:
                print(f'Unexpected reply type={reply.type}, '
                      f'should have been 0')
            elif reply.code != 0:
                print(f'Unexpected reply code={reply.code}, '
                      f'should have been 0')
            else:
                print(f'{reply.len} bytes from {self.host} '
                      f'({self.ip_addr}[:{self.port}]): icmp_seq={icmp_seq} '
                      f'ttl={reply.ttl} time={str(round(time, 1))} ms')
            return time
        except socket.timeout:
            print(f'Request timed out.')
        return None

    def ping(self):
        """ Send an ICMP echo echo_request and return the reply """
        start = perf_counter()
        socket = Socket(self.timeout)
        reply = socket.send_and_recv(EchoRequest(), self.ip, self.port)
        icmp_reply = EchoReply(reply)
        time = (perf_counter() - start) * 1000
        socket.close()
        return icmp_reply, time
