from Server.player import Player


def printPlayers():
    print(list)


class players_connected:
    list: list[Player]

    def __init__(self):
        self.list = []
        self.amount = 0

    def addPlayer(self, player):
        self.list.append(player)
        self.amount += 1

    def removePlayer(self, player):
        self.list.remove(player)
        self.amount -= 1

    def changeUsername(self, new_username, address):
        for player in self.list:
            if player.address == address:
                player.username = new_username
