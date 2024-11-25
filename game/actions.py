from game import init
from classes import player_definitions as p_def
from classes import tile_definitions as t_def

def checkGameOver() -> object:
    """
    Checks whether the game is finished
    :return: Object of winning player
    """
    found = False
    if init.bankruptPlayers == init.bankruptLimit:
        while not found:
            for player in init.playerList:
                if not player.bankrupt:
                    found = True
                    return player
    return False

def payRent(player: p_def.Player, property: t_def.Tile):
    """
    Remove rent of property from player balance
    :param player: Object of player
    :param property: int, Tile.pos
    :return: None
    """
    player.balance -= property.rent


def purchase(player: p_def.Player, property: t_def.Tile) -> None:
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
        print(f"You do not have enough money to purchase {property}!")

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
    if tile.owned:
        print(f"This tile is owned! You have to pay {tile.rent}")
        payRent(player, tile)
        player.checkBankruptcy()
    elif not tile.owned and input("Would you like to purchase? (y/n)").lower() == "y":
        purchase(player, tile)
    else:
        print("Continuing game...")

def upgradeHouse(player: p_def.Player, tile: t_def.Tile) -> None:
    """

    """
    if tile.level == 5:
        print("Your property is already fully upgraded!")
        return
    if player.balance > tile.upgradeCost:
        player.balance -= tile.upgradeCost
        tile.level += 1
        tile.rent = getattr(tile, f"l{tile.level}")
    else:
        print("You do not have sufficient funds!")