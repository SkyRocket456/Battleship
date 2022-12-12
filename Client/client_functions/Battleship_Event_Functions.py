from Client.client_functions.Battlehip_Window_Functions import *
from Client.helper_functions import *
from info.Codes import *

RPS_Did_Player_Make_Move = False
RPS_Did_Opponent_Make_Move = False

Player_Move_RPS = None
Opponent_Move_RPS = None

Turn_Chose_Location = False


def checkGameTurnEvents(player: GamePlayer, Is_Turn):
    global Turn_Chose_Location
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED
        if event.type == pygame.MOUSEBUTTONDOWN and Is_Turn:
            cell = player.WhatCellWasClicked(pygame.mouse.get_pos())
            if cell is not None and not Turn_Chose_Location:
                n.SendData((cell.j, cell.i))
                Turn_Chose_Location = True


def checkRPSEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if ROCK_BUTTON.click(pos) and not Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move:
                n.SendData(SELECTED_ROCK)
                Client.client_functions.Battleship_Event_Functions.Player_Move_RPS = "Rock"
                Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move = True
            if PAPER_BUTTON.click(pos) and not Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move:
                n.SendData(SELECTED_PAPER)
                Client.client_functions.Battleship_Event_Functions.Player_Move_RPS = "Paper"
                Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move = True
            if SCISSORS_BUTTON.click(pos) and not Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move:
                n.SendData(SELECTED_SCISSORS)
                Client.client_functions.Battleship_Event_Functions.Player_Move_RPS = "Scissors"
                Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move = True


def checkIfGameClosedEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the window is closed, send a message to the server that the client is gone
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED


def checkChoosingSpotsEvents(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the window is closed, send a message to the server that the client is gone
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED
        if event.type == pygame.MOUSEBUTTONDOWN:  # The conditions for the ship buttons
            pos = pygame.mouse.get_pos()
            if CarrierButton.click(pos) and not player.are_spots_chosen:
                player.ClickedCarrier()
            if BattleshipButton.click(pos) and not player.are_spots_chosen:
                player.ClickedBattleship()
            if CruiserButton.click(pos) and not player.are_spots_chosen:
                player.ClickedCruiser()
            if SubmarineButton.click(pos) and not player.are_spots_chosen:
                player.ClickedSubmarine()
            if DestroyerButton.click(pos) and not player.are_spots_chosen:
                player.ClickedDestroyer()
            player.ClickedGridShipLoc(pos)
            if DoneButton.click(pos) and player.isDoneValid():
                player.are_spots_chosen = True
                n.SendData(player)
    return None
