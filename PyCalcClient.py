#!/usr/bin/env python3
from cProfile import label
import random
import socket
import signal
import sys
import matplotlib.pyplot as plt
import time
from typing import Optional, Callable, Any, Tuple

# -*-
# python PyCalcClient 10 0.1
# -*-

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


def run(ncalc, delay, host="127.0.0.1", port=5000, buflen=4096):
    """Main server entry."""
    signal.signal(signal.SIGINT, on_quit)
    # while len(sys.argv) != 3:
    #     print("Incorrect command")
    #     print(f"usage: ./{sys.argv[0]} <ncalc> <delay>")
    #     print("Example:")
    #     print(f"    ./{sys.argv[0]} 10 0.1\n")
    #ncalc = int(sys.argv[1])
    #delay = float(sys.argv[2])

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
                print(f" -> Received {response!r} from SimpleCalcServer")
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
    timings = []
    rates = []
    for delay in (0.001, 0.01):
        for ncalc in (1, 10, 100, 1000):
            tic = time.time()
            out = run(ncalc, delay)
            toc = time.time()
            runtime = toc - tic
            rate = len([x for x in out if x != 'n']) / len(out)
            rates.append((ncalc, delay, rate))
            timings.append((ncalc, delay, runtime))

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    x1data = [item[-1] for item in timings]
    ax1.plot(x1data, lw=2.0)
    ax1.set_title("Completion times")
    ax2 = fig.add_subplot(1, 2, 2)
    x2data = [item[-1] for item in rates]
    ax2.plot(x2data, lw=2)
    ax2.set_title("Rate of success")
    plt.savefig("simplecalc.png")
    plt.show()



if __name__ == "__main__":
    main()
