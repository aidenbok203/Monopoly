from classes import tile_definitions as t_def
from classes import player_definitions as p_def

board = []
playerList = []

def initialiseTiles() -> None:
    """
    Initialise tile properties from database
    :return: None
    """
    with open("db/tiles.txt", "r") as f:
        tiles = f.readlines()
        for tile in tiles:
            pos, name, cost, l0, l1, l2, l3 = tile.strip().split(",")
            pos = t_def.Tile(int(pos), name, int(cost), int(l0), int(l1), int(l2), int(l3))
            board.append(pos)

def intialisePlayers() -> None:
    """
    Allow user to create new players at the start of the game
    :return: None
    """
    startMoney = int(input("Enter amount of money to start with: "))
    for i in range(int(input("Input the number of players: "))):
        name = input(f"Enter player {i + 1} name: ")
        name = p_def.Player(i + 1, startMoney)
        playerList.append(name)

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