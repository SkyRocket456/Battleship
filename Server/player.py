from Client.classes.cell import Cell
from Client.helper_functions import createTextSys
from info.Codes import *
from info.colors import *


class Player:
    def __init__(self, username, conn, address):
        self.username = username
        self.conn = conn
        self.address = address


class GamePlayer:
    ships_grid: list[list[Cell]]
    Carrier: list[Cell]
    Battleship: list[Cell]
    Cruiser: list[Cell]
    Submarine: list[Cell]
    Destroyer: list[Cell]

    def __init__(self, username):
        self.username = username
        self.ships_grid = []
        self.guessing_grid = []
        self.Carrier = []
        self.Battleship = []
        self.Cruiser = []
        self.Submarine = []
        self.Destroyer = []

        self.DidPlayerClickCarrier = False
        self.DidPlayerClickBattleship = False
        self.DidPlayerClickCruiser = False
        self.DidPlayerClickSubmarine = False
        self.DidPlayerClickDestroyer = False
        self.are_spots_chosen = False

    def ClickedCarrier(self):
        self.DidPlayerClickCarrier = True
        self.DidPlayerClickBattleship = False
        self.DidPlayerClickCruiser = False
        self.DidPlayerClickSubmarine = False
        self.DidPlayerClickDestroyer = False

    def ClickedBattleship(self):
        self.DidPlayerClickCarrier = False
        self.DidPlayerClickBattleship = True
        self.DidPlayerClickCruiser = False
        self.DidPlayerClickSubmarine = False
        self.DidPlayerClickDestroyer = False

    def ClickedCruiser(self):
        self.DidPlayerClickCarrier = False
        self.DidPlayerClickBattleship = False
        self.DidPlayerClickCruiser = True
        self.DidPlayerClickSubmarine = False
        self.DidPlayerClickDestroyer = False

    def ClickedSubmarine(self):
        self.DidPlayerClickCarrier = False
        self.DidPlayerClickBattleship = False
        self.DidPlayerClickCruiser = False
        self.DidPlayerClickSubmarine = True
        self.DidPlayerClickDestroyer = False

    def ClickedDestroyer(self):
        self.DidPlayerClickCarrier = False
        self.DidPlayerClickBattleship = False
        self.DidPlayerClickCruiser = False
        self.DidPlayerClickSubmarine = False
        self.DidPlayerClickDestroyer = True

    # This nested for loop prints the ships_grid for the game. It is 660 (width) by 649 (height). It starts at x = 320 and y = 151
    # The innermost for loop prints cells on the x axis where x =  320, 380, 440..., 980
    # The innermost for loop prints cells on the y axis where y =  151, 210, 269..., 800
    # Each ships_grid cell is 60 by 59 pixels
    def DrawShipsGrid(self, window):  # Draw the player's ships_grid onto the screen
        for i in range(10):
            for j in range(10):
                self.ships_grid[i][j].draw(window)

    def DrawGuessingGrid(self, window):  # Draw the player's ships_grid onto the screen
        for i in range(10):
            for j in range(10):
                self.guessing_grid[i][j].draw(window)

    # The 2nd cell in the ship decides if the ship is going to be up, down, left, or right. This function makes sure the 2nd cell is in fact either up, down, left, or right.
    @staticmethod
    def isUpDownLeftRight(cell: Cell, ship: list[Cell]):
        if cell.j - 1 == ship[0].j and cell.i == ship[0].i:
            return True
        if cell.j + 1 == ship[0].j and cell.i == ship[0].i:
            return True
        if cell.i - 1 == ship[0].i and cell.j == ship[0].j:
            return True
        if cell.i + 1 == ship[0].i and cell.j == ship[0].j:
            return True
        return False

    # If ship is horizontal, find the leftmost (min) and rightmost (max) cell. If ship is vertical, find the highest (min) and lowest (max) cell.
    @staticmethod
    def LowestAndHighestCell(vert_or_horz, ship: list[Cell]):
        min = ship[0]
        max = ship[0]
        if vert_or_horz == 'V':
            for cell in ship:
                if min.i > cell.i:
                    min = cell
            for cell in ship:
                if max.i < cell.i:
                    max = cell
        else:
            for cell in ship:
                if min.j > cell.j:
                    min = cell
            for cell in ship:
                if max.j < cell.j:
                    max = cell

        return min, max

    def isCellInLine(self, cell: Cell, ship: list[Cell]):  # Check if cells beyond the 1st and 2nd cells are in line with the rest of the ship
        if ship[0].i == ship[1].i:
            min, max = self.LowestAndHighestCell('H', ship)
            if (cell.j - 1 == max.j or cell.j + 1 == min.j) and (cell.i == max.i and cell.i == min.i):
                return True
        if ship[0].j == ship[1].j:
            min, max = self.LowestAndHighestCell('V', ship)
            if (cell.i - 1 == max.i or cell.i + 1 == min.i) and (cell.j == max.j and cell.j == min.j):
                return True
        return False

    # Checks if the selected cell is already occupied by another ship. If it is, remove that cell from the previous ship and add it to the newly selected ship
    @staticmethod
    def isCellOccupied(cell, other_ships: list[list[Cell]]):  # Check if the cell was occupied before selecting it
        for o_ship in other_ships:
            for cell_ in o_ship:
                if cell_ == cell:
                    return True
        return False

    # Check if the cell is valid to add to the selected ship button
    def checkForValidPlacement(self, ship_color, cell, ship: list[Cell], highest):
        if cell.color != ship_color:
            if len(ship) == 0:
                cell.color = ship_color
                ship.append(cell)
            elif len(ship) == 1 and self.isUpDownLeftRight(cell, ship):
                cell.color = ship_color
                ship.append(cell)
            elif 1 < len(ship) < highest and self.isCellInLine(cell, ship):
                cell.color = ship_color
                ship.append(cell)
            return cell
        else:
            cell.color = BLUE
            if cell in ship:
                ship.remove(cell)
            return cell

    def ClickedGridShipLoc(self, pos):  # Checks to see what happens next after a player clicks on the ships_grid
        for i in range(10):
            for j in range(10):
                if self.ships_grid[i][j].click(pos):
                    if self.DidPlayerClickCarrier:
                        other_ships = [self.Battleship, self.Cruiser, self.Submarine, self.Destroyer]
                        if not self.isCellOccupied(self.ships_grid[i][j], other_ships):
                            self.ships_grid[i][j] = self.checkForValidPlacement(Carrier_Color, self.ships_grid[i][j], self.Carrier, 5)
                    elif self.DidPlayerClickBattleship:
                        other_ships = [self.Carrier, self.Cruiser, self.Submarine, self.Destroyer]
                        if not self.isCellOccupied(self.ships_grid[i][j], other_ships):
                            self.ships_grid[i][j] = self.checkForValidPlacement(Battleship_Color, self.ships_grid[i][j], self.Battleship, 4)
                    elif self.DidPlayerClickCruiser:
                        other_ships = [self.Carrier, self.Battleship, self.Submarine, self.Destroyer]
                        if not self.isCellOccupied(self.ships_grid[i][j], other_ships):
                            self.ships_grid[i][j] = self.checkForValidPlacement(Cruiser_Color, self.ships_grid[i][j], self.Cruiser, 3)
                    elif self.DidPlayerClickSubmarine:
                        other_ships = [self.Carrier, self.Battleship, self.Cruiser, self.Destroyer]
                        if not self.isCellOccupied(self.ships_grid[i][j], other_ships):
                            self.ships_grid[i][j] = self.checkForValidPlacement(Submarine_Color, self.ships_grid[i][j], self.Submarine, 3)
                    elif self.DidPlayerClickDestroyer:
                        other_ships = [self.Carrier, self.Battleship, self.Cruiser, self.Submarine]
                        if not self.isCellOccupied(self.ships_grid[i][j], other_ships):
                            self.ships_grid[i][j] = self.checkForValidPlacement(Destroyer_Color, self.ships_grid[i][j], self.Destroyer, 2)

    def WhatCellWasClicked(self, pos):
        for j in range(10):
            for i in range(10):
                if self.guessing_grid[j][i].click(pos) and self.guessing_grid[j][i].hit_circle_color is None:
                    return self.guessing_grid[j][i]
        return None

    def WasShipHit(self, coordinates: tuple[int, int]):
        for cell in self.Carrier:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Carrier.remove(cell)
                if len(self.Carrier) == 0:
                    return SUNK_CARRIER, SUNK_CARRIER
                return HIT, HIT_CARRIER
        for cell in self.Battleship:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Battleship.remove(cell)
                if len(self.Battleship) == 0:
                    return SUNK_BATTLESHIP, SUNK_BATTLESHIP
                return HIT, HIT_BATTLESHIP
        for cell in self.Cruiser:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Cruiser.remove(cell)
                if len(self.Cruiser) == 0:
                    return SUNK_CRUISER, SUNK_CRUISER
                return HIT, HIT_CRUISER
        for cell in self.Submarine:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Submarine.remove(cell)
                if len(self.Submarine) == 0:
                    return SUNK_SUBMARINE, SUNK_SUBMARINE
                return HIT, HIT_SUBMARINE
        for cell in self.Destroyer:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Destroyer.remove(cell)
                if len(self.Destroyer) == 0:
                    return SUNK_DESTROYER, SUNK_DESTROYER
                return HIT, HIT_DESTROYER
        return MISS, MISS

    def isDoneValid(self):  # Checks to see with the player can press done or not
        if len(self.Carrier) == 5:
            if len(self.Battleship) == 4:
                if len(self.Cruiser) == 3:
                    if len(self.Submarine) == 3:
                        if len(self.Destroyer) == 2:
                            return True
        return False

    def AreAllShipsDown(self):
        if len(self.Carrier) == 0:
            if len(self.Battleship) == 0:
                if len(self.Cruiser) == 0:
                    if len(self.Submarine) == 0:
                        if len(self.Destroyer) == 0:
                            return True
        return False

    def DestroyedShipSpot(self, coordinates: tuple[int, int]):
        for cell in self.Carrier:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Carrier.remove(cell)

        for cell in self.Battleship:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Battleship.remove(cell)

        for cell in self.Cruiser:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Cruiser.remove(cell)

        for cell in self.Submarine:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Submarine.remove(cell)

        for cell in self.Destroyer:
            if cell.j == coordinates[0] and cell.i == coordinates[1]:
                self.Destroyer.remove(cell)

    def ChangeCellColorGuesserGrid(self, coordinates: tuple[int, int], color):
        for i in range(10):
            for j in range(10):
                if self.guessing_grid[i][j].j == coordinates[0] and self.guessing_grid[i][j].i == coordinates[1]:
                    self.guessing_grid[i][j].hit_circle_color = color
                    break

    def ChangeCellColorShipsGrid(self, coordinates: tuple[int, int], color):
        for i in range(10):
            for j in range(10):
                if self.ships_grid[i][j].j == coordinates[0] and self.ships_grid[i][j].i == coordinates[1]:
                    self.ships_grid[i][j].hit_circle_color = color
                    self.DestroyedShipSpot(coordinates)
                    break

    def CarrierStatus(self):
        if len(self.Carrier) > 0:
            text = createTextSys("comicsans", 40, "Carrier: Intact", BLACK)
        else:
            text = createTextSys("comicsans", 40, "Carrier: Sunk", BLACK)
        return text

    def BattleshipStatus(self):
        if len(self.Battleship) > 0:
            text = createTextSys("comicsans", 40, "Battleship: Intact", BLACK)
        else:
            text = createTextSys("comicsans", 40, "Battleship: Sunk", BLACK)
        return text

    def CruiserStatus(self):
        if len(self.Cruiser) > 0:
            text = createTextSys("comicsans", 40, "Cruiser: Intact", BLACK)
        else:
            text = createTextSys("comicsans", 40, "Cruiser: Sunk", BLACK)
        return text

    def SubmarineStatus(self):
        if len(self.Submarine) > 0:
            text = createTextSys("comicsans", 40, "Submarine: Intact", BLACK)
        else:
            text = createTextSys("comicsans", 40, "Submarine: Sunk", BLACK)
        return text

    def DestroyerStatus(self):
        if len(self.Destroyer) > 0:
            text = createTextSys("comicsans", 40, "Destroyer: Intact", BLACK)
        else:
            text = createTextSys("comicsans", 40, "Destroyer: Sunk", BLACK)
        return text
