from player import Player
from Client.classes.players_connected import players_connected

# used for the server
players_connected = players_connected()
player_client_thread_signal = []
game_queue = []

# used for the log
players_that_just_connected: list[Player] = []
players_that_just_disconnected: list[tuple[Player, bool]] = []
players_changed_username: list[tuple[str, Player]] = []
players_that_joined_queue: list[Player] = []
players_that_left_queue: list[Player] = []
players_that_are_in_game: list[tuple[Player, Player]] = []
players_left_during_game: list[tuple[Player, Player]] = []
players_time_ran_out: list[tuple[Player, Player, int]] = []
players_finished_game: list[tuple[Player, Player]] = []
