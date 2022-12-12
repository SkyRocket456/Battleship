from Client.classes.button import TextButton
from Client.classes.TextBox import TextBox
from Client.client_i import *
from info.Codes import *
from info.colors import *
from Client.helper_functions import *

image_alpha = 0  # Setting image transparency
fade_frame_number = 60  # Decide how many frames you want the image to fade in over
FPS = 30  # And the frames per second
FPS_Clock = pygame.time.Clock()

Find_Match = TextButton(createTextSys("comicsans", 40, "Find Match", WHITE), width / 2 - 100, height / 2, GREY, 200, 100)
Face_CPU = TextButton(createTextSys("comicsans", 40, "Vs CPU", WHITE), width / 2 - 100, height / 2 + 150, GREY, 200, 100)


# Functions

def updateWindowMenu():
    from Client import client_i
    global image_alpha
    menu_background_image = pygame.image.load('Client/assets/background.png').convert()

    while True:  # Slowly let the background image come into sight
        window.fill(GREY)  # Fill the window with a grey background
        if image_alpha < 125:
            image_alpha += 255 / fade_frame_number  # Change the transparency variable
        else:
            break  # If the transparency is what we want, break out of the loop
        menu_background_image.set_alpha(image_alpha)  # Set the image's alpha value
        window.blit(menu_background_image, (650 - menu_background_image.get_width() / 2, 50))
        pygame.display.update()  # Update the screen
        FPS_Clock.tick(FPS)  # Wait for the next frame

    # Set the final transparency of the background image and display it to the window
    menu_background_image.set_alpha(image_alpha)
    window.blit(menu_background_image, (650 - menu_background_image.get_width() / 2, 50))

    # The Title of the game
    title = createText("Client/assets/SaucerBB.ttf", 100, "BATTLESHIP", BLACK)
    window.blit(title, (width / 2 - title.get_width() / 2, 75))

    # The version number
    version_number = createTextSys('calibri', 40, version_n, BLACK)
    window.blit(version_number, (950, 720))

    # The rectangle around the username
    username_text = createTextSys("comicsans", 40, client_i.username, BLACK)
    user_rect = pygame.Rect(300, 725, username_text.get_width() + 10, 25)
    UsernameBox = TextBox(user_rect, username_text, BLACK)
    UsernameBox.draw(window)

    # Display the buttons onto the window
    Find_Match.draw(window)
    Face_CPU.draw(window)
    pygame.display.update()


def checkMenuEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the window is closed, send a message to the server that the client is gone
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED

        if event.type == pygame.MOUSEBUTTONDOWN:  # If the player left clicked, check to see if any of the menu buttons were pressed
            pos = pygame.mouse.get_pos()

            if Find_Match.click(pos) and n.isClientConnected():
                return FIND_MATCH

            if Face_CPU.click(pos):  # If the player wants to fight against a CPU, that mode isn't available yet :3
                sorry = createTextSys("comicsans", 40, "This mode is not available yet!", BLACK)
                window.blit(sorry, (width / 2 - sorry.get_width() / 2, 650))
                pygame.display.update()
                pygame.time.delay(3000)

    return ON_MENU_SCREEN


def menu_screen():
    run = ON_MENU_SCREEN
    clock = pygame.time.Clock()
    while run == ON_MENU_SCREEN:  # Keep looping while the player is still the menu screen
        clock.tick(60)
        updateWindowMenu()
        run = checkMenuEvents()
    return run

