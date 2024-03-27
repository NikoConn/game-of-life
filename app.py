import numpy as np
import cv2
from gameoflife import play_game_of_life
import argparse

help_page = "Press 'q' to quit\nPress 'n' to advance simulation by one iteration\nPress 'c' to clear the grid\nPress 'p' to toggle play/pause\nPress 'h' to print this help page\nDouble-click on a cell to toggle its state"


def draw_grid_with_bool_matrix(bool_matrix, square_size, line_thickness):
    """
    Draw a grid based on a boolean matrix representation.

    Args:
        bool_matrix (numpy.ndarray): The boolean matrix representing the state of the grid.
        square_size (int): The size of each square in pixels.
        line_thickness (int): The thickness of grid lines in pixels.

    Returns:
        numpy.ndarray: An image representing the grid with the specified parameters.
    """
    rows, columns = bool_matrix.shape

    total_width = columns * square_size + (columns + 1) * line_thickness
    total_height = rows * square_size + (rows + 1) * line_thickness

    grid_image = np.ones((total_height, total_width), dtype=np.uint8) * 255  # White background

    for i in range(0, total_height, square_size + line_thickness):
        cv2.line(grid_image, (0, i), (total_width, i), color=127, thickness=line_thickness)

    for j in range(0, total_width, square_size + line_thickness):
        cv2.line(grid_image, (j, 0), (j, total_height), color=127, thickness=line_thickness)

    for i in range(rows):
        for j in range(columns):
            if bool_matrix[i, j]:
                x1 = j * (square_size + line_thickness) + line_thickness
                y1 = i * (square_size + line_thickness) + line_thickness
                x2 = x1 + square_size - 1
                y2 = y1 + square_size - 1
                cv2.rectangle(grid_image, (x1, y1), (x2, y2), color=0, thickness=-1)

    return grid_image

class GoLVisualizer():
    """
    Class for visualizing the Game of Life simulation.

    Attributes:
        WINDOW_NAME (str): The name of the window for displaying the visualization.
        state (numpy.ndarray): The current state of the simulation.
        square_size (int): The size of each square in pixels.
        line_thickness (int): The thickness of grid lines in pixels.
        playing (bool): Flag indicating whether the simulation is playing or paused.
        help_visible (bool): Flag indicating whether the help page is currently visible.
    """

    def __init__(self, initial_state=None, square_size=5, line_thickness=1):
        """
        Initialize the visualizer.

        Args:
            initial_state (numpy.ndarray, optional): The initial state of the simulation (default is None).
            square_size (int, optional): The size of each square in pixels (default is 5).
            line_thickness (int, optional): The thickness of grid lines in pixels (default is 1).
        """
        if initial_state is None:
            initial_state = np.full([1, 1], False)
        
        self.WINDOW_NAME = 'Game of Life'
        self.state = initial_state
        self.square_size = square_size
        self.line_thickness = line_thickness
        self.playing = False

        grid = draw_grid_with_bool_matrix(self.state, self.square_size, self.line_thickness)

        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.WINDOW_NAME, self.mouse_callback)
        cv2.imshow(self.WINDOW_NAME, grid)

        while cv2.getWindowProperty(self.WINDOW_NAME, cv2.WND_PROP_VISIBLE) > 0:
            keyCode = cv2.waitKey(1) & 0xFF

            if keyCode == ord('q'):
                break
            if keyCode == ord('n'):
                self.state = play_game_of_life(self.state, 1)
                grid = draw_grid_with_bool_matrix(self.state, self.square_size, self.line_thickness)
                cv2.imshow(self.WINDOW_NAME, grid)
            if keyCode == ord('c'):
                self.state = np.full(self.state.shape, False)
                grid = draw_grid_with_bool_matrix(self.state, self.square_size, self.line_thickness)
                cv2.imshow(self.WINDOW_NAME, grid)
            if keyCode == ord('p'):
                self.playing = not self.playing
            
            if self.playing:
                self.state = play_game_of_life(self.state, 1)
                grid = draw_grid_with_bool_matrix(self.state, self.square_size, self.line_thickness)
                cv2.imshow(self.WINDOW_NAME, grid)
            if keyCode == ord('h'):
                print(help_page)

        cv2.destroyWindow(self.WINDOW_NAME)

    def mouse_callback(self, event, x, y, flags, param):
        """
        Handle mouse events for toggling cell states.

        Args:
            event: The mouse event.
            x (int): The x-coordinate of the mouse position.
            y (int): The y-coordinate of the mouse position.
            flags: Additional flags.
            param: Additional parameters.
        """
        if event != cv2.EVENT_LBUTTONDBLCLK:
            return
        
        x_adjusted = x - self.line_thickness
        y_adjusted = y - self.line_thickness

        row = y_adjusted // (self.square_size + self.line_thickness)
        column = x_adjusted // (self.square_size + self.line_thickness)

        self.state[row, column] = not self.state[row, column]
        grid = draw_grid_with_bool_matrix(self.state, self.square_size, self.line_thickness)
        cv2.imshow(self.WINDOW_NAME, grid)

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Game of Life Visualizer.', epilog='Press h to print help page.')
    parser.add_argument('--rows', type=int, default=100, help='Number of rows in the matrix')
    parser.add_argument('--columns', type=int, default=200, help='Number of columns in the matrix')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    m = np.full([args.rows, args.columns], False)
    visualizer = GoLVisualizer(m)
