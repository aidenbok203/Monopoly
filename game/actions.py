from game import init
from classes import player_definitions as p_def
from classes import tile_definitions as t_def

def checkBankruptcy(player: p_def.Player):
    

def purchase(player: p_def.Player, property: t_def.Tile):
    """
    Remove cost and add property to player
    :param player: Object of player
    :param property: int, Tile.pos
    :return: None
    """
    if player.balance >= property.cost:
        player.balance -= property.cost
        property.owned = True
        player.owned.append(property)
    else:


def roll(player: p_def.Player) -> None:
    """
    Functionality for roll dice
    :param player: Object of player
    :return: None
    """
    currentPos = player.rollDice()
    player.pos = currentPos
    for tile in init.board:
        if tile.pos == currentPos:
            print(f"You have landed on {tile.name}")
    if not tile.owned and input("Would you like to purchase? (y/n)").lower() == "y":
        