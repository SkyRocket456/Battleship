import pickle
import threading
from Server.player import Player
from Server import server_i
from Server.server_functions.Game_System import Game
from Server.server_functions.server_helper_functions import printPlayers,  printPlayersInQueue, printPlayersInGame

BarrierToClient = threading.Barrier(3, timeout=20)


def WaitToSendMessage(player, opponent):
    global BarrierToClient
    BarrierToClient.wait()  # Wait for both clients to send their messages at the same time
    player.conn.send(pickle.dumps(opponent.username))  # Send the client their opponent, indicating the match is about to begin
    server_i.player_client_thread_signal.append(player)  # Signal the Client Main Menu thread that they have found an opponent


def Queue():
    global BarrierToClient
    while True:
        if len(server_i.game_queue) > 1:

            # Take the first two players in the queue
            player1: Player = server_i.game_queue.pop(0)
            player2: Player = server_i.game_queue.pop(0)

            try:
                # Wait for both clients to receive the message at the same time so their countdown is synchronized
                p1_send_message = threading.Thread(target=WaitToSendMessage, args=(player1, player2))
                p1_send_message.start()
                p2_send_message = threading.Thread(target=WaitToSendMessage, args=(player2, player1))
                p2_send_message.start()

                if BarrierToClient.wait():  # If both players are ready, signal both WaitToSendMessage to send the message. it's game time!

                    print("A new match has begun! " + player1.username + " Vs " + player2.username + "!")

                    server_i.players_that_are_in_game.append((player1, player2))

                    newGame = threading.Thread(target=Game, args=(player1, player2))
                    newGame.start()

                    BarrierToClient.reset()  # Reset barrier

                    print("Players currently connected: ", printPlayers())
                    print("Players in queue: ", printPlayersInQueue())
                    print("Players currently in game: ", printPlayersInGame(), "\n")
            except:
                print("The Queue System had an unexpected error")
