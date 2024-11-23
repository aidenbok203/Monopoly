class Player:
    def __init__(self, id, pos, balance):
        self.id = id
        self.pos = pos
        self.balance = balance
        self.owned = []

    def __str__(self):
        return f"Player id {self.id}, position: {self.pos}, balance: ${self.balance}"