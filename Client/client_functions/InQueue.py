from info.Codes import *
from Client.helper_functions import *
from info.colors import *
import threading
from Client.client_i import *
from Client.classes.TextBox import TextBox
from Client.classes.button import TextButton
from Client import client_i

image_alpha = 0  # Setting image transparency
fade_frame_number = 60  # Decide how many frames you want the image to fade in over
FPS = 30  # And the frames per second
FPS_Clock = pygame.time.Clock()

dots_increment = 0
dots = "."

Go_Back_to_Main_Menu = TextButton(createTextSys("comicsans", 40, "Back to Main Menu", WHITE), width / 2 - 150, height / 2 + 150, GREY, 300, 100)

Searching_For_Game = True


def updateWindowMatchFound(time_left, o_disconnected):
    player_font = "Client/assets/Fragmentcore.otf"
    match_found_font = "Client/assets/Sheeping Dogs.ttf"
    window.fill(TEAL)

    # The Match Found Text
    found = createText(match_found_font, 40, "MATCH FOUND!", BLACK)  # Prints the Looking for Opponent
    window.blit(found, (width / 2 - found.get_width() / 2, 170))

    if not o_disconnected:
        # The Countdown Text
        count = createTextSys('calibri', 40, str(time_left), BLACK)
        window.blit(count, (width / 2 - count.get_width() / 2, 235))

    # Your username text
    your_username = createText(player_font, 50, client_i.username, BLACK)
    window.blit(your_username, (width / 2 - your_username.get_width() / 2, 300))

    # The versus text
    Versus = createText("Client/assets/Pervitina-Dex-FFP.ttf", 50, "VS", BLACK)
    window.blit(Versus, (width / 2 - Versus.get_width() / 2, 370))

    # Your opponent text
    opponent_text = createText(player_font, 50, str(client_i.opponent_username), BLACK)
    window.blit(opponent_text, (width / 2 - opponent_text.get_width() / 2, 435))

    if o_disconnected:
        o_d = createTextSys('calibri', 40, "OPPONENT DISCONNECTED", RED)
        window.blit(o_d, (width / 2 - o_d.get_width() / 2, 435 + opponent_text.get_height() + 10))
        return_ = createTextSys('calibri', 40, "Returning To Main Menu in: " + str(time_left), RED)
        window.blit(return_, (width / 2 - return_.get_width() / 2, 435 + opponent_text.get_height() + return_.get_height() + 20))

    pygame.display.update()


def updateWindowWaiting():
    global dots, dots_increment, Searching_For_Game
    while True:
        pygame.time.delay(1000)  # Call the delay first so the thread ends when the function In_Queue ends. This is why it is a thread
        if Searching_For_Game:
            window.fill(GREY)  # Fill the window with a grey background
            menu_background_image = pygame.image.load('Client/assets/background.png').convert()
            # Set the transparency of the background image and display it to the window
            menu_background_image.set_alpha(125)
            window.blit(menu_background_image, (650 - menu_background_image.get_width() / 2, 50))

            # The Title of the game
            title = createText("Client/assets/SaucerBB.ttf", 100, "BATTLESHIP", BLACK)
            window.blit(title, (width / 2 - title.get_width() / 2, 75))

            # The version number
            version_number = createTextSys('calibri', 40, version_n, BLACK)
            window.blit(version_number, (950, 720))

            # Looking for opponent... :) Controls the moving dots in the queue screen
            dots_increment += 1
            if dots_increment == 1:
                dots = "."
            elif dots_increment == 2:
                dots = "..."
            elif dots_increment == 3:
                dots = "....."
                dots_increment = 0
            waiting = createTextSys('calibri', 40, "Looking for an opponent" + dots, BLACK)  # Prints the Looking for Opponent
            window.blit(waiting, (width / 2 - 200, 170))

            # The rectangle around the username
            username_text = createTextSys("comicsans", 40, client_i.username, BLACK)
            user_rect = pygame.Rect(300, 725, username_text.get_width() + 10, 25)
            UsernameBox = TextBox(user_rect, username_text, BLACK)
            UsernameBox.draw(window)

            # The go back to menu button
            Go_Back_to_Main_Menu.draw(window)

            pygame.display.update()
        else:
            break


def checkMatchFoundEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the player quits the game, close the window
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED


def checkQueueEvents():
    global Searching_For_Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the player quits the game, close the window
            return GAME_CLOSED
        if event.type == pygame.MOUSEBUTTONDOWN:  # If the player left clicked, check to see if any of the menu buttons were pressed
            pos = pygame.mouse.get_pos()
            if Go_Back_to_Main_Menu.click(pos):
                Searching_For_Game = False
                return BACK_TO_MAIN_MENU
    return LOOKING_FOR_GAME


def In_Queue():
    global Searching_For_Game
    run = LOOKING_FOR_GAME
    clock = pygame.time.Clock()
    # The screen you see when you are looking for an opponent. This is in the background as to not slow down when you find an opponent
    Queue_Window = threading.Thread(target=updateWindowWaiting, args=())
    Queue_Window.start()
    # Create a new thread to run the window in the background so it does not slow down the connection time when the
    # player finds a match
    Searching_For_Game = True
    n.SendData(LOOKING_FOR_GAME)
    while run == LOOKING_FOR_GAME:  # Keep looping until the player finds another player to start a game with
        run = checkQueueEvents()
        client_i.opponent_username = n.ReceiveData()  # Continuously ping the server to notify when a match has been found
        if client_i.opponent_username:  # If an opponent is found, we start the countdown towards the match! :D
            Searching_For_Game = False  # Turn off the thread that controlled the "looking for opponent..." screen
            pygame.time.delay(1100)
            for i in range(5, 0 - 1, -1):  # The countdown from 5 to 0
                updateWindowMatchFound(i, False)
                pygame.time.delay(1000)
                data = n.ReceiveData()  # Continuously ping the server in case the opponent disconnects
                if data == OPPONENT_DISCONNECTED:  # If the opponent disconnected, return to main menu
                    for j in range(5, 0 - 1, -1):  # The countdown from 5 to 0
                        updateWindowMatchFound(j, True)
                        pygame.time.delay(1000)
                        run = checkMatchFoundEvents()
                        if run == GAME_CLOSED:  # If the player closes the screen while in countdown, quit the program
                            n.SendData(GAME_CLOSED)
                            return GAME_CLOSED
                    return BACK_TO_MAIN_MENU

                run = checkMatchFoundEvents()
                if run == GAME_CLOSED:  # If the player closes the screen while in countdown, quit the program
                    n.SendData(GAME_CLOSED)
                    return GAME_CLOSED
            return IN_GAME

        if run != LOOKING_FOR_GAME:  # If the players stops looking for a match
            Searching_For_Game = False
            if run == GAME_CLOSED:  # IF the player closed the game, send a message to the server
                n.SendData(GAME_CLOSED)
            elif run == BACK_TO_MAIN_MENU:  # If the player wants to go back to the main menu, send a message to the server
                n.SendData(LEFT_QUEUE)
            break

        clock.tick(60)
    return run
