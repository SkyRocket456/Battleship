from Server.player import GamePlayer
from Client.helper_functions import *
from Client import client_i
import Client.client_functions.Battleship_Client
import Client.client_functions.Battlehip_Window_Functions
from Client.client_i import *
from info.colors import *

Opponent_Carrier_Alive = True
Opponent_Battleship_Alive = True
Opponent_Cruiser_Alive = True
Opponent_Submarine_Alive = True
Opponent_Destroyer_Alive = True


def Countdown(count):  # The countdown function. Counts down from from number passed into it.
    while len(Client.client_functions.Battlehip_Window_Functions.Count_Array) > 0:
        Client.client_functions.Battlehip_Window_Functions.Count_Array.pop(0)
    while len(Client.client_functions.Battleship_Client.Time_Is_Up_List) > 0:
        Client.client_functions.Battleship_Client.Time_Is_Up_List.pop(0)

    # Appends number to an list in order for other functions to use it, such as functions that update the screen
    Client.client_functions.Battlehip_Window_Functions.Count_Array.append(count)

    clock = pygame.time.Clock()
    dt = 0  # Delta times (time since last tick).
    temp_dt = 0  # Delta times (time since last tick).
    one_sec = 1

    while one_sec > 0:  # Wait one second
        one_sec -= temp_dt
        temp_dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

    while len(Client.client_functions.Battleship_Client.Stop_Timer) == 0:
        Client.client_functions.Battlehip_Window_Functions.Count_Array[0] -= dt
        if Client.client_functions.Battlehip_Window_Functions.Count_Array[0] < -0.9999:
            break
        dt = clock.tick(30) / 1000  # / 1000 to convert to seconds.

    if len(Client.client_functions.Battleship_Client.Stop_Timer) > 0:  # If the timer was stopped due to an event between the two players, clear it afterwards
        while len(Client.client_functions.Battleship_Client.Stop_Timer) > 0:
            Client.client_functions.Battleship_Client.Stop_Timer.pop(0)
    else:  # Else, this means the timer reached 0
        Client.client_functions.Battleship_Client.Time_Is_Up_List.append(True)


def waitForCountdownToEnd():
    Client.client_functions.Battleship_Client.Stop_Timer.append(True)
    while len(Client.client_functions.Battleship_Client.Stop_Timer) > 0:  # Wait for the Countdown thread to close
        pass


def ResetRPS():
    Client.client_functions.Battleship_Event_Functions.RPS_Did_Player_Make_Move = False
    Client.client_functions.Battleship_Event_Functions.RPS_Did_Opponent_Make_Move = False
    Client.client_functions.Battleship_Event_Functions.Player_Move_RPS = None
    Client.client_functions.Battleship_Event_Functions.Opponent_Move_RPS = None


def DrawRectPlusBorder(color, left, top, x, y):  # Draw a rectangle on the screen with a border
    rect = pygame.draw.rect(window, color, (left, top, x, y))
    for i in range(1):
        pygame.draw.rect(window, (0, 0, 0), (rect.x - i, rect.y - i, rect.width, rect.height), 1)
    return rect


def BlitTextToCenterRect(rect, text, offset_x, offset_y):
    window.blit(text, (rect.x + rect.width / 2 - text.get_width() / 2 + offset_x, rect.y + rect.height / 2 - text.get_height() / 2 + offset_y))


def DrawCoordinates():
    # Print the coordinates on the left and top side
    for y, letter in zip(range(210, 800, 59), range(65, 75)):
        coord_letter_rect = pygame.draw.rect(window, WHITE, (320, y, 60, 59))
        letter_ = createTextSys("comicsans", 40, chr(letter), BLACK)
        BlitTextToCenterRect(coord_letter_rect, letter_, 0, 0)
    for x, number in zip(range(380, 980, 60), range(1, 11)):
        coord_number_rect = pygame.draw.rect(window, WHITE, (x, 151, 60, 59))
        number_ = createTextSys("comicsans", 40, str(number), BLACK)
        BlitTextToCenterRect(coord_number_rect, number_, 0, 0)


def DrawChooseSpotsBox(player: GamePlayer, opponent: GamePlayer, opponent_disconnected, i, is_time_up):
    choose_spots_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_choose_spots_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    # Cases for the player's box
    if not player.are_spots_chosen:
        if not is_time_up:
            choose_spots_text = createTextSys("comicsans", 40, "Choose the spots", BLACK)
            for_ships_text = createTextSys("comicsans", 40, "for your ships", BLACK)

            BlitTextToCenterRect(choose_spots_box, choose_spots_text, 0, -20)
            BlitTextToCenterRect(choose_spots_box, for_ships_text, 0, 20)
        else:
            too_long = createTextSys("comicsans", 35, "You took too long", RED)
            selecting = createTextSys("comicsans", 35, "selecting ship locations!", RED)
            return_to_menu = createTextSys("comicsans", 25, "Returning to Main Menu in: " + str(i), RED)

            BlitTextToCenterRect(choose_spots_box, too_long, 0, -50)
            BlitTextToCenterRect(choose_spots_box, selecting, 0, 0)
            BlitTextToCenterRect(choose_spots_box, return_to_menu, 0, 50)
    else:
        done_text_ = createTextSys("comicsans", 50, "DONE!", BLACK)
        BlitTextToCenterRect(choose_spots_box, done_text_, 0, 0)

    # Cases for the opponent's box
    if opponent_disconnected:
        opp_choose_spots_text_red = createTextSys("comicsans", 30, client_i.opponent_username, RED)
        disconnected = createTextSys("comicsans", 35, "DISCONNECTED", RED)
        return_to_menu = createTextSys("comicsans", 25, "Returning to Main Menu in: " + str(i), RED)
        BlitTextToCenterRect(opp_choose_spots_box, opp_choose_spots_text_red, 0, -50)
        BlitTextToCenterRect(opp_choose_spots_box, disconnected, 0, 0)
        BlitTextToCenterRect(opp_choose_spots_box, return_to_menu, 0, 50)

    elif not opponent.are_spots_chosen:
        if not is_time_up:
            opp_choose_spots_text = createTextSys("comicsans", 30, client_i.opponent_username, BLACK)
            opp_for_ships_text_1 = createTextSys("comicsans", 30, "is choosing the spots", BLACK)
            opp_for_ships_text_2 = createTextSys("comicsans", 30, "for their ships...", BLACK)

            BlitTextToCenterRect(opp_choose_spots_box, opp_choose_spots_text, 0, -50)
            BlitTextToCenterRect(opp_choose_spots_box, opp_for_ships_text_1, 0, 0)
            BlitTextToCenterRect(opp_choose_spots_box, opp_for_ships_text_2, 0, 50)
        else:
            opp_choose_spots_text_red = createTextSys("comicsans", 30, client_i.opponent_username, RED)
            selecting_o = createTextSys("comicsans", 35, "took too long selecting", RED)
            ship_loc_o = createTextSys("comicsans", 35, "ship locations", RED)
            return_to_menu = createTextSys("comicsans", 25, "Returning to Main Menu in: " + str(i), RED)

            BlitTextToCenterRect(opp_choose_spots_box, opp_choose_spots_text_red, 0, -50)
            BlitTextToCenterRect(opp_choose_spots_box, selecting_o, 0, -20)
            BlitTextToCenterRect(opp_choose_spots_box, ship_loc_o, 0, 20)
            BlitTextToCenterRect(opp_choose_spots_box, return_to_menu, 0, 50)
    else:
        opp_choose_spots_text = createTextSys("comicsans", 30, client_i.opponent_username, BLACK)
        opp_done_text_2 = createTextSys("comicsans", 29, "finished choosing their", BLACK)
        opp_done_text_3 = createTextSys("comicsans", 29, "ship locations.", BLACK)

        BlitTextToCenterRect(opp_choose_spots_box, opp_choose_spots_text, 0, -50)
        BlitTextToCenterRect(opp_choose_spots_box, opp_done_text_2, 0, 0)
        BlitTextToCenterRect(opp_choose_spots_box, opp_done_text_3, 0, 50)


def DrawShipButtonsBox():
    ship_buttons_box = DrawRectPlusBorder(TEAL, 0, 358, 320, 442)

    done_button_box = DrawRectPlusBorder(TEAL, 980, 358, 320, 442)

    done_text_1 = createTextSys("comicsans", 40, "Click DONE when you", BLACK)
    done_text_2 = createTextSys("comicsans", 40, "are finished selecting", BLACK)
    done_text_3 = createTextSys("comicsans", 40, "your ship locations", BLACK)

    BlitTextToCenterRect(done_button_box, done_text_1, 0, -221 + done_text_1.get_height() / 2 + 10)
    BlitTextToCenterRect(done_button_box, done_text_2, 0, -221 + done_text_1.get_height() / 2 + 40)
    BlitTextToCenterRect(done_button_box, done_text_3, 0, -221 + done_text_1.get_height() / 2 + 70)


def DrawShipsStatusBox(player: GamePlayer):
    this_player_text = createTextSys("comicsans", 29, client_i.username + "'s", BLACK)
    opponent_text = createTextSys("comicsans", 29, client_i.opponent_username + "'s", BLACK)

    ships_text = createTextSys("comicsans", 29, "ships", BLACK)
    if Opponent_Carrier_Alive:
        carrier_text = createTextSys("comicsans", 40, "Carrier: Intact", BLACK)
    else:
        carrier_text = createTextSys("comicsans", 40, "Carrier: Sunk", BLACK)
    if Opponent_Battleship_Alive:
        battleship_text = createTextSys("comicsans", 40, "Battleship: Intact", BLACK)
    else:
        battleship_text = createTextSys("comicsans", 40, "Battleship: Sunk", BLACK)
    if Opponent_Cruiser_Alive:
        cruiser_text = createTextSys("comicsans", 40, "Cruiser: Intact", BLACK)
    else:
        cruiser_text = createTextSys("comicsans", 40, "Cruiser: Sunk", BLACK)
    if Opponent_Submarine_Alive:
        submarine_text = createTextSys("comicsans", 40, "Submarine: Intact", BLACK)
    else:
        submarine_text = createTextSys("comicsans", 40, "Submarine: Sunk", BLACK)
    if Opponent_Destroyer_Alive:
        destroyer_text = createTextSys("comicsans", 40, "Destroyer: Intact", BLACK)
    else:
        destroyer_text = createTextSys("comicsans", 40, "Destroyer: Sunk", BLACK)

    your_player_box = DrawRectPlusBorder(TEAL, 0, 358, 320, 442)
    BlitTextToCenterRect(your_player_box, this_player_text, 0, -200)
    BlitTextToCenterRect(your_player_box, ships_text, 0, -180)
    BlitTextToCenterRect(your_player_box, player.CarrierStatus(), 0 - ((submarine_text.get_width() - carrier_text.get_width()) / 2), -100)
    BlitTextToCenterRect(your_player_box, player.BattleshipStatus(), 0 - ((submarine_text.get_width() - battleship_text.get_width()) / 2), -50)
    BlitTextToCenterRect(your_player_box, player.CruiserStatus(), 0 - ((submarine_text.get_width() - cruiser_text.get_width()) / 2), 0)
    BlitTextToCenterRect(your_player_box, player.SubmarineStatus(), 0, 50)
    BlitTextToCenterRect(your_player_box, player.DestroyerStatus(), 0 - ((submarine_text.get_width() - destroyer_text.get_width()) / 2), 100)

    opponent_box = DrawRectPlusBorder(TEAL, 980, 358, 320, 442)
    BlitTextToCenterRect(opponent_box, opponent_text, 0, -200)
    BlitTextToCenterRect(opponent_box, ships_text, 0, -180)
    BlitTextToCenterRect(opponent_box, carrier_text, 0 - ((submarine_text.get_width() - carrier_text.get_width()) / 2), -100)
    BlitTextToCenterRect(opponent_box, battleship_text, 0 - ((submarine_text.get_width() - battleship_text.get_width()) / 2), -50)
    BlitTextToCenterRect(opponent_box, cruiser_text, 0 - ((submarine_text.get_width() - cruiser_text.get_width()) / 2), 0)
    BlitTextToCenterRect(opponent_box, submarine_text, 0, 50)
    BlitTextToCenterRect(opponent_box, destroyer_text, 0 - ((submarine_text.get_width() - destroyer_text.get_width()) / 2), 100)


def DrawNotYourTurn():
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    opp_username_text = createTextSys("comicsans", 30, client_i.opponent_username, BLACK)

    waiting_text_1 = createTextSys("comicsans", 30, "Waiting for", BLACK)
    waiting_text_2 = createTextSys("comicsans", 30, "to finish their turn...", BLACK)

    opp_strike_text = createTextSys("comicsans", 28, "is choosing a location to strike...", BLACK)

    BlitTextToCenterRect(your_turn_box, waiting_text_1, 0, -50)
    BlitTextToCenterRect(your_turn_box, opp_username_text, 0, 0)
    BlitTextToCenterRect(your_turn_box, waiting_text_2, 0, 50)

    BlitTextToCenterRect(opp_turn_box, opp_username_text, 0, -20)
    BlitTextToCenterRect(opp_turn_box, opp_strike_text, 0, 20)


def DrawYourTurn():
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    your_strike_text_1 = createTextSys("comicsans", 28, "Choose a location", BLACK)
    your_strike_text_2 = createTextSys("comicsans", 28, "to hit!", BLACK)

    waiting_text_1 = createTextSys("comicsans", 30, "Waiting for", BLACK)
    username_text = createTextSys("comicsans", 30, client_i.username, BLACK)
    waiting_text_2 = createTextSys("comicsans", 30, "to finish their turn...", BLACK)

    BlitTextToCenterRect(your_turn_box, your_strike_text_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, your_strike_text_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, waiting_text_1, 0, -50)
    BlitTextToCenterRect(opp_turn_box, username_text, 0, 0)
    BlitTextToCenterRect(opp_turn_box, waiting_text_2, 0, 50)


def DrawHitAShip():
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    you_hit_their_ship_1 = createTextSys("comicsans", 28, "You hit one of", BLACK)
    you_hit_their_ship_2 = createTextSys("comicsans", 28, "their ships!", BLACK)

    revenge_text_1 = createTextSys("comicsans", 30, "Ow! You'll", BLACK)
    revenge_text_2 = createTextSys("comicsans", 30, "pay for that!", BLACK)

    BlitTextToCenterRect(your_turn_box, you_hit_their_ship_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, you_hit_their_ship_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, revenge_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, revenge_text_2, 0, 20)


def DrawShipWasHit(hit_ship):
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    ship_was_hit_1 = createTextSys("comicsans", 28, "Your " + hit_ship, BLACK)
    ship_was_hit_2 = createTextSys("comicsans", 28, "was hit!", BLACK)

    triumph_text_1 = createTextSys("comicsans", 30, "Haha! Looks like", BLACK)
    triumph_text_2 = createTextSys("comicsans", 30, "I hit your ship!", BLACK)

    BlitTextToCenterRect(your_turn_box, ship_was_hit_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, ship_was_hit_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, triumph_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, triumph_text_2, 0, 20)


def DrawShipWasSunkGuesser(sunk_ship):
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    ship_was_hit_1 = createTextSys("comicsans", 28, "You sunk their " + sunk_ship + "!", BLACK)

    sad_text_1 = createTextSys("comicsans", 30, "NOO! How could", BLACK)
    sad_text_2 = createTextSys("comicsans", 30, "you sink my " + sunk_ship + "!", BLACK)

    BlitTextToCenterRect(your_turn_box, ship_was_hit_1, 0, -20)

    BlitTextToCenterRect(opp_turn_box, sad_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, sad_text_2, 0, 20)


def DrawShipWasSunkGuessed(sunk_ship):
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    ship_was_hit_1 = createTextSys("comicsans", 28, "Your " + sunk_ship, BLACK)
    ship_was_hit_2 = createTextSys("comicsans", 28, "was sunk!", BLACK)

    triumph_text_1 = createTextSys("comicsans", 30, "Down she goes!", BLACK)
    triumph_text_2 = createTextSys("comicsans", 30, "Your " + sunk_ship + " is gone!", BLACK)

    BlitTextToCenterRect(your_turn_box, ship_was_hit_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, ship_was_hit_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, triumph_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, triumph_text_2, 0, 20)


def DrawShotMissedGuesser():
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    shot_missed_1 = createTextSys("comicsans", 28, "You missed all", BLACK)
    shot_missed_2 = createTextSys("comicsans", 28, "of their ships!", BLACK)

    triumph_text_1 = createTextSys("comicsans", 30, "Haha! Better", BLACK)
    triumph_text_2 = createTextSys("comicsans", 30, "luck next time!", BLACK)

    BlitTextToCenterRect(your_turn_box, shot_missed_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, shot_missed_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, triumph_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, triumph_text_2, 0, 20)


def DrawShotMissedGuessed():
    your_turn_box = DrawRectPlusBorder(GREY, 0, 151, 320, 207)
    opp_turn_box = DrawRectPlusBorder(GREY, 980, 151, 320, 207)

    shot_missed_1 = createTextSys("comicsans", 28, "They missed all", BLACK)
    shot_missed_2 = createTextSys("comicsans", 28, "of your ships!", BLACK)

    sad_text_1 = createTextSys("comicsans", 30, "Damn, I missed", BLACK)
    sad_text_2 = createTextSys("comicsans", 30, "all of them?!", BLACK)

    BlitTextToCenterRect(your_turn_box, shot_missed_1, 0, -20)
    BlitTextToCenterRect(your_turn_box, shot_missed_2, 0, 20)

    BlitTextToCenterRect(opp_turn_box, sad_text_1, 0, -20)
    BlitTextToCenterRect(opp_turn_box, sad_text_2, 0, 20)
