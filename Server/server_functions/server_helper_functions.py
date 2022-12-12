from Server import server_i


def printPlayers():
    usernames = []
    for player in server_i.players_connected.list:
        player_t = (player.username, player.address)
        usernames.append(player_t)
    return usernames


def printPlayersInQueue():
    usernames = []
    for player in server_i.game_queue:
        usernames.append(player.username)
    return usernames


def printPlayersInGame():
    usernames = []
    for player_sets in server_i.players_that_are_in_game:
        usernames.append((player_sets[0].username, player_sets[1].username))
    return usernames


def IsUsernameTaken(username):
    for player in server_i.players_connected.list:
        if player.username == username:
            return True
    return False


def giveFullTupleForInGame(player):
    for pair in server_i.players_that_are_in_game:
        if player in pair:
            return pair
    return None
