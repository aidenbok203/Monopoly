from random import randint
from game import init
from classes import tile_definitions as t_def

class Player:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.pos = 0
        self.owned = []
        self.bankrupt = False

    def __str__(self):
        return f"Player id {self.id}, position: {self.pos}, balance: ${self.balance}"

    def rollDice(self) -> int:
        """
        Rolls a dice and moves the player
        :return: int, the current position of player
        """
        self.pos += randint(1, 6)
        if self.pos > 22:
            self.pos -= 22
        return self.pos

    def checkBankruptcy(self) -> bool:
        """
        Checks if a user is bankrupt
        :param player: Object of player
        :return: bool, If user is bankrupt
        """
        if self.balance < 0:
            self.bankrupt = True
            init.bankruptPlayers += 1
            return True
        else:
            return False

    def removeProperty(self, tile: t_def.Tile):
        """
        Remove property from player
        :param tile: Object of tile
        :return: None
        """
        if tile in self.owned:
            self.balance += tile.cost
            self.owned.remove(tile)