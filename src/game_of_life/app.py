"""The module contains the class to launch the app."""
import random

import pygame
from pybase_ext.constants import RGB

pygame.init()


class GameOfLife:
    """Class containing the main code and all routines for the simulation."""

    TILE_SIZE = 20
    FPS = 10

    def __init__(self, width: int = 800, height: int = 800):
        """Constructor of the class.

        Parameters
        ----------
        width: int
            Number of pixels that represent the width of the screen.
        height: int
            Number of pixels that represent the height of the screen.
        """
        self._running = True
        self._playing = True
        self._grid_width = width // GameOfLife.TILE_SIZE
        self._grid_height = height // GameOfLife.TILE_SIZE

        self._screen = pygame.display.set_mode((width, width))
        self._clock = pygame.time.Clock()
        self._positions = self.generate_random_cells(
            random.randrange(3, 8) * self._grid_width
        )

    def generate_random_cells(self, nof_cells: int) -> set[tuple[int, int]]:
        """
        Generates randoms positions, without repeating them, to be considered
        as living cells.

        Parameters
        ----------
        nof_cells: int
            Ideal number of cells to generate.

        Returns
        -------
        set of positions:
            Final random generated positions. Its length might be lower than the
            specified number of cells, as the same cell position could be generated
            multiple times. This final returned value does not contain any repeated
            position.
        """
        return set(
            (
                random.randrange(0, self._grid_height),
                random.randrange(0, self._grid_width),
            )
            for _ in range(nof_cells)
        )

    def get_neighbors_positions(self, col: int, row: int) -> list[tuple[int, int]]:
        """
        Giving a cell coordinates, returns all its neighbors. The method does not
        consider the state of the cells at these positions.

        Parameters
        ----------
        col: int
            Number of the column, or X position, of the central cell.
        row: int
            Number of the row, or Y position, of the central cell.

        Returns
        -------
        list of tuples:
            List containing the neighbors' positions.
        """
        displacement = (-1, 0, 1)
        valid_neighbors = []

        for dx in displacement:
            cell_x = col + dx
            # Skip cells outside the width limits.
            if cell_x < 0 or cell_x > self._grid_width:
                continue
            for dy in displacement:
                cell_y = row + dy
                # Skip cells outside the height limits.
                if cell_y < 0 or cell_y > self._grid_height:
                    continue

                # Skip current cell
                if dx == 0 and dy == 0:
                    continue

                valid_neighbors.append((cell_x, cell_y))

        return valid_neighbors

    def calculate_next_cells_generation(self):
        """
        Calculates the positions of the cells to be alive at the next frame.

        Algorithm logic
        ---------------
        Cells update their position and other near cells by the following rules:

        * Birth: A cell becomes alive if it is surrounded exactly by three cells.
        * Death: A cell dies in one of two cases:
            - Overpopulation: If it is surrounded by more than three living cells.
            - Isolation: If it doesn't have any living neighbors.
        * Remain alive: If it has two or three living neighbors.
        """
        visited_neighbors = set()
        new_positions = set()

        for position in self._positions:
            neighbors = self.get_neighbors_positions(*position)
            visited_neighbors.update(neighbors)
            nof_neighbors = len(list(filter(lambda x: x in self._positions, neighbors)))

            if nof_neighbors in (2, 3):
                new_positions.add(position)

        for position in visited_neighbors:
            neighbors = self.get_neighbors_positions(*position)
            neighbors = list(filter(lambda x: x in self._positions, neighbors))

            if len(neighbors) == 3:
                new_positions.add(position)

        self._positions = new_positions

    def draw_grid(self):
        """
        Draws, on the screen, the vertical and horizontal lines that compose the grid.
        """
        width = self._screen.get_width()
        height = self._screen.get_height()

        for row in range(self._grid_height):
            row_cell_line_pos = row * GameOfLife.TILE_SIZE
            pygame.draw.line(
                surface=self._screen,
                color=RGB.BLACK,
                start_pos=(0, row_cell_line_pos),
                end_pos=(width, row_cell_line_pos),
            )

        for col in range(self._grid_width):
            col_cell_line_pos = col * GameOfLife.TILE_SIZE
            pygame.draw.line(
                surface=self._screen,
                color=RGB.BLACK,
                start_pos=(col_cell_line_pos, 0),
                end_pos=(col_cell_line_pos, height),
            )

    def paint_cells(self, positions: set[tuple[int, int]]):
        """
        Paints as yellow all the parsed cell positions.

        Parameters
        ----------
        positions: set of cell coordinates
            All cells' positions, specified as (col, row), representing the
            living cells.
        """
        size = GameOfLife.TILE_SIZE
        for col, row in positions:
            cell_rect = (col * size, row * size, size, size)
            pygame.draw.rect(surface=self._screen, color=RGB.YELLOW, rect=cell_rect)

    def update_display(self):
        """
        Method to be called every iteration, holding all the drawing functions that
        refer to the grid (the display).
        """
        self._screen.fill(color=RGB.SILVER)
        self.draw_grid()
        self.paint_cells(self._positions)
        pygame.display.update()

    def update_mouse_clicked_cell(self):
        """Updates the state of the cell, which was clicked by the mouse."""
        pixel_x, pixel_y = pygame.mouse.get_pos()
        cell_pos = (pixel_x // GameOfLife.TILE_SIZE, pixel_y // GameOfLife.TILE_SIZE)

        if cell_pos in self._positions:
            self._positions.remove(cell_pos)
        else:
            self._positions.add(cell_pos)

    def run(self):
        """Main run loop for the game."""
        pygame.display.set_caption("Playing")
        self.print_instructions()

        while self._running:
            self._clock.tick(GameOfLife.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_mouse_clicked_cell()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._playing = not self._playing
                        pygame.display.set_caption(
                            "Playing" if self._playing else "Paused"
                        )
                    elif event.key == pygame.K_g:
                        self._positions = self.generate_random_cells(
                            nof_cells=random.randrange(4, 8) * self._grid_width
                        )

            self.update_display()
            if self._playing:
                self.calculate_next_cells_generation()

        pygame.quit()

    @staticmethod
    def print_instructions():
        """Prints the instructions to understand how to use the keys on the terminal."""
        print(
            "Conway's Game Of Life\n"
            "---------------------\n\n"
            "Welcome to the simulation!\n"
            "Use the following commands to interact with it:\n"
            "\t- Use the space bar to stop/resume the simulation.\n"
            "\t- Press 'G' to generate a new random game.\n"
            "\t- Click on a cell with the mouse to update its state."
        )


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
