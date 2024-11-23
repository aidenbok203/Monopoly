class Player:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.pos = 0
        self.owned = []

    def __str__(self):
        return f"Player id {self.id}, position: {self.pos}, balance: ${self.balance}"