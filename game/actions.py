from game import init
from classes import card_definitions as c_def
from classes import player_definitions as p_def
from classes import tile_definitions as t_def
from os import system, name
from random import randint


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
        property.owned = player.id
        player.owned.append(property)
    else:
        print(f"You do not have enough money to purchase {property.name}!")

def resetCards(type: str) -> None:
    """
    Resets all cards to unused
    :param type: str, "Chance Card" or "Community Chest"
    :return: None
    """
    match type:
        case "Chance Card":
            for card in init.chanceList:
                if not card.used:
                    return
            for card in init.chanceList:
                card.used = False
        case "Community Chest":
            for card in init.communityList:
                if not card.used:
                    return
            for card in init.communityList:
                card.used = False

def drawCard(player: p_def.Player, type: str) -> None:
    """
    Draws a card from the specified deck
    :param player: Object of player
    :param str: "Chance Card" or "Community Chest"
    :return: None
    """
    match type:
        case "Chance Card":
            while True:
                card: c_def.Card = init.chanceList[randint(0, len(init.chanceList) - 1)]
                if not card.used:
                    break
        case "Community Chest":
            while True:
                card: c_def.Card = init.communityList[randint(0, len(init.communityList) - 1)]
                if not card.used:
                    break
    print(f"You have drawn \"{card.title}\".")
    card.used = True
    card.execute(player)
    resetCards(type)

def roll(player: p_def.Player) -> None:
    """
    Functionality for roll dice
    :param player: Object of player
    :return: None
    """
    if player.jailed:
        player.jail()
        return
    currentPos = player.rollDice()
    if currentPos == "jail":
        player.jail()
        return
    player.pos = currentPos
    for tile in init.board:
        if tile.pos == currentPos:
            if tile.name == "Jail":
                print("You are visiting the jail!")
                return
            print(f"You have landed on {tile.name}")
            if tile.name == "Chance Card" or tile.name == "Community Chest":
                drawCard(player, tile.name)
                input("Press enter to continue...")
                return
            break
    if tile.owned is not None:
        print(f"This tile is owned! You have to pay {tile.rent}")
        payRent(player, tile)
        player.checkBankruptcy()
    else:
        select = False
        while not select:
            match input("Would you like to purchase? (y/n) ").lower():
                case "y":
                    purchase(player, tile)
                    select = True
                case "n":
                    print("Continuing game...")
                    select = True
                case _:
                    print("Invalid input.")
                    clearTerminal()
                    print(f"You have landed on {tile.name}!")

def upgradeHouse(player: p_def.Player, property: t_def.Tile) -> None:
    """
    Adds level to tile, sets new rent, and charges player
    :param player: Object of player
    :param property: Object of tile
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
    if player.balance >= property.upgradeCost:
        player.balance -= property.upgradeCost
        property.level += 1
        property.rent = getattr(property, f"l{property.level}")
        print(f"Upgraded {property.name} to level {property.level}!")
    else:
        print("You do not have sufficient funds!")

def clearTerminal() -> None:
    """
    Clears the terminal.
    :return: None
    """
    if name == "nt":
        system("cls")
    else:
        system("clear")