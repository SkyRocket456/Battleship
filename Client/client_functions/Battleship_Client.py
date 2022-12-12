import threading
from Client.client_functions.Battleship_Event_Functions import *
from info.Codes import *
from Client.classes.cell import Cell
import Client.client_functions.Battleship_Event_Functions
import Client.client_functions.Battleship_Helper_Functions

Time_Is_Up_List = []
Stop_Timer = []


def Battleship():
    global Time_Is_Up_List, Stop_Timer

    # Reset game parameters
    Client.client_functions.Battleship_Helper_Functions.Opponent_Carrier_Alive = True
    Client.client_functions.Battleship_Helper_Functions.Opponent_Battleship_Alive = True
    Client.client_functions.Battleship_Helper_Functions.Opponent_Cruiser_Alive = True
    Client.client_functions.Battleship_Helper_Functions.Opponent_Submarine_Alive = True
    Client.client_functions.Battleship_Helper_Functions.Opponent_Destroyer_Alive = True

    Client.client_functions.Battleship_Event_Functions.Player_Move_RPS = None
    Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS = None
    Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move = False
    Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move = False

    Client.client_functions.Battleship_Event_Functions.Turn_Chose_Location = False

    clock = pygame.time.Clock()
    this_player = GamePlayer(client_i.username)
    opponent = GamePlayer(client_i.opponent_username)
    player_n = n.SendAndReceive(IN_GAME)  # Receive the game from the server

    grid = [[None for x in range(10)] for y in range(10)]  # Initialize 2d array for ships_grid on the screen
    for j, y in zip(range(10), range(210, 800, 59)):  # Creates cells on the ships_grid and adds them to the player's object
        for i, x in zip(range(10), range(380, 980, 60)):
            Grid_Cell = Cell(x, y, BLUE, 60, 59, j, i)
            grid[j][i] = Grid_Cell

    this_player.ships_grid = grid  # New ships_grid

    g_grid = [[None for x in range(10)] for y in range(10)]  # Initialize 2d array for guessing grid on the screen
    for j, y in zip(range(10), range(210, 800, 59)):  # Creates cells on the guessing grid and adds them to the player's object
        for i, x in zip(range(10), range(380, 980, 60)):
            Grid_Cell = Cell(x, y, BLUE, 60, 59, j, i)
            g_grid[j][i] = Grid_Cell

    this_player.guessing_grid = g_grid

    # Start the timer for choosing ship locations
    countdown_ShipLoc = threading.Thread(target=Countdown, args=([60]))
    countdown_ShipLoc.start()
    # Keep looping until
    # 1. Both players have selected their ship locations
    # 2. The timer runs out
    while not this_player.are_spots_chosen or not opponent.are_spots_chosen:
        data = n.ReceiveData()  # Continually check for data from the server
        # If the opponent is done choosing their ship locations, update this client's window
        if data == OPPONENT_DONE_CHOOSING_LOCATIONS:
            opponent.are_spots_chosen = True
        run = checkChoosingSpotsEvents(this_player)
        # If the player closed the client, stop the timer and end the program
        if run == GAME_CLOSED:
            Stop_Timer.append(True)
            return run
        # If the opponent disconnected and this client hasn't closed their game, stop the timer and update this client's window with that information. Return to the main menu after
        if data == OPPONENT_DISCONNECTED:
            Stop_Timer.append(True)
            for i in range(5, 0 - 1, -1):
                updateTopInfoWindow()
                UpdateWindowChoosingLocations(this_player, opponent, True, i, False)
                pygame.display.update()
                pygame.time.delay(1000)
                run = checkIfGameClosedEvents()
                if run == GAME_CLOSED:  # If the player closes the screen while in countdown
                    return GAME_CLOSED
            return OPPONENT_DISCONNECTED
        if len(Time_Is_Up_List) > 0:  # If the timer reached 0
            if not this_player.are_spots_chosen:
                n.SendData(TIME_RAN_OUT_ShipLoc)  # If the player didn't choose fast enough, send a message to the server
            for i in range(5, 0 - 1, -1):
                updateTopInfoWindow()
                UpdateWindowChoosingLocations(this_player, opponent, False, i, True)
                pygame.display.update()
                pygame.time.delay(1000)
                run = checkIfGameClosedEvents()
                if run == GAME_CLOSED:  # If the player closes the screen while in countdown
                    return GAME_CLOSED
            return BACK_TO_MAIN_MENU
        updateTopInfoWindow()
        UpdateWindowChoosingLocations(this_player, opponent, False, None, False)
        pygame.display.update()
        clock.tick(60)

    waitForCountdownToEnd()
    count_RPS = threading.Thread(target=Countdown, args=[15])
    count_RPS.start()
    while True:  # Rock Paper Scissors to decide who goes first
        updateTopInfoWindow()
        data = n.ReceiveData()  # Continually check for data from the server
        # If the opponent made a move, document it and update the client's window
        if data == SELECTED_ROCK or data == SELECTED_PAPER or data == SELECTED_SCISSORS:
            Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move = True
            if data == SELECTED_ROCK:
                Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS = "Rock"
            if data == SELECTED_PAPER:
                Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS = "Paper"
            if data == SELECTED_SCISSORS:
                Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS = "Scissors"
            updateRPSWindow(Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move, Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move, False, None, False, None)
        # If the game was a tie, update the client's window and reset
        elif data == RPS_TIE_GAME:
            updateRPSWindow(Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move, Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move, True, None, False, None)
            pygame.display.update()
            pygame.time.delay(2000)
            ResetRPS()
        # If there was a RPS Winner, see who goes first
        elif isinstance(data, int):
            if data == player_n:
                RPS_Winner = client_i.username
                Is_It_My_Turn = True
            else:
                RPS_Winner = opponent.username
                Is_It_My_Turn = False
            updateRPSWindow(Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move, Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move, False, RPS_Winner, False, None)
            pygame.display.update()
            pygame.time.delay(2000)
            break
        elif data == OPPONENT_DISCONNECTED:
            Stop_Timer.append(True)
            for i in range(5, 0 - 1, -1):
                updateTopInfoWindow()
                updateRPSWindow(Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move, Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move, False, None, True, i)
                pygame.display.update()
                pygame.time.delay(1000)
                run = checkIfGameClosedEvents()
                if run == GAME_CLOSED:  # If the player closes the screen while in countdown
                    return GAME_CLOSED
            return OPPONENT_DISCONNECTED
        run = checkRPSEvents()
        if run == GAME_CLOSED:  # If the player closed the client, stop the timer and end the program
            Stop_Timer.append(True)
            return GAME_CLOSED
        if len(Time_Is_Up_List) > 0:  # If the timer reached , tell the server
            if Client.client_functions.Battleship_Event_Functions.Player_Move_RPS is None:
                n.SendData(TIME_RAN_OUT_RPS)
        updateRPSWindow(Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move, Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move, False, None, False, None)
        pygame.display.update()
        clock.tick(60)

    while True:  # The turn system
        data = n.ReceiveData()  # Continually check for data from the server
        updateTopInfoWindow()
        # If client hit a ship, update game window and change grid
        if isinstance(data, tuple):
            if data[0] == HIT:
                this_player.ChangeCellColorGuesserGrid(data[1], Hit_Cell_Color)
                updateGameTurnWindow(this_player, Is_It_My_Turn, True, None, None, False, None, None)
                Client.client_functions.Battleship_Event_Functions.Turn_Chose_Location = False
                pygame.display.update()
                pygame.time.delay(2000)
            # If client missed the opponent's ships, update game window and change grid
            elif data[0] == MISS:
                if Is_It_My_Turn:
                    this_player.ChangeCellColorGuesserGrid(data[1], Missed_Cell_Color)
                else:
                    this_player.ChangeCellColorShipsGrid(data[1], Missed_Cell_Color)
                updateGameTurnWindow(this_player, Is_It_My_Turn, False, None, None, True, None, None)
                Client.client_functions.Battleship_Event_Functions.Turn_Chose_Location = False
                pygame.display.update()
                pygame.time.delay(2000)
            elif data[0] == HIT_CARRIER or data[0] == HIT_BATTLESHIP or data[0] == HIT_CRUISER or data[0] == HIT_SUBMARINE or data[0] == HIT_DESTROYER:
                this_player.ChangeCellColorShipsGrid(data[1], Hit_Cell_Color)
                Client.client_functions.Battleship_Event_Functions.Turn_Chose_Location = False
                updateGameTurnWindow(this_player, Is_It_My_Turn, False, data[0], None, False, None, None)
                pygame.display.update()
                pygame.time.delay(2000)
            elif data[0] == SUNK_CARRIER or data[0] == SUNK_BATTLESHIP or data[0] == SUNK_CRUISER or data[0] == SUNK_SUBMARINE or data[0] == SUNK_DESTROYER:
                if Is_It_My_Turn:
                    this_player.ChangeCellColorGuesserGrid(data[1], Hit_Cell_Color)
                else:
                    this_player.ChangeCellColorShipsGrid(data[1], Hit_Cell_Color)
                Client.client_functions.Battleship_Event_Functions.Turn_Chose_Location = False
                updateGameTurnWindow(this_player, Is_It_My_Turn, False, None, data[0], False, None, None)
                pygame.display.update()
                pygame.time.delay(2000)
            Is_It_My_Turn = not Is_It_My_Turn
        elif isinstance(data, int):
            if data == player_n:
                Winner = client_i.username
            else:
                Winner = opponent.username
            for i in range(10, 0 - 1, -1):
                updateGameTurnWindow(this_player, Is_It_My_Turn, False, None, None, False, Winner, i)
                pygame.display.update()
                pygame.time.delay(1000)
                run = checkIfGameClosedEvents()
                if run == GAME_CLOSED:  # If the player closes the screen while in countdown
                    return GAME_CLOSED
            return BACK_TO_MAIN_MENU
        else:
            updateGameTurnWindow(this_player, Is_It_My_Turn, False, None, None, False, None, None)
            pygame.display.update()
        run = checkGameTurnEvents(this_player, Is_It_My_Turn)
        if run == GAME_CLOSED:  # If the player closes the client
            return GAME_CLOSED
