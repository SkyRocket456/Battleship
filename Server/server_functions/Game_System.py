import pickle
import threading
from random import randint
from Server.player import Player, GamePlayer
from Server import server_i
from info.Codes import *
from Server.server_functions.server_client_threads import Client_In_Game


def sendData(player1, player2, Information_Q, data):  # Send data to both clients. If any of them close their game, notify the Game
    try:
        player1.conn.send(pickle.dumps(data))
    except:
        Information_Q[0] = GAME_CLOSED
        Information_Q[1] = BACK_TO_MAIN_MENU
    try:
        player2.conn.send(pickle.dumps(data))
    except:
        Information_Q[0] = BACK_TO_MAIN_MENU
        Information_Q[1] = GAME_CLOSED


def Game(player1: Player, player2: Player):
    Information_Q = [None, None]  # List that exists to confirm that ship locations are secured for both players
    RPS_Moves = [None, None]  # The moves for Rock, Paper, Scissors
    RPS_Winner = None  # The winner of Rock, Paper, Scissors. Defaulted to
    Rock_Paper_Scissors = True  # If playing Rock, Paper, Scissors is valid
    Battleship_Winner = [None]  # The winner

    Game_Thread_1 = threading.Thread(target=Client_In_Game, args=(player1, player2, 0, 1, Information_Q, RPS_Moves, Battleship_Winner))
    Game_Thread_1.start()

    Game_Thread_2 = threading.Thread(target=Client_In_Game, args=(player2, player1, 1, 0, Information_Q, RPS_Moves, Battleship_Winner))
    Game_Thread_2.start()

    # This while loop does multiple things:
    # 1. While both players' confirmation are not sent yet, check to see if any player has disconnected
    # 2. Check to see if the timer ran out for the countdown for both the ship locations and RPS
    # 3. Checks to see who won in RPS. If there is a winner, that player goes first and Battleship begins!
    while True:
        if isinstance(Information_Q[0], GamePlayer) and isinstance(Information_Q[1], GamePlayer):
            # Check to see if somebody won
            if not Information_Q[0].AreAllShipsDown() and Information_Q[1].AreAllShipsDown():
                Battleship_Winner[0] = 1
                server_i.players_finished_game.append((player1, player2))
                break
            if Information_Q[0].AreAllShipsDown() and not Information_Q[1].AreAllShipsDown():
                Battleship_Winner[0] = 2
                server_i.players_finished_game.append((player2, player1))
                break
        if Information_Q[0] == GAME_CLOSED and Information_Q[1] == BACK_TO_MAIN_MENU:
            break
        if Information_Q[1] == GAME_CLOSED and Information_Q[0] == BACK_TO_MAIN_MENU:
            break
        if Information_Q[0] == TIME_RAN_OUT_ShipLoc or Information_Q[1] == TIME_RAN_OUT_ShipLoc:
            break
        if Rock_Paper_Scissors:
            if RPS_Moves[0] is not None and RPS_Moves[0] != TIME_RAN_OUT_RPS and RPS_Moves[1] is not None and RPS_Moves[1] != TIME_RAN_OUT_RPS:  # Find who won in the RPS game
                if RPS_Moves[0] == RPS_Moves[1]:
                    RPS_Winner = RPS_TIE_GAME
                elif RPS_Moves[0] == SELECTED_PAPER:
                    if RPS_Moves[1] == SELECTED_SCISSORS:
                        RPS_Winner = 2
                    elif RPS_Moves[1] == SELECTED_ROCK:
                        RPS_Winner = 1
                elif RPS_Moves[0] == SELECTED_ROCK:
                    if RPS_Moves[1] == SELECTED_SCISSORS:
                        RPS_Winner = 1
                    elif RPS_Moves[1] == SELECTED_PAPER:
                        RPS_Winner = 2
                elif RPS_Moves[0] == SELECTED_SCISSORS:
                    if RPS_Moves[1] == SELECTED_ROCK:
                        RPS_Winner = 2
                    elif RPS_Moves[1] == SELECTED_PAPER:
                        RPS_Winner = 1
                sendData(player1, player2, Information_Q, RPS_Winner)
                if RPS_Winner == RPS_TIE_GAME:
                    RPS_Moves[0] = None
                    RPS_Moves[1] = None
                else:
                    Rock_Paper_Scissors = False
            if RPS_Moves[0] == TIME_RAN_OUT_RPS and RPS_Moves[1] != TIME_RAN_OUT_RPS:
                RPS_Winner = 2
                sendData(player1, player2, Information_Q, RPS_Winner)
                Rock_Paper_Scissors = False
            elif RPS_Moves[0] != TIME_RAN_OUT_RPS and RPS_Moves[1] == TIME_RAN_OUT_RPS:
                RPS_Winner = 1
                sendData(player1, player2, Information_Q, RPS_Winner)
                Rock_Paper_Scissors = False
            elif RPS_Moves[0] == TIME_RAN_OUT_RPS and RPS_Moves[1] == TIME_RAN_OUT_RPS:
                player_n = randint(1, 2)
                if player_n == 1:
                    RPS_Winner = 1
                else:
                    RPS_Winner = 2
                sendData(player1, player2, Information_Q, RPS_Winner)
                Rock_Paper_Scissors = False
