# Author: Thomas J. Buser
# Date Created: 30 August 2023
# Purpose: Module to handle UDP networking for the Photon laser tag system communication between the control console and the packs.

from typing import Dict, List
import socket
import time

from user import User
from game_logic import GameState

# Defining constants for transmitting and receiving codes
START_GAME_CODE: int = 202
END_GAME_CODE: int = 221
RED_BASE_SCORED_CODE: int = 53
GREEN_BASE_SCORED_CODE: int = 43
BUFFER_SIZE: int = 1024
GAME_TIME_SECONDS: int = 360 # Seconds
BROADCAST_ADDRESS: str = "127.0.0.1"
RECEIVE_ALL_ADDRESS: str = "0.0.0.0"
TRANSMIT_PORT: int = 7501
RECEIVE_PORT: int = 7500

class Networking:
    def __init__(self) -> None:
        pass
    
    def set_sockets(self) -> bool:
        # Set up transmit and receive sockets
        try:
            self.transmit_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receive_socket.bind((RECEIVE_ALL_ADDRESS, RECEIVE_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def close_sockets(self) -> bool:
        # Close transmit and receive sockets
        try:
            self.transmit_socket.close()
            self.receive_socket.close()
            return True
        except Exception as e:
            print(e)
            return False

    def transmit_equipment_code(self, equipment_code: str) -> bool:
        # Enable broadcasts at the syscall level and priviledged process
        # Transmit provided equipment code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(equipment_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
    
    def transmit_start_game_code(self) -> bool:
        # Transmit start game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(START_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False
            
    def transmit_end_game_code(self) -> bool:
        # Transmit end game code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(END_GAME_CODE)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def transmit_player_hit(self, player_code: int) -> bool:
        # Transmit player hit code to the broadcast address
        try:
            self.transmit_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.transmit_socket.sendto(str.encode(str(player_code)), (BROADCAST_ADDRESS, TRANSMIT_PORT))
            return True
        except Exception as e:
            print(e)
            return False

    def run_game(self, current_game_state: GameState) -> None:
        # While the game is still running, receive data from the receive socket
        start_time: int = int(time.time())
        while int(time.time()) < (start_time + GAME_TIME_SECONDS):
            raw_message, return_address = self.receive_socket.recvfrom(BUFFER_SIZE)
            decoded_message: str = raw_message.decode("utf-8")
            message_components: [str] = decoded_message.split(":")
            left_code: int = int(message_components[0])
            right_code: int = int(message_components[1])

            # If the red base is hit, attribute 100 points to green team and vice versa
            # If player was hit instead, attribute 10 points to the attacker
            if right_code == 53:
                current_game_state.red_base_hit(left_code)
                self.transmit_equipment_code(str(RED_BASE_SCORED_CODE))
            elif right_code == 43:
                current_game_state.green_base_hit(left_code)
                self.transmit_equipment_code(str(GREEN_BASE_SCORED_CODE))
            elif right_code != 53 and right_code != 43 and right_code <= 100:
                current_game_state.player_hit(left_code, right_code)
                self.transmit_player_hit(right_code)
            else:
                print("Invalid codes: Left Code is " + str(left_code) + " Right Code is " + str(right_code))

        # Once game ends, transmit end game code 3 times
        self.transmit_end_game_code()
        self.transmit_end_game_code()
        self.transmit_end_game_code()
    
# Below is only for testing purposes, ran if this file is the entry point
if __name__ == "__main__":
    # Create networking object and dictionary to store user info
    network_mod: Networking = Networking()
    users: Dict[str, List[User]] = {
        "green" : [],
        "red" : []
    }

    # Add fake users to the dictionary
    users["green"].append(User(1, 10, 10, "John Conner"))
    users["green"].append(User(2, 20, 20, "Sarah Conner"))
    users["red"].append(User(3, 30, 30, "James Conner"))
    users["red"].append(User(4, 40, 40, "Someone Conner"))
    game: GameState = GameState(users)

    # Open sockets, transmit start game code, run game, transmit end game code, close sockets
    network_mod.set_sockets()
    network_mod.transmit_start_game_code()
    network_mod.run_game(game)
    network_mod.transmit_end_game_code()
    network_mod.close_sockets()