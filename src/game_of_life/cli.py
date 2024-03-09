"""This module contains the entry point for the command line interface."""
import argparse

from game_of_life.app import GameOfLife


def launch_game():
    """Entry point of the CLI to launch the game."""
    parser = argparse.ArgumentParser(
        description=(
            "Launcher to play Conway's Game of Life, a zero-player cell simulator."
        )
    )
    parser.add_argument(
        "-gw",
        "--grid-width",
        help="Number of cells that represent the width of the grid.",
        type=int,
        default=40,
    )
    parser.add_argument(
        "-gh",
        "--grid-height",
        help="Number of cells that represent the height of the grid.",
        type=int,
        default=40,
    )
    args = parser.parse_args()

    app = GameOfLife(grid_width=args.grid_width, grid_height=args.grid_height)
    app.run()
