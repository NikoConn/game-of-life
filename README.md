# Game of Life Visualizer

This is a Python program that visualizes [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). It provides an interactive interface for users to interact with the simulation.

## Features

- Interactive grid where users can toggle the state of cells
- Play/pause functionality to run the simulation automatically
- Advance simulation by one iteration
- Clear the grid
- Help page to guide users on how to use the interface

## Usage

1. Clone the repository:

```bash
git clone https://github.com/NikoConn/game-of-life.git
```

2. Navigate to the project directory:

```bash
cd game-of-life
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Run the visualizer:

```bash
python app.py
```

Use the following keys to interact with the simulation:

```
q: Quit the program
n: Advance simulation by one iteration
c: Clear the grid
p: Toggle play/pause
h: Toggle help page
Double-click on a cell to toggle its state
```

## API

The project includes a package `gameoflife` which provides a function for Game of Life simulation. 

```python
from gameoflife import play_game_of_life
```

#### `play_game_of_life(matrix, n_iters=1)`


Simulate the Game of Life on a given matrix for a specified number of iterations.

Args:
* matrix (list or numpy.ndarray): The initial state of the matrix, where each element represents a cell.
* n_iters (int): The number of iterations to run the simulation (default is 1).

Returns:
* numpy.ndarray: The state of the matrix after the specified number of iterations.

Example:
```python
from gameoflife import play_game_of_life
import numpy as np

m = np.full([3, 3], False)
m[1] = True
play_game_of_life(m, 100)
```

Prints

```python
array([[False, False, False],
       [ True,  True,  True],
       [False, False, False]])
```