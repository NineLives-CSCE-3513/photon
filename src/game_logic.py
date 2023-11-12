# Author: Thomas J. Buser
# Date Created: 15 September 2023
# Purpose: Module to handle game state including who hit who and what bases have been scored.

from typing import Dict

class GameState:
    def __init__(self) -> None:
        self.users = {}
        self.red_team_score: int = 0
        self.green_team_score: int = 0
        self.red_base_score_valid: bool = True
        self.green_base_score_valid: bool = True
        self.red_base_scored: bool = False
        self.green_base_scored: bool = False

    def set_users(self, users: Dict[str, Dict[int, tuple[int, str]]]) -> None:
        self.users = users

    def player_hit(self, equipment_shooter_code: int, equipment_hit_code: int):
        pass

    def red_base_hit(self, equipment_shooter_code: int):
        if self.red_base_hit_valid:
            self.red_base_hit = True
            # TODO: Attribute points to player and team
            self.red_base_hit_valid = False
        else:
            pass

    def green_base_hit(self, equipment_shooter_code: int):
        if self.green_base_hit_valid:
            self.green_base_hit = True
            # TODO: Attribute points to player and team
            self.green_base_hit_valid = False
        else:
            pass