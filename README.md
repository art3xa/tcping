# TCPing

Version 0.1

Author: Artyom Romanov (artem.romanov.03@bk.ru)

Reviewers:

## Description
 - An analog of the ping command in Linux. 
 - Sends Echo requests via ICMP. 
 - At the end of the work, it builds a statistics


# Usage
- Working with the program is very simple. 
- You need to specify the host and the number of requests to be sent. 
- The program will send the specified number of requests and display the statistics.
- Support Windows, Linux.

`tcping.py [-h] [-p PORT] [-c COUNT] [-i INTERVAL] [-t TIMEOUT] ip`

Run on Linux:
`sudo python3 tcping.py [OPTIONS] ip`

Run on Windows:
`python tcping.py [OPTIONS] ip`


Run tests:
`python -m unittest src/tests/tests.py`

# Options
Options `[OPTIONS]` must be the following:

`-p, --port` — port (80 by default)

`-t, --timeout` — response timeout (2s by default)

`-c, --count` — number of requests (infinity by default)

`-i, --interval` — interval between requests (1s by default)

`-h, --help` — show this help message and exit

# Examples
`python tcping.py wikipedia.org -p 80`

`python tcping.py 8.8.8.8 -p 53 -c 10`

`python tcping.py 1.1.1.1 -p 53 -c 10 -i 0.5 -t 5`

## Functionality
- TCPing
- Statistics
- Support Windows, Linux
- Support IPv4, IPv6
- Support port
- Mock tests

## Structure
- `tcping.py` — main file
- `src/` — source files
- `tests/` — tests
- `README.md` — this file
- `src/modules/` — modules
- `src/modules/icmp/Socket.py` — ICMP socket
- `src/modules/icmp/EchoRequest.py` — ICMP Echo Request
- `src/modules/icmp/EchoReply.py` — ICMP Echo Reply
- `src/modules/logic/Pinger` — Logic of the program
- `src/modules/helpers.py` — Statistics
- `src/modules/console/ArgParser` — Arguments parser
- `src/modules/console/DataArgumnets` — Dataclass with arguments

## Realization
### ICMP
`https://www.rfc-editor.org/rfc/rfc792`

Echo or Echo Reply Message
```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type      |     Code      |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Data ...
   +-+-+-+-+-
```
   IP Fields:

   Addresses

      The address of the source in an echo message will be the
      destination of the echo reply message.  To form an echo reply
      message, the source and destination addresses are simply reversed,
      the type code changed to 0, and the checksum recomputed.

   IP Fields:

   Type

      8 for echo message;

      0 for echo reply message.

   Code

      0

   Checksum

      The checksum is the 16-bit ones's complement of the one's
      complement sum of the ICMP message starting with the ICMP Type.
      For computing the checksum , the checksum field should be zero.
      If the total length is odd, the received data is padded with one
      octet of zeros for computing the checksum.  This checksum may be
      replaced in the future.

   Identifier

      If code = 0, an identifier to aid in matching echos and replies,
      may be zero.
    
   Sequence Number

      If code = 0, a sequence number to aid in matching echos and
          replies, may be zero.

   Description

      The data received in the echo message must be returned in the echo
      reply message.

      The identifier and sequence number may be used by the echo sender
      to aid in matching the replies with the echo requests.  For
      example, the identifier might be used like a port in TCP or UDP to
      identify a session, and the sequence number might be incremented
      on each echo request sent.  The echoer returns these same values
      in the echo reply.

      Code 0 may be received from a gateway or a host.

# Requirements
- Python 3.8+
