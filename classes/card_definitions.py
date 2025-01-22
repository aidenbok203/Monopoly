from dataclasses import dataclass
from typing import Callable
from classes import player_definitions as p_def

@dataclass
class Chance:
    title: str
    desc: str
    func: str
    used: bool = False

    def execute(self, player: p_def.Player) -> None:
        """
        Executes the function(s) attributed to the card for the specified player
        :param player: Object of player
        """
        for func in self.func:
            eval(func)

