from game import init
from game import actions
from classes import player_definitions as p_def

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
                

def main():
