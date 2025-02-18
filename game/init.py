from classes import card_definitions as c_def
from classes import tile_definitions as t_def
from classes import player_definitions as p_def
import os
import json
import sqlite3

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

# def path(relative_path) -> str:
#     """
#     Get the absolute path to the resource
#     :param relative_path: Path to the file
#     :return str: Absolute path to resource
#     """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     if getattr(sys, "frozen", False):
#         # Running in a bundled executable
#         abs_path = os.path.join(base_path, relative_path)
#     else:
#         # Running in a local env
#         base_path = os.path.dirname(os.path.abspath(__file__))
#         abs_path = os.path.join(base_path, f"../{relative_path}")
#     return abs_path

def initialiseCards() -> None:
    """
    Initialise community chest and chance cards from database
    :return: None
    """
    global chanceList, communityList
    with open("db/cards.json", "r") as f:
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
    conn = sqlite3.connect("db/data.db")
    cur = conn.cursor()
    cur.execute("SELECT pos, colour, name, cost, l1, l2, l3, l4, l5, upgradeCost, rent FROM tiles")
    rows = cur.fetchall()
    for row in rows:
        board.append(t_def.Tile(pos=row[0], colour=row[1], name=row[2], cost=row[3],
                                l1=row[4], l2=row[5], l3=row[6], l4=row[7], l5=row[8],
                                upgradeCost=row[9], rent=row[10]))
    conn.close()

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
    Save current state into db
    """
    conn = sqlite3.connect("db/data.db")
    cur = conn.cursor()
    # Player save
    cur.execute("DROP TABLE IF EXISTS playerSave")
    cur.execute("""CREATE TABLE playerSave (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50),
                balance INTEGER,
                pos INTEGER,
                sameDice INTEGER,
                jailed INTEGER,
                bankrupt INTEGER
                )""")
    for player in playerList:
        cur.execute("INSERT INTO playerSave (id, name, balance, pos, sameDice, jailed, bankrupt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (player.id, player.name, player.balance, player.pos, player.sameDice, player.jailed, player.bankrupt)
                    )
    # Tile save
    cur.execute("DROP TABLE IF EXISTS tileSave")
    cur.execute("""CREATE TABLE tileSave (
                pos INTEGER PRIMARY KEY,
                rent INTEGER,
                level INTEGER,
                owned INTEGER
    )""")
    for tile in board:
        cur.execute("INSERT INTO tileSave (pos, rent, level, owned) VALUES (?, ?, ?, ?)",
                    (tile.pos, tile.rent, tile.level, tile.owned)
                    )
    conn.commit()
    conn.close()

def loadGame() -> None:
    """
    Loads game from db
    """
    global bankruptLimit, bankruptPlayers, playerNum
    playerNum, bankruptPlayers = 0, 0
    conn = sqlite3.connect("db/data.db")
    cur = conn.cursor()

    # Player data
    cur.execute("SELECT id, name, balance, pos, sameDice, jailed, bankrupt FROM playerSave")
    rows = cur.fetchall()
    for row in rows:
        playerList.append(p_def.Player(id=row[0], name=row[1], balance=row[2], sameDice=bool(row[3]), jailed=bool(row[4]), bankrupt=bool(row[5])))
        playerNum += 1
    bankruptLimit = playerNum - 1

    # Tile data
    cur.execute("SELECT pos, rent, level, owned FROM tileSave")
    tileSave = cur.fetchall()
    cur.execute("SELECT colour, name, cost, l1, l2, l3, l4, l5, upgradeCost FROM tiles")
    tiles = cur.fetchall()
    for save, data in zip(tileSave, tiles):
        board.append(t_def.Tile(pos=save[0], colour=data[0], name=data[1], cost=data[2], l1=data[3], l2=data[4], l3=data[5], l4=data[6], l5=data[7], upgradeCost=data[8], rent=save[1], level=save[2], owned=save[3]))
    conn.close()

    for tile in board:
        if tile.owned is None:
            continue
        for player in playerList:
            if player.id != tile.owned:
                continue
            player.owned.append(tile)
    initialiseCards()

def checkLoad() -> bool:
    """
    Checks if user wants to load savefile
    :return bool: Returns if user wants to load save
    """
    if os.path.exists("db/save.json"):
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
    print("Close game...................f")