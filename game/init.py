from classes import tile_definitions as t_def
from classes import player_definitions as p_def
import os
import sys

board = []
playerList = []

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def initialiseTiles() -> None:
    """
    Initialise tile properties from database
    :return: None
    """
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
        tiles_path = os.path.join(base_path, 'db', 'tiles.txt')
    else:
        tiles_path = resource_path("db/tiles.txt")
    with open(tiles_path, "r") as f:
        tiles = f.readlines()
        for tile in tiles:
            pos, name, cost, l1, l2, l3, l4, l5, upgradeCost = tile.strip().split(",")
            pos = t_def.Tile(int(pos), name, int(cost), int(l1), int(l2), int(l3), int(l4), int(l5), int(upgradeCost), int(l1))
            board.append(pos)

def intialisePlayers() -> None:
    """
    Allow user to create new players at the start of the game
    :return: None
    """
    validate = False
    while not validate:
        try:
            startMoney = int(input("Enter amount of money to start with: "))
            playerNum = int(input("Input the number of players: "))
            if playerNum == 1:
                print("You need at least 2 players!")
                continue
            validate = True
        except:
            print("Invalid input!")
    global bankruptLimit
    bankruptLimit = playerNum - 1
    global bankruptPlayers
    bankruptPlayers = 0
    for i in range(playerNum):
        name = input(f"Enter player {i + 1} name: ")
        playerList.append(p_def.Player(i + 1, name, startMoney))

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
