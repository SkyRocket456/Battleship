from Client.classes.button import TextButton
from Client.client_functions.Battleship_Helper_Functions import *
from Client.helper_functions import *
from info.Codes import *
from info.colors import *
from Client.client_i import *
import Client.client_functions.Battleship_Helper_Functions

Count_Array = []

carrier_text = createTextSys("comicsans", 40, "Carrier", WHITE)
CarrierButton = TextButton(carrier_text, 160 - 100, 579 - 198, GREY, 200, 75)

battleship_text = createTextSys("comicsans", 40, "Battleship", WHITE)
BattleshipButton = TextButton(battleship_text, 160 - 100, 579 - 118, GREY, 200, 75)

cruiser_text = createTextSys("comicsans", 40, "Cruiser", WHITE)
CruiserButton = TextButton(cruiser_text, 160 - 100, 579 - 38, GREY, 200, 76)

submarine_text = createTextSys("comicsans", 40, "Submarine", WHITE)
SubmarineButton = TextButton(submarine_text, 160 - 100, 579 + 42, GREY, 200, 75)

destroyer_text = createTextSys("comicsans", 40, "Destroyer", WHITE)
DestroyerButton = TextButton(destroyer_text, 160 - 100, 579 + 122, GREY, 200, 75)

ShipsButtons = [CarrierButton, BattleshipButton, CruiserButton, SubmarineButton, DestroyerButton]

done_text = createTextSys("comicsans", 40, "DONE", WHITE)
DoneButton = TextButton(done_text, 980 + 160 - 75, 579 - 75, GREY, 150, 75)

ROCK = createTextSys("comicsans", 40, "Rock", WHITE)
ROCK_BUTTON = TextButton(ROCK, 660 - 75 - 200, 500, BLACK, 150, 100)

PAPER = createTextSys("comicsans", 40, "Paper", WHITE)
PAPER_BUTTON = TextButton(PAPER, 660 - 75, 500, RED, 150, 100)

SCISSORS = createTextSys("comicsans", 40, "Scissors", WHITE)
SCISSORS_BUTTON = TextButton(SCISSORS, 660 - 75 + 200, 500, GREEN, 150, 100)


# Window that decides what pops up on the screen during the turns of the game
def updateGameTurnWindow(player: GamePlayer, your_turn, you_hit_ship, ship_was_hit, ship_was_sunk, shot_missed, winner, i):
    if winner is None:
        if your_turn:
            player.DrawGuessingGrid(window)
        else:
            player.DrawShipsGrid(window)
        DrawCoordinates()

        if you_hit_ship:
            DrawHitAShip()
        elif ship_was_hit is not None:
            if ship_was_hit == HIT_CARRIER:
                hit_ship = "Carrier"
            elif ship_was_hit == HIT_BATTLESHIP:
                hit_ship = "Battleship"
            elif ship_was_hit == HIT_CRUISER:
                hit_ship = "Cruiser"
            elif ship_was_hit == HIT_SUBMARINE:
                hit_ship = "Submarine"
            elif ship_was_hit == HIT_DESTROYER:
                hit_ship = "Destroyer"
            DrawShipWasHit(hit_ship)
        elif ship_was_sunk is not None:
            if ship_was_sunk == SUNK_CARRIER:
                hit_ship = "Carrier"
                if your_turn:
                    Client.client_functions.Battleship_Helper_Functions.Opponent_Carrier_Alive = False
            elif ship_was_sunk == SUNK_BATTLESHIP:
                hit_ship = "Battleship"
                if your_turn:
                    Client.client_functions.Battleship_Helper_Functions.Opponent_Battleship_Alive = False
            elif ship_was_sunk == SUNK_CRUISER:
                hit_ship = "Cruiser"
                if your_turn:
                    Client.client_functions.Battleship_Helper_Functions.Opponent_Cruiser_Alive = False
            elif ship_was_sunk == SUNK_SUBMARINE:
                hit_ship = "Submarine"
                if your_turn:
                    Client.client_functions.Battleship_Helper_Functions.Opponent_Submarine_Alive = False
            elif ship_was_sunk == SUNK_DESTROYER:
                hit_ship = "Destroyer"
                if your_turn:
                    Client.client_functions.Battleship_Helper_Functions.Opponent_Destroyer_Alive = False
            if your_turn:
                DrawShipWasSunkGuesser(hit_ship)
            else:
                DrawShipWasSunkGuessed(hit_ship)
        elif shot_missed and your_turn:
            DrawShotMissedGuesser()
        elif shot_missed and not your_turn:
            DrawShotMissedGuessed()
        elif your_turn:
            DrawYourTurn()
        else:
            DrawNotYourTurn()
    else:
        DrawRectPlusBorder(BLACK, 0, 151, 320, 207)
        DrawRectPlusBorder(BLACK, 980, 151, 320, 207)

        results_rect = pygame.draw.rect(window, WHITE, (320, 151, 660, 649))
        return_to_menu = createTextSys('comicsans', 40, "Returning to Main Menu in: " + str(i), BLACK)
        if winner == client_i.username:
            you_win_text = createTextSys("calibri", 40, "You sunk all of their ships! You win!", BLACK)
            BlitTextToCenterRect(results_rect, you_win_text, 0, -20)
            BlitTextToCenterRect(results_rect, return_to_menu, 0, 20)
        else:
            you_lost_text_1 = createTextSys("calibri", 40, client_i.opponent_username + " sunk", BLACK)
            you_lost_text_2 = createTextSys("calibri", 40, "all of your ships...You Lost", BLACK)
            BlitTextToCenterRect(results_rect, you_lost_text_1, 0, -20)
            BlitTextToCenterRect(results_rect, you_lost_text_2, 0, 20)
            BlitTextToCenterRect(results_rect, return_to_menu, 0, 60)
    DrawShipsStatusBox(player)


def updateRPSWindow(did_player_move, did_opponent_move, was_game_tied, who_won, opponent_disconnected, i):
    global Count_Array
    RPS_rect = pygame.draw.rect(window, GREY, (320, 151, 660, 649))

    # The countdown text
    if Count_Array[0] < 0:
        countdown_text = createTextSys("comicsans", 40, str(0), BLACK)
    else:
        countdown_text = createTextSys("comicsans", 40, str(round(Count_Array[0])), BLACK)
    window.blit(countdown_text, (width / 2 - countdown_text.get_width() / 2, 200))

    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Your Move", True, (0, 255, 255))
    BlitTextToCenterRect(RPS_rect, text, -160, -200)

    text = font.render("Opponent's", True, (0, 255, 255))
    BlitTextToCenterRect(RPS_rect, text, 160, -200)

    move1 = Client.client_functions.Battleship_Event_Functions.Player_Move_RPS
    move2 = Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS
    if did_player_move and did_opponent_move:
        text1 = font.render(move1, True, (0, 0, 0))
        text2 = font.render(move2, True, (0, 0, 0))
    else:
        if did_player_move:
            text1 = font.render(move1, True, (0, 0, 0))
        else:
            text1 = font.render("Waiting...", True, (0, 0, 0))
        if opponent_disconnected:
            text2 = font.render("DISCONNECTED", True, RED)
            return_to_menu = createTextSys('calibri', 20, "Returning to Main Menu in: " + str(i), RED)
            BlitTextToCenterRect(RPS_rect, return_to_menu, 160, -65)
        else:
            if did_opponent_move:
                text2 = font.render("Locked In", True, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (0, 0, 0))
    BlitTextToCenterRect(RPS_rect, text1, -160, -100)
    BlitTextToCenterRect(RPS_rect, text2, 160, -100)

    ROCK_BUTTON.draw(window)
    PAPER_BUTTON.draw(window)
    SCISSORS_BUTTON.draw(window)

    if was_game_tied:
        text = font.render("Tie Game! Go Again!", True, (255, 0, 0))
        BlitTextToCenterRect(RPS_rect, text, 0, -55)
    elif who_won is not None:
        if who_won == client_i.username:
            text = font.render("You Won! You go first!", True, (255, 0, 0))
            BlitTextToCenterRect(RPS_rect, text, 0, -55)
        else:
            text = font.render("You Lost...Opponent goes first.", True, (255, 0, 0))
            BlitTextToCenterRect(RPS_rect, text, 0, -55)


def UpdateWindowChoosingLocations(this_player, opponent, opponent_disconnected, i, is_time_up):
    global Count_Array

    this_player.DrawShipsGrid(window)
    DrawCoordinates()

    # The countdown text
    if Count_Array[0] < 0:
        countdown_text = createTextSys("comicsans", 40, str(0), BLACK)
    else:
        countdown_text = createTextSys("comicsans", 40, str(round(Count_Array[0])), BLACK)
    window.blit(countdown_text, (width / 2 - countdown_text.get_width() / 2, 80))

    # If the player or the opponent's spots aren't chosen yet, ask either or to do so
    if not this_player.are_spots_chosen or not opponent.are_spots_chosen:
        # Draws the "Choose your spots for your ships" text on a rectangle on the screen
        DrawChooseSpotsBox(this_player, opponent, opponent_disconnected, i, is_time_up)
        DrawShipButtonsBox()
        for button in ShipsButtons:
            button.draw(window)
        DoneButton.draw(window)


def updateTopInfoWindow():
    window.fill(WHITE)

    # The Title of the game
    title = createText("Client/assets/SaucerBB.ttf", 75, "BATTLESHIP", BLACK)
    window.blit(title, (width / 2 - title.get_width() / 2, 10))

    # The versus text
    Versus = createText("Client/assets/Pervitina-Dex-FFP.ttf", 30, "VS", BLACK)
    window.blit(Versus, (width / 2 - Versus.get_width() / 2, 110))

    # Player 1 text
    your_username = createText("Client/assets/Fragmentcore.otf", 32, client_i.username, BLACK)
    window.blit(your_username, ((width / 2 - Versus.get_width() / 2) / 2 - your_username.get_width() / 2, 110))

    # Player 2 text
    opponent_text = createText("Client/assets/Fragmentcore.otf", 32, client_i.opponent_username, BLACK)
    window.blit(opponent_text, ((width - (width / 2 - Versus.get_width() / 2) / 2) - opponent_text.get_width() / 2, 110))
