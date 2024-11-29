from dataclasses import dataclass

@dataclass
class Tile:
    pos: int
    colour: str
    name: str
    cost: int
    l1: int
    l2: int
    l3: int
    l4: int
    l5: int
    upgradeCost: int
    rent: int
    level: int = 1
    owned: bool = False

    def __str__(self):
        return f"Position: {self.pos}, Colour: {self.colour}, Name: {self.name}, Cost: {self.cost}, Level {self.level}, Upgrade cost: {self.upgradeCost}, Rent: {self.rent}, Owned: {self.owned}"

    def sellTile(self):
        """
        Revert the tile to default
        :return: None
        """
        self.level = 1
        self.rent = self.l1
        self.owned = False