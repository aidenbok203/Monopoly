from game import init
from game import actions
from classes import player_definitions as p_def

def round(player: p_def.Player) -> None:
    """
    Run at start of each turn, perform actions
    :param player: Object of player
    :return: None
    """
    rolled = False
    validate = False
    while not rolled and validate:
        init.displayMenu()
        action = input("What would you like to do? ")
        match action:
            case "r":
                actions.roll(player)

def main():
