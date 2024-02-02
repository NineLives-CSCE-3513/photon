import socket
import random
import time
from typing import Tuple

BUFFER_SIZE: int = 1024
SERVER_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7501)
CLIENT_ADDRESS_PORT: Tuple[str, int] = ("127.0.0.1", 7500)
START_CODE: str = "202"
END_CODE: str = "221"

def get_player_id(color: str, player_number: int) -> str:
    return input(f"Enter equipment id of {color} player {player_number} ==> ")

def create_socket(address_port: Tuple[str, int]) -> socket.socket:
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind(address_port)
    return sock

def wait_for_start(sock: socket.socket) -> None:
    print ("waiting for start from game_software")
    received_data: str = " "
    while received_data != START_CODE:
        received_data, address = sock.recvfrom(BUFFER_SIZE)
        received_data = received_data.decode("utf-8")
        print("Received from game software: ", received_data)

def main() -> None:
    print("This program will generate some test traffic for 2 players\n"
		  "on the red team as well as 2 players on the green team\n")

    red1: str = get_player_id("red", 1)
    red2: str = get_player_id("red", 2)
    green1: str = get_player_id("green", 1)
    green2: str = get_player_id("green", 2)

    UDPServerSocketReceive: socket.socket = create_socket(SERVER_ADDRESS_PORT)
    UDPClientSocketTransmit: socket.socket = create_socket(CLIENT_ADDRESS_PORT)

    wait_for_start(UDPServerSocketReceive)

    while True:
        redplayer: str = red1 if random.randint(1,2) == 1 else red2
        greenplayer: str = green1 if random.randint(1,2) == 1 else green2
        message: str = f"{redplayer}:{greenplayer}" if random.randint(1,2) == 1 else f"{greenplayer}:{redplayer}"

        print(message)

        if int(input("Exit?")) == 1:
            exit()

        UDPClientSocketTransmit.sendto(str.encode(str(message)), CLIENT_ADDRESS_PORT)

        received_data: str
        address: Tuple[str, int]
        received_data, address = UDPServerSocketReceive.recvfrom(BUFFER_SIZE)
        received_data = received_data.decode("utf-8")
        print ("Received from game software: ", received_data)

        if received_data == END_CODE:
            break

        time.sleep(random.randint(1,3))

    print("program complete")

if __name__ == "__main__":
    main()