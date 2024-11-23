from random import randint

class Player:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.pos = 0
        self.owned = []

    def __str__(self):
        return f"Player id {self.id}, position: {self.pos}, balance: ${self.balance}"

    def rollDice(self) -> int:
        """
        Rolls a dice and moves the player
        :return: int, the current position of player
        """
        self.pos += randint(1, 6)
        if self.pos > 26:
            self.pos -= 26
        return self.pos