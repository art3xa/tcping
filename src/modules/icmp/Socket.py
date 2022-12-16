import socket


class Socket:
    def __init__(self, timeout=None):
        """ Initialize Socket """
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_RAW,
                                    socket.IPPROTO_ICMP)
        self.socket.settimeout(timeout)

    def send_and_recv(self, icmp_echo_request, host, port=80):
        """ Send ICMP Echo Request to ip:port and return reply """
        self.socket.sendto(bytes(icmp_echo_request), (host,  port))
        return self.socket.recvfrom(2 ** 12)

    def close(self):
        """ Close socket """
        self.socket.close()
