from Client.classes.TextBox import UserInputBox
from Client.classes.button import TextButton
from Client.client_i import *
from info.Codes import *
from info.colors import *
from Client.helper_functions import *

user_text = ""


def updateWindowUserName(run, active):
    global user_text
    if run != DONE_INPUTTING_USERNAME:
        window.fill(GREY)  # Fill the window with a grey background to allow transparency

        # Load the image to the background
        background_image = pygame.image.load('Client/assets/background.png').convert()
        background_image.set_alpha(125)
        window.blit(background_image, (650 - background_image.get_width() / 2, 50))

        # Create a text asking the player for their username
        request = createTextSys("comicsans", 25, "Enter a username you'd like to be seen as. Press enter after you are done", BLACK)
        window.blit(request, (width / 2 - request.get_width() / 2, 200))

        # A textbox that allows user input and gets bigger as more text is added
        username = createTextSys("comicsans", 40, user_text, BLACK)
        user_rect = pygame.Rect(width / 2 - request.get_width() / 2, 250, max(300, username.get_width() + 10), 32)
        UsernameBox = UserInputBox(user_rect, username, BLUE, BLACK)
        UsernameBox.draw(window, active)

        pygame.display.update()  # Update the window
        return user_rect
    else:
        from Client import client_i
        last_call = createTextSys("comicsans", 50, "Are you sure?", BLACK)  # Create text that says "Are you sure?
        window.blit(last_call, (width / 2 - last_call.get_width() / 2, 350))

        yes_text = createTextSys("comicsans", 40, "YES", WHITE)  # Create a button that says YES
        Yes = TextButton(yes_text, 650 - 140, 400, GREY, 100, 100)
        Yes.draw(window)

        no_text = createTextSys("comicsans", 40, "NO", WHITE)  # Create a button that says NO
        No = TextButton(no_text, 650 + 40, 400, GREY, 100, 100)
        No.draw(window)

        pygame.display.update()  # Update the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user quits the game, close the window
                n.SendData(GAME_CLOSED)  # Send "a message to the server indicating that the client has closed the window
                return GAME_CLOSED
            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player left clicks,
                pos = pygame.mouse.get_pos()  # Get
                # the position of the clicked cursor
                if Yes.click(pos):  # If the player clicked "YES",
                    if len(user_text) > 16:
                        not_valid = createTextSys("comicsans", 40, "Username is too long. Maximum of 16 characters", RED)
                        window.blit(not_valid, (width / 2 - not_valid.get_width() / 2, 600))
                    elif n.SendAndReceive(user_text) == USERNAME_TAKEN:  # Send username to the server. If the username is already taken, it is INVALID
                        not_valid = createTextSys("comicsans", 40, "This username is already taken!", RED)
                        window.blit(not_valid, (width / 2 - not_valid.get_width() / 2, 600))
                    else:
                        client_i.username = user_text
                        return ALLOW_INTO_MENU  # Else, allow them to enter the menu screen
                    pygame.display.update()
                    pygame.time.delay(3000)
                    return NO_USERNAME_INPUTTED
                if No.click(pos):  # If the user clicked "NO", return to default
                    return NO_USERNAME_INPUTTED
        return DONE_INPUTTING_USERNAME


def checkUserEvents(user_rect, active):
    global user_text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the player quits the game, close the window
            n.SendData(GAME_CLOSED)
            return GAME_CLOSED, active

        if event.type == pygame.MOUSEBUTTONDOWN:  # If the player left clicks,
            if user_rect.collidepoint(event.pos):  # Check if the player clicked on the text box
                active = True  # If the text box was clicked, change the color of the box
            else:
                active = False

        if event.type == pygame.KEYDOWN:  # If the player presses down a key
            if active:
                if event.key == pygame.K_BACKSPACE:  # If the player pressed backspace, delete the last letter of their input
                    user_text = user_text[0: -1]
                else:
                    user_text += event.unicode  # Else, add the letter they just typed into their input

            if event.key == pygame.K_RETURN:  # If the player pressed Enter, check if their username is valid
                if len(user_text) == 0:  # If the username is empty, it is invalid
                    invalid = createTextSys("comicsans", 50, "Invalid Username!", RED)
                    window.blit(invalid, (width / 2 - invalid.get_width() / 2, 350))
                    pygame.display.update()
                    pygame.time.delay(3000)
                else:
                    return DONE_INPUTTING_USERNAME, active  # Return that the player is done inputting their username
    return NO_USERNAME_INPUTTED, active


def askForUsername():
    global user_text
    run = NO_USERNAME_INPUTTED
    active = False
    clock = pygame.time.Clock()
    while run == NO_USERNAME_INPUTTED:  # Keep looping until the player has entered a valid username
        if run == GAME_CLOSED:  # If the player closes the window, end the game
            break

        if run == ALLOW_INTO_MENU:  # If the player enters a valid username, take them to the main menu
            break

        user_rect = updateWindowUserName(run, active)  # Update the window asking for the username
        run, active = checkUserEvents(user_rect, active)  # Constantly check for new events in the window
        while run == DONE_INPUTTING_USERNAME:
            run = updateWindowUserName(run, active)  # Check if the player is sure of their username

        clock.tick(60)
    return run
