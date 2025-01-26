from game import init
from game import actions
from classes import player_definitions as p_def
from time import sleep

def round(player: p_def.Player) -> str:
    """
    Run at start of each turn, perform actions
    :param player: Object of player
    :return: str, Whether game is completed
    """
    rolled = False
    roundFinish = False
    print(f"It's {player.name}'s turn!")
    while not roundFinish:
        sleep(1)
        actions.clearTerminal()
        print(f"It's {player.name}'s turn!")
        init.displayMenu()
        action = input("What would you like to do? ")
        match action:
            case "r":
                if not rolled:
                    rolled = True
                    actions.roll(player)
                    if not actions.checkGameOver():
                        continue
                    else:
                        return "Game complete"
                else:
                    print("You have already rolled the dice! Choose another option.")
            case "b":
                print(f"Your balance is ${player.balance}.")
            case "o":
                for tile in player.owned:
                    print(tile)
                    input("Press enter to continue...")
            case "p":
                try:
                    prop = int(input("Enter the position of the property: "))
                    for tile in init.board:
                        if tile.pos == prop:
                            print(tile)
                            input("Press enter to continue...")
                except:
                    print("Invalid input.")
            case "s":
                try:
                    choice = int(input("Enter the position of the property you want to sell: "))
                    for tile in player.owned:
                        if tile.pos == choice:
                            if input(f"Confirm you would like to sell {tile.name} for ${tile.cost * 0.75}? (y/n) ").lower() == "y":
                                player.removeProperty(tile)
                                tile.sellTile()
                                print(f"Sold {tile.name} for ${tile.cost * 0.75}.")
                                break
                            else:
                                break
                    else:
                        print("You do not own this property!")
                except:
                    print("Invalid input!")
            case "l":
                for tile in player.owned:
                    if tile.pos == player.pos:
                        if input(f"Confirm you want to upgrade {tile.name} for ${tile.upgradeCost}? (y/n) ").lower():
                            actions.upgradeHouse(player, tile)
                            break
                else:
                    print("You do not own this property!")
            case "c":
                roundFinish = True
                print("Completing round...")
            case "g":
                print(actions.stateSave())
            case "f":
                if input("Enter \"y\" if you would like to exit the game: ") == "y":
                    print("Exiting game...")
                    sleep(2.5)
                    exit()
            case _:
                print("Invalid input.")

def main():
    init.initialiseTiles()
    init.initialiseCards()
    init.initialisePlayers()
    while not actions.checkGameOver():
        for player in init.playerList:
            round(player)
            winner = actions.checkGameOver()
            if winner:
                break
    if winner:
        print(f"{winner.name} has won the game with ${winner.balance}!")

if __name__ == "__main__":
    main()