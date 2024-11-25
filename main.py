from game import init
from game import actions
from classes import player_definitions as p_def
from classes import tile_definitions as t_def

def round(player: p_def.Player) -> str:
    """
    Run at start of each turn, perform actions
    :param player: Object of player
    :return: str, Whether game is completed
    """
    rolled = False
    roundFinish = False
    while not roundFinish:
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
            case "p":
                prop = int(input("Enter the position of the property: "))
                for tile in init.board:
                    if tile.pos == prop:
                        print(tile)
            case "s":
                choice = int(input("Enter the position of the property you want to sell: "))
                for tile in player.owned:
                    if tile.pos == choice:
                        player.removeProperty(tile)
                        tile.sellTile()  # Reset the property
                        print(f"Sold {tile.name} for ${tile.cost}.")
                        break
                else:
                    print("You do not own this property!")
            case "l":
                choice = int(input("Enter the position of the property you want to sell: "))
                for tile in player.owned:
                    if tile.pos == choice:
                        actions.upgradeHouse(player, tile)


def main():
