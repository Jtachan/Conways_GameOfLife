"""main"""
import random
from typing import Optional

import pygame
from pybase_ext.constants import RGB

pygame.init()

WIDTH = 800
HEIGHT = 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 10


class GameOfLife:
    def __init__(self):
        self._running = True
        self._playing = True
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._clock = pygame.time.Clock()
        self._positions = self.generate_random_cells(
            random.randrange(3, 8) * GRID_WIDTH
        )

    @staticmethod
    def generate_random_cells(nof_cells: int) -> set[tuple[int, int]]:
        return set(
            (random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH))
            for _ in range(nof_cells)
        )

    @staticmethod
    def get_neighbors(pos_x: int, pos_y: int) -> list[tuple[int, int]]:
        displacement = (-1, 0, 1)
        valid_neighbors = []

        for dx in displacement:
            cell_x = pos_x + dx
            # Skip cells outside the width limits.
            if cell_x < 0 or cell_x > GRID_WIDTH:
                continue
            for dy in displacement:
                cell_y = pos_y + dy
                # Skip cells outside the height limits.
                if cell_y < 0 or cell_y > GRID_HEIGHT:
                    continue

                # Skip current cell
                if dx == 0 and dy == 0:
                    continue

                valid_neighbors.append((cell_x, cell_y))

        return valid_neighbors

    def calculate_next_cells_generation(self):
        all_cells_neighbors = set()
        new_positions = set()

        for position in self._positions:
            neighbors = self.get_neighbors(*position)
            all_cells_neighbors.update(neighbors)
            neighbors = list(filter(lambda x: x in self._positions, neighbors))

            if len(neighbors) in (2, 3):
                new_positions.add(position)

        for position in all_cells_neighbors:
            neighbors = self.get_neighbors(*position)
            neighbors = list(filter(lambda x: x in self._positions, neighbors))

            if len(neighbors) == 3:
                new_positions.add(position)

        self._positions = new_positions

    def draw_grid(self):
        for row in range(GRID_HEIGHT):
            row_cell_line_pos = row * TILE_SIZE
            pygame.draw.line(
                surface=self._screen,
                color=RGB.BLACK,
                start_pos=(0, row_cell_line_pos),
                end_pos=(WIDTH, row_cell_line_pos),
            )

        for col in range(GRID_WIDTH):
            col_cell_line_pos = col * TILE_SIZE
            pygame.draw.line(
                surface=self._screen,
                color=RGB.BLACK,
                start_pos=(col_cell_line_pos, 0),
                end_pos=(col_cell_line_pos, HEIGHT),
            )

    def paint_cells(self, positions: Optional[set[tuple[int, int]]] = None):
        for col, row in positions:
            cell_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface=self._screen, color=RGB.YELLOW, rect=cell_rect)

    def update_display(self):
        self._screen.fill(color=RGB.SILVER)
        self.draw_grid()
        self.paint_cells(self._positions)
        pygame.display.update()

    def update_mouse_clicked_cell(self):
        pixel_x, pixel_y = pygame.mouse.get_pos()
        cell_pos = (pixel_x // TILE_SIZE, pixel_y // TILE_SIZE)

        if cell_pos in self._positions:
            self._positions.remove(cell_pos)
        else:
            self._positions.add(cell_pos)

    def run(self):

        while self._running:
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.update_mouse_clicked_cell()

            self.update_display()
            self.calculate_next_cells_generation()

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
