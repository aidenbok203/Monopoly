from dataclasses import dataclass
from classes import player_definitions as p_def
from game import init

@dataclass
class Card:
    title: str
    func: list[str]
    used: bool = False

    def __str__(self):
        return f"{self.title}, Used: {self.used}"

    def execute(self, player: p_def.Player) -> None:
        """
        Executes the function(s) attributed to the card for the specified player
        :param player: Object of player
        :return: None
        """
        context = {
            "Player": player,
            "pos": player.pos,
            "balance": player.balance,
            "playerNum": init.playerNum
        }
        for func in self.func:
            exec(func, context)

    def dictForm(self):
        """
        Returns in dictionary format
        :return dict: Dictionary including data of tile object
        """
        return {
            "title": self.title,
            "func": self.func,
            "used": self.used
        }

