from game import init
from classes import player_definitions as p_def
from classes import tile_definitions as t_def
from os import system, name


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
    :param property: Object of tile
    :return: None
    """
    if player.balance >= property.cost:
        player.balance -= property.cost
        property.owned = True
        player.owned.append(property)
    else:
        print(f"You do not have enough money to purchase {property.name}!")

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
            break
    if tile.owned:
        print(f"This tile is owned! You have to pay {tile.rent}")
        payRent(player, tile)
        player.checkBankruptcy()
    else:
        try:
            if input("Would you like to purchase? (y/n) ").lower() == "y":
                purchase(player, tile)
        except:
            print("Invalid input.")
        else:
            print("Continuing game...")

def upgradeHouse(player: p_def.Player, property: t_def.Tile) -> None:
    """
    Adds level to tile, sets new rent, and charges player
    :param player: Object of player
    :return: None
    """
    if property not in player.owned:
        print("You do not own this property!")
        return
    match = 0
    for tile in player.owned:
        if tile.colour == property.colour:
            match += 1
    if match != init.setLimit[property.colour]:
        print(f"You do not have the full set of {property.colour} properties!")
        return
    if property.level == 5:
        print("Your property is already fully upgraded!")
        return
    if player.balance > property.upgradeCost:
        player.balance -= property.upgradeCost
        property.level += 1
        property.rent = getattr(property, f"l{property.level}")
        print(f"Upgraded {property.name} to level {property.level}!")
    else:
        print("You do not have sufficient funds!")

def clearTerminal():
    """
    Clears the terminal.
    :return: None
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")
