#!/usr/bin/env python3
#!/usr/bin/env python3
import random
import socket
import signal
import json
import time
import sys
from typing import Optional, Callable, Any


def get_operation(op):
    """Return a random arithmetic operator."""
    opmap = {}
    opmap["+"] = lambda x, y: x + y
    opmap["-"] = lambda x, y: x - y

    return opmap[op]


def on_quit(signum, args):
    """Handle the CTRL-C signal"""
    if signum == signal.SIGINT:
        sys.exit(0)   # Quit gracefully


def main(host="127.0.0.1", port=5000, buflen=4096):
    """Main server entry."""
    random.seed(time.time())
    signal.signal(signal.SIGINT, on_quit)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockfd:
        sockfd.bind((host, port))
        print(f"Server ready at {sockfd.getsockname()}")
        while True:
            req, address = sockfd.recvfrom(buflen)
            req = req.decode("utf-8").strip().split()
            x = req[1]
            op = req[2]
            y = req[3]
            fun = get_operation(op)
            result = fun(x, y)
            message = f"ans {result}".encode("utf-8")
            sockfd.sendto(message, address)

if __name__ == "__main__":
    main()
