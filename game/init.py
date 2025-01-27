from classes import card_definitions as c_def
from classes import tile_definitions as t_def
from classes import player_definitions as p_def
import os
import sys
import json

board = []
playerList = []
chanceList = []
communityList = []

setLimit = {
    "Brown": 2,
    "Teal": 3,
    "Pink": 3,
    "Orange": 3,
    "Red": 3,
    "Yellow": 3,
    "Green": 3,
    "Blue": 2
}

def path(relative_path) -> str:
    """
    Get the absolute path to the resource
    :param relative_path: Path to the file
    :return str: Absolute path to resource
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    if getattr(sys, "frozen", False):
        # Running in a bundled executable
        abs_path = os.path.join(base_path, relative_path)
    else:
        # Running in a local env
        base_path = os.path.dirname(os.path.abspath(__file__))
        abs_path = os.path.join(base_path, f"../{relative_path}")
    return abs_path

def initialiseCards() -> None:
    """
    Initialise community chest and chance cards from database
    :return: None
    """
    global chanceList, communityList
    with open(path("db/cards.json"), "r") as f:
        data = json.load(f)
    chanceList = [
        c_def.Card(card["name"], card["functions"])
        for card in data["chance"]
    ]
    communityList = [
        c_def.Card(card["name"], card["functions"])
        for card in data["community"]
    ]
    return chanceList, communityList

def initialiseTiles() -> None:
    """
    Initialise tile properties from database
    :return: None
    """
    with open(path("db/tiles.txt"), "r") as f:
        tiles = f.readlines()
        for tile in tiles:
            pos, group, name, cost, l1, l2, l3, l4, l5, upgradeCost = tile.strip().split(",")
            pos = t_def.Tile(int(pos), group, name, int(cost), int(l1), int(l2), int(l3), int(l4), int(l5), int(upgradeCost), int(l1))
            board.append(pos)

def initialisePlayers() -> None:
    """
    Allow user to create new players at the start of the game
    :return: None
    """
    validate = False
    while not validate:
        try:
            global playerNum
            startMoney = int(input("Enter amount of money to start with: "))
            playerNum = int(input("Input the number of players: "))
            if playerNum == 1:
                print("You need at least 2 players!")
                continue
            validate = True
        except Exception:
            print("Invalid input!")
    global bankruptLimit
    bankruptLimit = playerNum - 1
    global bankruptPlayers
    bankruptPlayers = 0
    for i in range(playerNum):
        name = input(f"Enter player {i + 1} name: ")
        playerList.append(p_def.Player(i + 1, name, startMoney))

def stateSave() -> None:
    """
    Writes current variables into json file
    """
    try:
        players = [player.dictForm() for player in playerList]
        tiles = [tile.dictForm() for tile in board]
        chances = [chance.dictForm() for chance in chanceList]
        communitys = [community.dictForm() for community in communityList]
        data = {
            "players": players,
            "tiles": tiles,
            "chance": chances,
            "community": communitys
        }
        with open(path("db/save.json"), "w") as f:
            json.dump(data, f, indent = 4)
            return "Game saved!"
    except Exception as e:
        return f"Error occured: {e}"

def loadGame() -> None:
    """
    Loads game from save.json
    """
    global bankruptPlayers, bankruptLimit
    bankruptPlayers = 0
    bankruptLimit = 0
    with open(path("db/save.json"), "r") as f:
        data = json.load(f)
        for playerData in data["players"]:
            playerList.append(p_def.Player(
                playerData["id"],
                playerData["name"],
                playerData["balance"],
                playerData["pos"],
                playerData["owned"],
                playerData["sameDice"],
                playerData["jailed"],
                playerData["bankrupt"]
            ))
            bankruptLimit += 1

def checkLoad() -> bool:
    """
    Checks if user wants to load savefile
    :return bool: Returns if user wants to load save
    """
    if os.path.exists(path("db/save.json")):
        if input("Would you like to load previous save? (y/n) ") == "y":
            try:
                loadGame()
                print("Loaded save!")
                return True
            except Exception as e:
                print(f"Error occured: {e}")
        return False
    return False

def displayMenu() -> None:
    """
    Displays available actions to player
    :return: None
    """
    print("Roll dice....................r")
    print("Display balance..............b")
    print("Display owned properties.....o")
    print("Display specific property....p")
    print("Sell property................s")
    print("Upgrade property.............l")
    print("Complete turn................c")
    print("Save game....................g")
    print("Close game...................f")