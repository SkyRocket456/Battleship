import threading

from Server.player import GamePlayer, Player
from info.Codes import *
import pickle
import socket
from Server.server_functions.server_helper_functions import *


# The thread does two things:
# 1. Monitors what happens to the client during the countdowns.
# 2. Waits for both players to send confirmation that they have each selected their ship locations. Either the client closes the game, the opponent disconnects, or
# the client sends their GamePlayer back, indicating that they have confirmed their ship locations
# 3. Receives guesses (coordinates) from the client and checks if they hit a ship from the opponent's side
def Client_In_Game(player, opponent, p_n, o_n, Information_Q: list[GamePlayer], RPS_Moves, Battleship_Winner):
    Close = False
    player.conn.settimeout(0.1)
    while True:
        new_data = []
        data = None
        while True:
            try:
                packet = player.conn.recv(4096)
                new_data.append(packet)
            except socket.timeout:
                break
            except Exception as e:  # If any lethal errors occur,
                print(e)
                Close = True
                Information_Q[p_n] = GAME_CLOSED
                try:
                    opponent.conn.send(pickle.dumps(OPPONENT_DISCONNECTED))
                except:
                    pass
                if player in server_i.players_connected.list:
                    server_i.players_left_during_game.append((player, opponent))  # Notify the log that the player left
                player.conn.close()  # Close the connection
                break
        if Close:
            break
        if new_data:
            data = pickle.loads(b"".join(new_data))  # Receive message from client that they are done choosing ship locations, or...
        if data == IN_GAME:  # If the client is beyond countdown, send them the game object
            player.conn.send(pickle.dumps(p_n + 1))
        if isinstance(data, GamePlayer):  # CONFIRMATION that the player has confirmed their ship locations
            opponent.conn.send(pickle.dumps(OPPONENT_DONE_CHOOSING_LOCATIONS))
            Information_Q[p_n] = data
        if data == SELECTED_ROCK or data == SELECTED_PAPER or data == SELECTED_SCISSORS:  # If the client selected a move in RPS, save it
            RPS_Moves[p_n] = data
            opponent.conn.send(pickle.dumps(data))
        if isinstance(data, tuple):  # Client sends back coordinates, their guess as to where they think the enemy's ship is.
            asker_result, asked_result = Information_Q[o_n].WasShipHit(data)
            player.conn.send(pickle.dumps((asker_result, data)))
            opponent.conn.send(pickle.dumps((asked_result, data)))
        if data == TIME_RAN_OUT_ShipLoc:  # If the countdown ran out, end the thread
            Information_Q[p_n] = data
            server_i.players_time_ran_out.append((player, opponent, 0))
            BACK_to_Client_Main_Menu = threading.Thread(target=Client_In_Main_Menu, args=[player])
            BACK_to_Client_Main_Menu.start()
            break
        if data == TIME_RAN_OUT_RPS:
            RPS_Moves[p_n] = data
        if data == GAME_CLOSED:  # If they closed the game, message the other player, and make a note of it in the Log
            Information_Q[p_n] = GAME_CLOSED
            opponent.conn.send(pickle.dumps(OPPONENT_DISCONNECTED))
            if player in server_i.players_connected.list:
                server_i.players_left_during_game.append((player, opponent))  # Notify the log that the player left
            player.conn.close()  # Close the connection
            break
        if Information_Q[o_n] == GAME_CLOSED:  # If the opponent closed their game, break out of this thread
            Information_Q[p_n] = BACK_TO_MAIN_MENU
            BACK_to_Client_Main_Menu = threading.Thread(target=Client_In_Main_Menu, args=[player])
            BACK_to_Client_Main_Menu.start()
            break
        if Battleship_Winner[0] is not None:
            player.conn.send(pickle.dumps(Battleship_Winner[0]))
            BACK_to_Client_Main_Menu = threading.Thread(target=Client_In_Main_Menu, args=[player])
            BACK_to_Client_Main_Menu.start()
            break


def Client_In_Main_Menu(this_player: Player):
    Client_Abruptly_Closed = False
    Main_Menu = True
    Now_In_Game = False
    try:
        this_player.conn.settimeout(0.1)
    except:  # Return if connection could not be timed out
        Main_Menu = False
        if this_player not in server_i.players_that_just_disconnected:
            server_i.players_that_just_disconnected.append((this_player, True))  # Notify the log that the player left
    while Main_Menu:  # Keep looping while the client is in the main menu
        try:
            data = pickle.loads((this_player.conn.recv(2048)))  # Receive data from the client
            # If the client wants to find a match, add them to the queue
            if data == LOOKING_FOR_GAME:
                if this_player not in server_i.game_queue:  # If the player isn't in the queue when they are finding a match, add them to the queue
                    server_i.players_that_joined_queue.append(this_player)  # Notify the log that the player joined
            else:
                if data == LEFT_QUEUE:  # If the client is closed, break off the thread
                    if this_player in server_i.game_queue:
                        server_i.players_that_left_queue.append(this_player)  # Notify the log that the player left
                if data == GAME_CLOSED:
                    break
        except socket.timeout:
            pass
            if this_player in server_i.player_client_thread_signal:  # If the player is in the list to signal a player when they found a game, it's game time!
                server_i.player_client_thread_signal.remove(this_player)
                Now_In_Game = True
                break
        except:  # If the client abruptly closed
            Client_Abruptly_Closed = True
            break
    if Main_Menu and not Now_In_Game:
        if this_player in server_i.player_client_thread_signal:  # If the player was is in the list to signal a player when they found a game, remove them
            server_i.player_client_thread_signal.remove(this_player)
        if this_player not in server_i.players_that_just_disconnected:
            server_i.players_that_just_disconnected.append((this_player, Client_Abruptly_Closed))  # Notify the log that the player left
        this_player.conn.close()  # Close the connection


def Client_In_Username_Screen(conn, address):  # conn means connection
    this_player = Player(None, conn, address)  # Define the player with no username
    server_i.players_that_just_connected.append(this_player)  # Add players to the list of currently connected
    while True:  # Keep looping while the client is in the username screen
        try:
            username = pickle.loads(conn.recv(2048))  # Receive username from the client
            if username == GAME_CLOSED:  # If the client has closed the game, end the thread3
                server_i.players_that_just_disconnected.append((this_player, False))  # Notify the log that the player left
                break
            elif IsUsernameTaken(username):  # If the username is already taken, it is invalid
                conn.send(pickle.dumps(USERNAME_TAKEN))
            else:  # If the username is valid,
                conn.send(pickle.dumps(VALID_USERNAME))  # Send a message to the client saying the username was valid
                old_username = this_player.username  # Save the old username
                this_player.username = username  # Save the new username
                server_i.players_changed_username.append((str(old_username), this_player))  # Change the username in the server database for the log
                To_Client_Main_Menu = threading.Thread(target=Client_In_Main_Menu, args=[this_player])
                To_Client_Main_Menu.start()
                break
        except:  # If the client abruptly closed
            # This code is executed when the client closes the game window
            # The "True" Condition checks if client had an error when closing
            server_i.players_that_just_disconnected.append((this_player, True))  # Notify the log that the player left
            conn.close()  # Close the connection
            break
