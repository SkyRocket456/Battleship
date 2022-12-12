from Client.client_functions.AskForUsername import askForUsername
from Client.client_functions.MenuScreen import menu_screen
from Client.client_functions.InQueue import In_Queue
from Client.client_functions.Battleship_Client import Battleship
from info.Codes import *

while askForUsername() != GAME_CLOSED:  # Ask the player for their username. If they closed the window, quit the game
    menu_authorization = menu_screen()  # Enter the main menu
    while menu_authorization == FIND_MATCH:  # If the player wants to find a match,
        queue_authorization = In_Queue()  # Enter the queue
        if queue_authorization == GAME_CLOSED:  # If the game closed while in queue, quit the game
            break
        elif queue_authorization == BACK_TO_MAIN_MENU:  # If the player wants to go back to the main menu, let them do so
            menu_authorization = menu_screen()
        elif queue_authorization == IN_GAME:  # If the player found a match, it's GAME TIME
            game_authorization = Battleship()
            if game_authorization == GAME_CLOSED:  # If the game was closed during the game, end the program
                break
            elif game_authorization == OPPONENT_DISCONNECTED:  # If the opponent disconnected during the game, return back to main menu
                menu_authorization = menu_screen()
            elif game_authorization == BACK_TO_MAIN_MENU:  # If anything happens during the game that causes the game to end prematurely, return back to the main menu
                menu_authorization = menu_screen()
    if menu_authorization == CHANGE_USERNAME:  # if the player wants to change their username, go back to the username screen
        pass
    else:  # If anything else, break and exit
        break


