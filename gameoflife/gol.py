import numpy as np

def get_neigh_coordinates(point, matrix_shape):
    """
    Get the coordinates of neighboring cells around a given point within a matrix.

    Args:
        point (tuple): The coordinates (row, column) of the center point.
        matrix_shape (tuple): The shape of the matrix (rows, columns).

    Returns:
        list of tuples: A list of tuples representing the coordinates of neighboring cells.
    """
    row, col = point
    rows, cols = matrix_shape

    return [(row + i, col + j) for i in range(-1, 2) for j in range(-1, 2)
                if (i != 0 or j != 0)  # Excluir la coordenada actual
                and 0 <= row + i < rows  # Verificar límites de filas
                and 0 <= col + j < cols]  # Verificar límites de columnas

def count_neighs(point, matrix):
    """
    Count the number of live neighbors around a given point in a matrix.

    Args:
        point (tuple): The coordinates (row, column) of the point.
        matrix (numpy.ndarray): The matrix representing the current state of the game.

    Returns:
        int: The count of live neighbors around the given point.
    """
    return sum(matrix[coords] for coords in get_neigh_coordinates(point, matrix.shape))

def play_game_of_life(matrix, n_iters=1):
    """
    Simulate the Game of Life on a given matrix for a specified number of iterations.

    Args:
        matrix (list or numpy.ndarray): The initial state of the matrix, where each element represents a cell.
        n_iters (int): The number of iterations to run the simulation (default is 1).

    Returns:
        numpy.ndarray: The state of the matrix after the specified number of iterations.
    """
    matrix = np.array(matrix).astype(bool)

    is_alive = [False, False, True, True, False, False, False, False, False]
    revives = [False, False, False, True, False, False, False, False, False]
    
    m = np.copy(matrix)

    states = set()
    states.add(tuple(m.flatten()))
    for state_index in range(n_iters):
        new_m = np.copy(m)

        alive_coords = np.argwhere(m)
        visited_coords = []
        for alive_coord in alive_coords:
            new_m[alive_coord[0], alive_coord[1]] = is_alive[count_neighs(alive_coord, m)]

            dead_neighs = [x for x in get_neigh_coordinates(alive_coord, m.shape)
                        if not m[x] and tuple(x) not in visited_coords]
            
            for dead_coord in dead_neighs:
                new_m[dead_coord[0], dead_coord[1]] = revives[count_neighs(dead_coord, m)]
                visited_coords.append(tuple(dead_coord))
        m = new_m

        if not m.any():
            break

        current_state = tuple(m.flatten())
        if current_state in states:
            print('loop detected, calculating state at iter {}'.format(n_iters))
            states_list = list(states)
            seen_state_index = states_list.index(current_state)
            if seen_state_index == state_index:
                return m
            n_iter_state_index = (n_iters - seen_state_index) % (state_index - seen_state_index) + seen_state_index
            return np.array(states_list[n_iter_state_index]).reshape(matrix.shape)
        else:
            states.add(current_state)

    return m