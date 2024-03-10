# Game of Life

The "Game of Life" is a cellular automaton (simulation) devised by the British mathematician John Horton Conway in 1970.
It is a 'zero-player' game, where each cell evolution is pre-defined by the initial state. 

## Installation

The package is installed as `conways-game-of-life`.

There is no PyPI release and it won't be, but the two following methods can be used to install the package.

### Method 1: pip

Install the repository with pip + git:

```shell
pip install git+https://github.com/Jtachan/Conways_GameOfLife.git
```

### Method 2: clone

Clone the repository.

```shell
git clone https://github.com/Jtachan/Conways_GameOfLife.git
```

Then install locally the package.

```shell
pip install .
```

## Usage

### CLI call

The game is launchable through the command line interface:

```commandline
game-of-life [-gw <grid-width>] [-gh <grid-height>]
```

- `grid-width`: Optional parameter to set the number of cells that compose the width of the grid. By default, it is set to 40.
- `grid-height`: Optional parameter to set the number of cells that compose the height of the grid. By default, it is set to 40. 

### Instructions

The following instructions are printed on the terminal:

```text
Conway's Game Of Life
---------------------

Welcome to the simulation!
Use the following commands to interact with it:
    - Use the space bar to stop/resume the simulation.
    - Press 'G' to generate a new random game.
    - Click on a cell with the mouse to update its state.
```

