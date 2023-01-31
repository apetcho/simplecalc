#!/usr/bin/env python3
import random
import socket
import signal
import sys
import json
from typing import Optional, Callable, Any, Tuple


def on_quit(signum, args):
    """Handle the CTRL-C signal"""
    if signum == signal.SIGINT:
        sys.exit(0)   # Quit gracefully

def get_random_operator() -> str:
    """Return randomly on '+' or '-' arithmetic operator."""
    return random.choice(["+", "-"])

def get_random_args() -> Tuple[int, int]:
    """Get random args"""
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    return (x, y)


def run(host="127.0.0.1", port=5000, buflen=4096):
    """Main server entry."""
    signal.signal(signal.SIGINT, on_quit)
    while len(sys.argv) != 3:
        print("Incorrect command")
        print(f"usage: ./{sys.argv[0]} <ncalc> <delay>")
        print("Example:")
        print(f"    ./{sys.argv[0]} 10 0.1\n")
    ncalc = int(sys.argv[1])
    delay = float(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockfd:
        sockfd.connect((host, port))
        k = 0
        results = []
        op = get_random_operator()
        while k < ncalc:
            x, y = get_random_args()
            req = f"calc {x} {op} {y}"
            sockfd.send(req.encode("utf-8"))
            sockfd.settimeout(delay)
            try:
                response = sockfd.recv(buflen).decode("utf-8")
            except socket.timeout:
                response = "n"
            if response == "n":
                results.append(response)
            else:
                response = response.strip().split()[1]
                results.append(response)
            k += 1
    return results

def main():
    """Main entry"""
    out = run()
    print(f"Result:\n{out}")



if __name__ == "__main__":
    main()
