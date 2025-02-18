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
    owned: int = None

    def __str__(self):
        return f"Position: {self.pos}, Colour: {self.colour}, Name: {self.name}, Cost: {self.cost}, Level {self.level}, Upgrade cost: {self.upgradeCost}, Rent: {self.rent}, Owned by: {self.owned}"

    def sellTile(self) -> None:
        """
        Revert the tile to default
        :return: None
        """
        self.level = 1
        self.rent = self.l1
        self.owned = False

    def dictForm(self):
        """
        Returns in dictionary format
        :return dict: Dictionary including data of player object
        """
        return {
            "pos": self.pos,
            "colour": self.colour,
            "name": self.name,
            "cost": self.cost,
            "l1": self.l1,
            "l2": self.l2,
            "l3": self.l3,
            "l4": self.l4,
            "l5": self.l5,
            "upgradeCost": self.upgradeCost,
            "rent": self.rent,
            "level": self.level,
            "owned": self.owned
        }