from classes import tile_definitions as t_def
from classes import player_definitions as p_def

board = []
playerList = []

# Load tiles.txt into classes in t_def
def initialiseTiles():
    with open("db/tiles.txt", "r") as f:
        tiles = f.readlines()
        for tile in tiles:
            pos, name, cost, l0, l1, l2, l3 = tile.strip().split(",")
            pos = t_def.Tile(int(pos), name, int(cost), int(l0), int(l1), int(l2), int(l3))
            board.append(pos)

# Load players into p_def
def intialisePlayers():
    startMoney = int(input("Enter amount of money to start with: "))
    for i in range(int(input("Input the number of players: "))):
        name = input(f"Enter player {i + 1} name: ")
        name = p_def.Player(i + 1, startMoney)
        playerList.append(name)