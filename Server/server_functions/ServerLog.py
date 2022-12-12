from Server.server_functions.server_helper_functions import *


def ServerLog():
    while True:
        if len(server_i.players_that_just_disconnected) > 0:  # If a player disconnects, announce it
            player, Client_Abruptly_Closed = server_i.players_that_just_disconnected.pop(0)
            if Client_Abruptly_Closed:  # If the player abruptly closed the game
                print("A player has abruptly closed their game: ", end='')
            else:
                print("A player has closed their client: ", end='')
            print(str(player.username) + ", " + str(player.address))
            server_i.players_connected.removePlayer(player)  # Delete their username from the list
            if player in server_i.game_queue:  # If the player was in the queue, remove them from it
                server_i.game_queue.remove(player)
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_that_just_connected) > 0:  # If a new player connects, announce it
            new_player = server_i.players_that_just_connected.pop(0)
            print("A new player has joined: " + str(new_player.username) + ", " + str(new_player.address))
            server_i.players_connected.addPlayer(new_player)  # Add player to the list of current connected
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_changed_username) > 0:  # If a player changes their username, announce it
            old_username, changed_player = server_i.players_changed_username.pop(0)
            print(str(old_username) + ", " + str(changed_player.address) + " has a new username: " + str(changed_player.username) + ", " + str(changed_player.address))
            server_i.players_connected.changeUsername(changed_player.username, changed_player.address)  # Change username in the list of current connected
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_that_joined_queue) > 0:  # If a player joined the queue, announce it
            player_join_q = server_i.players_that_joined_queue.pop(0)
            print(player_join_q.username + " has entered the queue to find a match")
            server_i.game_queue.append(player_join_q)
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_that_left_queue) > 0:  # If a player left the queue, announce it
            player_left_q = server_i.players_that_left_queue.pop(0)
            print(player_left_q.username + " has left the queue to find a match")
            server_i.game_queue.remove(player_left_q)
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_left_during_game) > 0:  # If a player disconnects during a game, announce it
            player_left_g, opponent = server_i.players_left_during_game.pop(0)
            print(player_left_g.username + " has disconnected during his match against " + opponent.username)

            full_t = giveFullTupleForInGame(player_left_g)  # Delete the set of players from the list of current players that are in game
            if full_t in server_i.players_that_are_in_game:
                server_i.players_that_are_in_game.remove(full_t)

            server_i.players_connected.removePlayer(player_left_g)  # Delete their username from the list
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")

        if len(server_i.players_time_ran_out) > 0:  # If a player ran out of time during the match, announce it
            player_time_out_g, opponent, state = server_i.players_time_ran_out.pop(0)
            if state == 0:
                print(player_time_out_g.username + " ran out of time selecting ship locations. The match between " + player_time_out_g.username + " and " + opponent.username + " has ended")
                full_t = giveFullTupleForInGame(player_time_out_g)  # Delete the set of players from the list of current players that are in game
                if full_t is not None and full_t in server_i.players_that_are_in_game:
                    server_i.players_that_are_in_game.remove(full_t)
            if state == 1:
                print(player_time_out_g.username + " ran out of time selecting a move in Rock, Paper, Scissors. The player going first has been randomly selected")
            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")
        if len(server_i.players_finished_game) > 0:
            winner, loser = server_i.players_finished_game.pop(0)
            print(winner.username + " just won against " + loser.username + " in a match! Good game, players.")

            full_t = giveFullTupleForInGame(winner)  # Delete the set of players from the list of current players that are in game
            if full_t in server_i.players_that_are_in_game:
                server_i.players_that_are_in_game.remove(full_t)

            print("Players currently connected: ", printPlayers())
            print("Players in queue: ", printPlayersInQueue())
            print("Players currently in game: ", printPlayersInGame(), "\n")
