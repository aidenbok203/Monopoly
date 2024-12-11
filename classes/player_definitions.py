from random import randint
from game import init
from classes import tile_definitions as t_def

class Player:
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name
        self.balance = balance
        self.pos = 0
        self.owned = []
        self.sameDice = 0
        self.jailed = False
        self.bankrupt = False

    def __str__(self):
        return f"Player id {self.id}, position: {self.pos}, balance: ${self.balance}"

    def rollDice(self) -> int:
        """
        Rolls a dice and moves the player
        :return: int, the current position of player
        """
        random = randint(1, 6)
        random2 = randint(1, 6)
        print(f"You rolled a {random} and {random2}!")
        if random == random2:
            self.sameDice += 1
            print(f"You have rolled the same number! It is your {self.sameDice} double!")
            if self.sameDice == 3:
                self.jailed = True
                self.sameDice = 0
                print("You are in jail!")
                return "jail"
        else:
            self.sameDice = 0
        self.pos += random + random2
        if self.pos > 22:
            self.pos -= 22
            input("You have passed go! Claim $200...")
            self.balance += 200
        return self.pos

    def jail(self) -> bool:
        """
        Rolls dice to get out of jail, or pay $50
        :param player: Object of player
        :return: bool, if user can get out of jail.
        """
        print("You are in jail.")
        match input("Would you like to roll the dice or pay $50? (r/p) "):
            case "r":
                random, random2 = randint(1,6), randint(1, 6)
                print(f"You have rolled {random} and {random2}.")
                if random == random2:
                    self.jailed = False
                    print("You have been released!")
                return
            case "p":
                match input("Confirm you would like to bail for $50? (y/n) "):
                    case "y":
                        self.balance -= 50
                        print("You have been released!")
                        self.jailed = False
                        return
                    case "n":
                        self.jail()
                    case _:
                        print("Invalid input.")
                        return

    def checkBankruptcy(self) -> bool:
        """
        Checks if a user is bankrupt
        :param player: Object of player
        :return: bool, If user is bankrupt
        """
        if self.balance < 0:
            self.bankrupt = True
            init.bankruptPlayers += 1
            return True
        else:
            return False

    def removeProperty(self, tile: t_def.Tile):
        """
        Remove property from player
        :param tile: Object of tile
        :return: None
        """
        if tile in self.owned:
            self.balance += tile.cost * 0.75
            self.owned.remove(tile)