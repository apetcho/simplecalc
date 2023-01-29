#!/usr/bin/env python3
import socket
import random
import json
import matplotlib.pyplot as plt

def plotdata(data:dict):
    """Plot data"""
    xdata = data["x"]
    ydata = data["y"]
    num = data["num"]
    elapsed = data["elapsed"]
    # ---------  -----------
    # |       |  |          |
    # | y vs x|  | el  vs i |
    # ---------  -----------
    #
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.plot(xdata, ydata)
    indices = list(range(num))
    ax2.plot(indices, elapsed)
    plt.savefig("calcdata.png")
    plt.show()


def get_random_number_of_computation() -> int:
    """Get ...."""
    nums = [1, 10, 100, 1000]
    return random.choice(nums)


def check_request(request:str) -> int:
    """Check message."""
    if request.strip() == "quit":
        return 0 # Ok
    req = request.strip().split()
    # ["calc", ...]
    if req[0] != "calc":
        return -1 # Error
    if len(req) == 2 and req[1] != "shutdown":
        return -1 # Error
    # ["calc", "4", "+", "5"]
    if len(req) == 4 and req[2] in ("+", "-"):
        return 0  # Ok
    if len(req) == 2 and req[1] == "shutdown":
        return 0 # Ok
    return -1 # Error


def read_request() -> str:
    """Read the client request."""
    req = input("> ")
    return req
    

def main():
    """Client main app."""
    SERVER = ("127.0.0.1", 5500)
    header = "Simple Calculator Client"
    print(f"-*--{'-'*len(header)}--*-")
    print(f"-*- {header} -*-")
    print(f"-*--{'-'*len(header)}--*-")
    # print("You send a request to server using an expression as follows:")
    # print(" calc num1 op num2")
    # print("where num1 and num2 are integer and op is either + or -")
    # print("Example:")
    # print(" calc 3 + 2")
    # print(" calc 23 - 99")
    # print("\nTo shutdown the server, send the following request:")
    # print(" calc shutdown")
    # print("\nTo quit this application send the following request:")
    # print("quit")

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    req = f"{get_random_number_of_computation()}".encode("utf-8")
    sockfd.sendto(req, SERVER)
    answer = ""
    while True:
        response, addr = sockfd.recvfrom(2048)
        if len(response) == 0:
            break
        answer += response.decode("utf-8")
    response = json.loads(answer)


    # print(f"{json.dumps(response, indent=4)}")
    print(f"{response}")
    plotdata(response)
    
    # while True:
    #     req = read_request()
    #     if req == "quit":
    #         break
    #     status = check_request(req)
    #     while status != 0:
    #         print("\x1b[31mBad request format\x1b[m. Try again")
    #         req = read_request()
    #         if req == "quit" or req.strip().split()[1] == "shutdown":
    #             break
    #         status = check_request(req)
    #     sockfd.sendto(req.encode("utf-8"), SERVER)
    #     response, addr = sockfd.recvfrom(1024)
    #     answer = response.decode("utf-8")
    #     print(f"{answer}")

    sockfd.close()
        

if __name__ == "__main__":
    main()
